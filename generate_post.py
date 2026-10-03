import os
import re
import json
import random
import time
import urllib.request
import urllib.parse
import urllib.error
import base64
from datetime import datetime, timezone, timedelta
from PIL import Image, ImageDraw

# 1. 한국 시간대(KST = UTC+9) 및 날짜 포맷 설정
KST = timezone(timedelta(hours=9))
now = datetime.now(KST)
date_dash = now.strftime("%Y-%m-%d")    # YYYY-MM-DD
date_compact = now.strftime("%Y%m%d")   # YYYYMMDD
date_full = now.strftime("%Y-%m-%d %H:%M:%S +0900") # 타임존 포함 날짜

# 2. 토큰 검증
token = os.environ.get("GH_MODELS_TOKEN")
if not token:
    raise ValueError("GH_MODELS_TOKEN 환경 변수가 설정되지 않았습니다.")

# 2-1. GitHub Models 직접 호출 함수 (SDK 미사용, 순수 REST API)
def query_github_models(messages, model="gpt-4o", temperature=0.7, max_tokens=1000, max_retries=3):
    """
    OpenAI SDK 호환성 문제 및 'OK' 텍스트 반환 버그를 방지하기 위해
    GitHub Models API 규격에 맞춰 직접 HTTP POST 호출을 수행합니다.
    """
    # 1순위: GitHub Models 표준 엔드포인트, 2순위: 대체 엔드포인트
    endpoints = [
        "https://models.inference.ai.azure.com/chat/completions",
        "https://models.github.ai/inference/chat/completions"
    ]
    
    payload = {
        "messages": messages,
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    json_data = json.dumps(payload).encode("utf-8")
    
    for attempt in range(1, max_retries + 1):
        for endpoint in endpoints:
            try:
                req = urllib.request.Request(
                    endpoint,
                    data=json_data,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {token}",
                        "User-Agent": "GitHubAction-PostGenerator/1.0"
                    }
                )
                
                with urllib.request.urlopen(req, timeout=90) as response:
                    res_body = response.read().decode("utf-8")
                    
                    # 단순 상태 텍스트("OK") 필터링
                    if res_body.strip().upper() == "OK":
                        continue
                    
                    parsed = json.loads(res_body)
                    if "choices" in parsed and len(parsed["choices"]) > 0:
                        content = parsed["choices"][0]["message"]["content"]
                        if content and content.strip().upper() != "OK":
                            return content.strip()

            except urllib.error.HTTPError as http_err:
                err_detail = http_err.read().decode("utf-8", errors="ignore")
                print(f"[HTTP 오류 {http_err.code}] {endpoint}: {err_detail[:150]}")
            except Exception as e:
                print(f"[{endpoint} 호출 실패]: {e}")

        sleep_sec = attempt * 3
        print(f"⏳ {sleep_sec}초 후 API 재시도 ({attempt}/{max_retries})...")
        time.sleep(sleep_sec)

    raise RuntimeError("모든 엔드포인트에서 유효한 응답을 수신하지 못했습니다.")

# 3. 최신 IT 동향 및 핵심 기술 주제를 동적으로 가져오는 함수
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
4. 선택된 주제가 고급/차세대 개념인 경우, 범용적인 기초 예제(예: 기본 EC2 생성)가 아닌 해당 주제의 핵심을 직접 다루는 심화 코드(예: Redfish API, CXL resource pool, Kubernetes CRD 등)를 작성할 것.
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
        print(f"[경고] 동적 주제 생성 실패({e}). 기본 예비 목록에서 임의 선택합니다.")
    
    return random.choice(fallback_categories)

# 4. 예외 발생 시 대체 이미지를 만드는 함수
def create_fallback_image(img_path, category_text):
    width, height = 500, 300
    img = Image.new('RGB', (width, height), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)
    draw.rectangle([5, 5, width - 6, height - 6], outline=(56, 189, 248), width=2)
    text = f"Tech Topic:\n{category_text}"
    draw.text((30, 120), text, fill=(241, 245, 249))
    img.save(img_path, "PNG")
    print(f"⚠️ 대체 이미지 생성 완료: {img_path}")

# 5. Pollinations.ai API를 활용한 이미지 생성
def generate_and_save_image(img_dir, category):
    img_path = os.path.join(img_dir, "0_.png")
    temp_download_path = os.path.join(img_dir, "temp_raw.png")
    
    prompt = f"A high quality visual technical architecture diagram representing {category}, professional tech blog style, modern infographic with clean node graphs, dark background, vector art"
    encoded_prompt = urllib.parse.quote(prompt)
    
    seed = random.randint(10000, 99999)
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1000&height=600&seed={seed}&nologo=true&model=flux"
    
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

        print(f"✅ 무료 AI 이미지 생성 및 500x300 저장 완료: {img_path}")
        return True

    except Exception as e:
        print(f"[경고] 이미지 생성 중 오류 발생: {e}")
        if os.path.exists(temp_download_path):
            os.remove(temp_download_path)
            
        create_fallback_image(img_path, category)
        return False

# 6. 기술 포스팅 생성
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

# 7. 엔트리포인트 실행
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
    
    if len(final_content.strip()) < 100 or "---" not in final_content:
        raise ValueError(f"유효하지 않은 본문 내용입니다 ({len(final_content)}자). 저장을 취소합니다.")

    filename = os.path.join(posts_dir, f"{date_dash}-{date_compact}.md")
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(final_content)
        
    print(f"✅ 포스팅 생성 완벽 종료 ({len(final_content)}자 저장됨): {filename}")

if __name__ == "__main__":
    main()
