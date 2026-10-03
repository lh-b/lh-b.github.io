import os
import re
import json
import random
import time
import socket
import ssl
import subprocess
import urllib.request
import urllib.parse
import urllib.error
import base64
from datetime import datetime, timezone, timedelta
from PIL import Image, ImageDraw

# ====================================================
# 0. 네트워크 & DNS 안정화 (Errno -2 및 SSL 오류 차단)
# ====================================================
TARGET_HOST = "models.inference.ai.azure.com"

def setup_reliable_dns():
    """
    1. 러너의 /etc/resolv.conf를 구글/클라우드플레어 공용 DNS로 갱신 시도
    2. 해석 실패 시 DoH(8.8.8.8)를 통해 실제 A 레코드 IP를 직접 획득하여 바인딩
    """
    # 1단계: OS 레벨 DNS 갱신 (GitHub Actions 러너 환경 대응)
    try:
        resolv_content = "nameserver 8.8.8.8\nnameserver 1.1.1.1\noptions timeout:2 attempts:3\n"
        with open("/tmp/resolv_override.conf", "w") as f:
            f.write(resolv_content)
        subprocess.run(
            ["sudo", "cp", "/tmp/resolv_override.conf", "/etc/resolv.conf"],
            check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
    except Exception:
        pass

    # 2단계: 시스템 DNS 테스트
    orig_getaddrinfo = socket.getaddrinfo
    try:
        res = orig_getaddrinfo(TARGET_HOST, 443, socket.AF_INET, socket.SOCK_STREAM)
        if res:
            print(f"🌐 [DNS 확인 성공] 시스템 DNS가 정상적으로 {TARGET_HOST}를 해석합니다.")
            return
    except Exception:
        print(f"⚠️ 시스템 DNS 해석 실패. DoH(8.8.8.8)를 통해 IP 직접 조회를 시도합니다.")

    # 3단계: DoH IP(8.8.8.8)를 통해 실제 A 레코드 IP 조회
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        doh_url = f"https://8.8.8.8/resolve?name={TARGET_HOST}&type=A"
        req = urllib.request.Request(doh_url, headers={"Accept": "application/json", "User-Agent": "curl/7.68.0"})
        with urllib.request.urlopen(req, context=ctx, timeout=6) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            real_ip = None
            for ans in data.get("Answer", []):
                if ans.get("type") == 1:  # IPv4 A 레코드
                    real_ip = ans.get("data")
                    break

            if real_ip:
                print(f"🌐 [DoH 매핑 완료] {TARGET_HOST} -> {real_ip}")
                def custom_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
                    if host == TARGET_HOST:
                        p = int(port) if port else 443
                        return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (real_ip, p))]
                    return orig_getaddrinfo(host, port, family, type, proto, flags)
                socket.getaddrinfo = custom_getaddrinfo
            else:
                print("⚠️ DoH에서 A 레코드를 찾지 못함. 기본 시스템 리졸버를 유지합니다.")
    except Exception as e:
        print(f"⚠️ DoH 조회 중 오류: {e}. 기본 리졸버를 유지합니다.")

# DNS 설정 실행
setup_reliable_dns()

# ====================================================
# 1. 시간대(KST = UTC+9) 및 날짜 설정
# ====================================================
KST = timezone(timedelta(hours=9))
now = datetime.now(KST)
date_dash = now.strftime("%Y-%m-%d")    # YYYY-MM-DD
date_compact = now.strftime("%Y%m%d")   # YYYYMMDD
date_full = now.strftime("%Y-%m-%d %H:%M:%S +0900")

# ====================================================
# 2. 토큰 및 REST API 통신 모듈
# ====================================================
token = os.environ.get("GH_MODELS_TOKEN")
if not token:
    raise ValueError("GH_MODELS_TOKEN 환경 변수가 설정되지 않았습니다.")

def query_github_models(messages, model="gpt-4o", temperature=0.7, max_tokens=1000, max_retries=4):
    """
    GitHub Models 공식 엔드포인트로 직접 POST 요청을 전송합니다.
    """
    url = f"https://{TARGET_HOST}/chat/completions"
    payload = {
        "messages": messages,
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    json_bytes = json.dumps(payload).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
        "User-Agent": "GitHubAction-PostGenerator/1.0"
    }

    for attempt in range(1, max_retries + 1):
        try:
            req = urllib.request.Request(url, data=json_bytes, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=120) as resp:
                raw_body = resp.read().decode("utf-8")
                
                # 게이트웨이 텍스트('OK') 필터링
                if not raw_body or raw_body.strip().upper() == "OK":
                    raise ValueError(f"비정상 응답 수신: '{raw_body}'")

                parsed = json.loads(raw_body)
                if "choices" in parsed and len(parsed["choices"]) > 0:
                    content = parsed["choices"][0].get("message", {}).get("content", "")
                    if content and len(content.strip()) > 5:
                        return content.strip()
                raise ValueError("응답 내 본문 데이터(content) 누락")

        except urllib.error.HTTPError as http_err:
            err_msg = http_err.read().decode("utf-8", errors="ignore")
            print(f"[시도 {attempt}/{max_retries}] HTTP 오류 {http_err.code}: {err_msg[:200]}")
            if http_err.code == 401:
                raise RuntimeError("GH_MODELS_TOKEN 인증 실패(401). GitHub 시크릿 토큰을 확인하세요.") from http_err
        except Exception as e:
            print(f"[시도 {attempt}/{max_retries}] API 요청 실패: {e}")

        if attempt < max_retries:
            wait_sec = attempt * 4
            print(f"⏳ {wait_sec}초 후 재시도합니다...")
            time.sleep(wait_sec)

    raise RuntimeError(f"최대 재시도 횟수({max_retries}회)를 초과하여 API 응답 수신에 실패했습니다.")

# ====================================================
# 3. 최신 IT 주제 동적 선정
# ====================================================
def get_latest_tech_topic():
    fallback_categories = [
        "Agentic AI Systems & Multi-Agent Workflows",
        "Retrieval-Augmented Generation (RAG) & Vector Search",
        "Multimodal AI & Visual Language Models",
        "LLMOps, Evaluation & AI Observability",
        "Edge AI & On-Device Inference Optimization",
        "eBPF & Modern Cloud-Native Observability",
        "High-Performance System Architecture with Rust",
        "Zero Trust Security & AI Governance",
        "Real-Time Data Streaming & Lakehouse Architecture"
    ]

    system_prompt = """
너는 글로벌 IT 기술 트렌드 분석가이자 최고 기술 책임자(CTO)이다.
현재 최신 IT/소프트웨어 엔지니어링 분야에서 가장 중요한 실무 아키텍처 및 트렌드 주제 1개를 선정하라.

[선정 조건]
1. 단순 추상적/마케팅 용어가 아니라 실제 코드 및 기술 아키텍처로 구현 가능한 구체적인 엔지니어링 주제일 것.
2. 영문 제목으로 명확하고 간결하게 출력할 것 (예: "Agentic Multi-Agent Workflows with LangGraph", "eBPF-driven Zero Trust Network Security").
3. 따옴표, 설명, 번호 등의 부연 설명 없이 오직 '주제명 텍스트'만 단 한 줄로 출력할 것.
4. 선택된 주제가 고급/차세대 개념인 경우, 범용적인 기초 예제가 아닌 해당 주제의 핵심을 직접 다루는 심화 코드를 작성할 것.
"""
    user_prompt = f"오늘 날짜({date_dash}) 기준, 최근 IT 산업에서 가장 주목받고 가치 있는 고난도 기술 주제 1개를 선정해줘."

    try:
        topic_raw = query_github_models(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model="gpt-4o",
            temperature=0.7,
            max_tokens=100
        )
        
        topic = topic_raw.strip().strip('"').strip("'")
        if topic and len(topic) > 3 and topic.upper() != "OK":
            print(f"✨ 동적 생성된 최신 IT 주제: {topic}")
            return topic
            
    except Exception as e:
        print(f"[경고] 동적 주제 생성 실패({e}). 기본 예비 목록에서 선택합니다.")
    
    return random.choice(fallback_categories)

# ====================================================
# 4. 이미지 생성 및 폴백 처리
# ====================================================
def create_fallback_image(img_path, category_text):
    width, height = 500, 300
    img = Image.new('RGB', (width, height), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)
    draw.rectangle([5, 5, width - 6, height - 6], outline=(56, 189, 248), width=2)
    text = f"Tech Topic:\n{category_text}"
    draw.text((30, 120), text, fill=(241, 245, 249))
    img.save(img_path, "PNG")
    print(f"⚠️ 대체 이미지 생성 완료: {img_path}")

def generate_and_save_image(img_dir, category):
    img_path = os.path.join(img_dir, "0_.png")
    temp_download_path = os.path.join(img_dir, "temp_raw.png")
    
    prompt = f"A high quality visual technical architecture diagram representing {category}, professional tech blog style, modern infographic with clean node graphs, dark background, vector art"
    encoded_prompt = urllib.parse.quote(prompt)
    seed = random.randint(10000, 99999)
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1000&height=600&seed={seed}&nologo=true"
    
    try:
        req = urllib.request.Request(
            image_url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        
        with urllib.request.urlopen(req, timeout=60) as response, open(temp_download_path, 'wb') as out_file:
            out_file.write(response.read())

        with Image.open(temp_download_path) as img:
            target_width, target_height = 500, 300
            img_ratio = img.width / img.height
            target_ratio = target_width / target_height

            if img_ratio > target_ratio:
                new_width = int(target_ratio * img.height)
                offset = (img.width - new_width) // 2
                crop_box = (offset, 0, offset + new_width, img.height)
            else:
                new_height = int(img.width / target_ratio)
                offset = (img.height - new_height) // 2
                crop_box = (0, offset, img.width, offset + new_height)

            cropped_img = img.crop(crop_box)
            resized_img = cropped_img.resize((target_width, target_height), Image.Resampling.LANCZOS)
            resized_img.save(img_path, "PNG")

        if os.path.exists(temp_download_path):
            os.remove(temp_download_path)

        print(f"✅ AI 이미지 생성 및 저장 완료: {img_path}")
        return True

    except Exception as e:
        print(f"[경고] AI 이미지 생성 실패({e}). 대체 이미지로 전환합니다.")
        if os.path.exists(temp_download_path):
            os.remove(temp_download_path)
            
        create_fallback_image(img_path, category)
        return False

# ====================================================
# 5. 기술 포스팅 생성
# ====================================================
def generate_article(category):
    safe_title = json.dumps(category, ensure_ascii=False)
    first_tag = re.sub(r'[^a-zA-Z0-9]', '', category.split()[0])

    system_prompt = f"""
너는 IT 분야 수석 엔지니어이다.
주어진 주제에 맞춰 깊이 있는 기술 문서를 작성하라.

[어조 및 스타일 규칙 - 엄격 준수]
1. 존댓말(~해요, ~합니다, ~습니다)을 절대로 사용하지 말 것.
2. 개조식 표현(~함, ~임) 또는 서술용 평어/해라체(~다, ~한다)만 사용할 것.

[Frontmatter 규칙]
---
title: {safe_title}
date: {date_full}
tags:
  - IT Technology
  - {first_tag}
  - Engineering
header:
  teaser: /assets/images/{date_compact}/0_.png
toc: true
toc_sticky: true
excerpt_separator: <!--more-->
---

[본문 필수 구조]
1. 개요 서술 후 `<!--more-->` 주석 필수 삽입.
2. 시스템 아키텍처 / 데이터 흐름을 설명하는 Mermaid 다이어그램 작성 (```mermaid 코드 블록 사용).
3. 기술 개요 및 핵심 원리 설명.
4. 실무에서 검증된 코드 구현체(Python/PyTorch/Pandas 등)와 사용 가이드 작성.
5. 적용 시 장단점 및 고려사항 명시.
"""

    user_prompt = f"""
오늘 날짜: {date_dash}
주제: {category}

해당 분야의 핵심 기술을 선정하여 실무 중심의 기술 문서를 작성하라.
"""

    content = query_github_models(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        model="gpt-4o",
        temperature=0.3,
        max_tokens=3500,
        max_retries=4
    )
    
    return content

def clean_markdown_output(text):
    text = text.strip()
    if text.startswith("```markdown"):
        text = text[11:].lstrip()
    elif text.startswith("```"):
        text = text[3:].lstrip()
    
    if text.endswith("```"):
        text = text[:-3].rstrip()
        
    return text.strip()

def convert_mermaid_to_image_tag(text):
    def replace_match(match):
        mermaid_code = match.group(1).strip()
        encoded_bytes = base64.b64encode(mermaid_code.encode('utf-8'))
        base64_str = encoded_bytes.decode('utf-8')
        image_url = f"https://mermaid.ink/svg/{base64_str}"
        return f"![System Architecture]({image_url})"

    pattern = r"```mermaid\s*\n(.*?)```"
    return re.sub(pattern, replace_match, text, flags=re.DOTALL)

# ====================================================
# 6. 메인 실행부
# ====================================================
def main():
    posts_dir = "_posts"
    img_dir = f"assets/images/{date_compact}"
    
    os.makedirs(posts_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)

    selected_category = get_latest_tech_topic()
    print(f"🎯 최종 작성 주제: {selected_category}")

    generate_and_save_image(img_dir, selected_category)

    content = generate_article(selected_category)
    cleaned_content = clean_markdown_output(content)
    final_content = convert_mermaid_to_image_tag(cleaned_content)
    
    # 생성된 글 유효성 최종 검증 (단문 방지)
    if len(final_content.strip()) < 150 or "---" not in final_content:
        raise ValueError(f"생성된 포스팅 내용이 유효하지 않습니다 ({len(final_content)}자). 저장을 취소합니다.")

    filename = os.path.join(posts_dir, f"{date_dash}-{date_compact}.md")
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(final_content)
        
    print(f"✅ 포스팅 생성 완벽 종료 ({len(final_content)}자 저장 완료): {filename}")

if __name__ == "__main__":
    main()
