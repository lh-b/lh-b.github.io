import os
import re
import json
import random
import time
import subprocess
import urllib.request
import urllib.parse
import base64
from datetime import datetime, timezone, timedelta
from PIL import Image, ImageDraw

# ====================================================
# 상수 정의 (마크다운 백틱 문자 충돌 방지)
# ====================================================
TICK = "```"

# 1. 한국 시간대(KST = UTC+9) 및 날짜 포맷 설정
KST = timezone(timedelta(hours=9))
now = datetime.now(KST)
date_dash = now.strftime("%Y-%m-%d")    # YYYY-MM-DD
date_compact = now.strftime("%Y%m%d")   # YYYYMMDD
date_full = now.strftime("%Y-%m-%d %H:%M:%S +0900") # 타임존 포함 날짜

# 2. 토큰 확인
token = os.environ.get("GH_MODELS_TOKEN")
if not token:
    raise ValueError("GH_MODELS_TOKEN 환경 변수가 설정되지 않았습니다.")

# ====================================================
# 2-1. curl + DoH(DNS-over-HTTPS) 기반 API 호출
# (Ubuntu 러너의 DNS 차단 및 SSL Hostname 불일치 완벽 해결)
# ====================================================
def query_github_models_via_curl(messages, model="gpt-4o", temperature=0.7, max_tokens=3000):
    url = "[https://models.inference.ai.azure.com/chat/completions](https://models.inference.ai.azure.com/chat/completions)"
    payload = {
        "messages": messages,
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    json_payload = json.dumps(payload, ensure_ascii=False)
    
    # 443 포트로 DNS를 질의하여 Azure 방화벽(53 포트 차단) 및 CNAME 오류 우회
    doh_resolvers = [
        "[https://dns.google/dns-query](https://dns.google/dns-query)",
        "[https://cloudflare-dns.com/dns-query](https://cloudflare-dns.com/dns-query)"
    ]

    for doh in doh_resolvers:
        try:
            cmd = [
                "curl", "-s", "-X", "POST", url,
                "--doh-url", doh,
                "-H", f"Authorization: Bearer {token}",
                "-H", "Content-Type: application/json",
                "-d", json_payload,
                "--max-time", "75"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=85)
            
            if result.returncode == 0 and result.stdout:
                res_body = result.stdout.strip()
                if res_body.upper() == "OK":
                    continue
                
                parsed = json.loads(res_body)
                if "choices" in parsed and len(parsed["choices"]) > 0:
                    content = parsed["choices"][0].get("message", {}).get("content", "")
                    if content and len(content.strip()) > 10:
                        print(f"✅ GitHub Models API 호출 성공 (DoH: {doh})")
                        return content.strip()
                elif "error" in parsed:
                    print(f"⚠️ API 반환 에러: {parsed['error'].get('message')}")
        except Exception as e:
            print(f"⚠️ curl ({doh}) 호출 예외: {e}")
            
    return None

# ====================================================
# 3. 최신 IT 주제 동적 선정 (API 실패 시 Fallback 지원)
# ====================================================
def get_latest_tech_topic():
    fallback_categories = [
        "High-Performance System Architecture with Rust",
        "Agentic AI Systems & Multi-Agent Workflows",
        "Retrieval-Augmented Generation (RAG) & Vector Search",
        "LLMOps, Evaluation & AI Observability",
        "eBPF & Modern Cloud-Native Observability",
        "Zero Trust Security & AI Governance",
        "Real-Time Data Streaming & Lakehouse Architecture"
    ]

    system_prompt = (
        "너는 글로벌 IT 기술 트렌드 분석가이자 최고 기술 책임자(CTO)이다.\n"
        "현재 최신 IT/소프트웨어 엔지니어링 분야에서 가장 중요한 실무 아키텍처 및 트렌드 주제 1개를 선정하라.\n"
        "설명 없이 오직 '영문 주제명 텍스트'만 단 한 줄로 출력하라."
    )
    user_prompt = f"오늘 날짜({date_dash}) 기준, 최근 IT 산업에서 가장 주목받고 가치 있는 고난도 기술 주제 1개를 선정해줘."

    topic = query_github_models_via_curl(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        model="gpt-4o",
        temperature=0.7,
        max_tokens=80
    )

    if topic and len(topic) > 3 and "\n" not in topic:
        clean_topic = topic.strip().strip('"').strip("'")
        print(f"✨ 동적 생성된 최신 IT 주제: {clean_topic}")
        return clean_topic

    selected = random.choice(fallback_categories)
    print(f"ℹ️ 사전 정의된 추천 주제 적용: {selected}")
    return selected

# ====================================================
# 4. 이미지 생성 및 Fallback 이미지 처리
# ====================================================
def create_fallback_image(img_path, category_text):
    width, height = 500, 300
    img = Image.new("RGB", (width, height), color=(15, 23, 42))
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
    image_url = f"[https://image.pollinations.ai/prompt/](https://image.pollinations.ai/prompt/){encoded_prompt}?width=1000&height=600&seed={seed}&nologo=true"
    
    try:
        req = urllib.request.Request(
            image_url, 
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        
        with urllib.request.urlopen(req, timeout=40) as response, open(temp_download_path, "wb") as out_file:
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
        print(f"[경고] 이미지 생성 실패({e}). 대체 이미지로 전환합니다.")
        if os.path.exists(temp_download_path):
            os.remove(temp_download_path)
            
        create_fallback_image(img_path, category)
        return False

# ====================================================
# 5. 기술 포스팅 생성 (API 및 고품질 자체 Fallback 엔진)
# ====================================================
def generate_fallback_article(category, safe_title, first_tag):
    """API 호출이 완전히 불가능한 비상 상황에서도 100% 정상 발행을 보장하는 구조화된 문서 생성기"""
    return f"""---
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

## 개요
{category}는 현대 대규모 분산 시스템 및 엔지니어링 아키텍처에서 시스템의 안정성, 확장성 및 운영 효율을 극대화하기 위한 핵심 기술 패러다임이다. 고도화된 클라우드 네이티브 환경에서 발생하는 복잡도를 제어하고 레이턴시를 최소화하기 위한 실무 접근법을 분석한다.

<!--more-->

## 시스템 아키텍처 및 데이터 흐름

{TICK}mermaid
flowchart TD
    Client[Client Ingress] --> Gateway[API Gateway / Envoy]
    Gateway --> ServiceA[Core Processing Service]
    ServiceA --> Cache[(Distributed Cache / Redis)]
    ServiceA --> Broker[Event Broker / Kafka]
    Broker --> Worker[Async Worker Cluster]
    Worker --> Storage[(Data Lakehouse / S3)]
    Storage --> Monitor[Observability & Governance]
{TICK}

## 기술 핵심 원리 및 아키텍처 패턴

1. **상태 비저장성(Stateless)과 분산 동기화**:
   분산 인프라 전반에서 세션 종속성을 분리하고 일관된 상태 전이를 보장하기 위해 분산 락 및 낙관적 동시성 제어(OCC)를 적용한다.
2. **비동기 이벤트 스트리밍 파이프라인**:
   서비스 간 결합도를 낮추고 배압(Backpressure)을 효율적으로 핸들링하기 위해 메시지 큐 기반의 비동기 버퍼링을 구성한다.
3. **무정지 관측성 및 장애 격리(Fault Tolerance)**:
   서킷 브레이커와 분산 추적(OpenTelemetry)을 결합하여 개별 마이크로서비스 장애가 전체 시스템으로 전파되는 계단식 장애(Cascading Failure)를 차단한다.

## 실무 구현 예제

아래는 프로덕션 환경에서 확장 가능한 비동기 이벤트 프로세서 및 복원력 있는 클라이언트 구조를 구현한 Python 예시이다.

{TICK}python
import asyncio
import logging
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ArchitectureEngine")

class ResilientEventProcessor:
    def __init__(self, max_concurrency: int = 5):
        self.semaphore = asyncio.Semaphore(max_concurrency)

    async def execute_task(self, event_id: str, payload: Dict[str, Any]) -> bool:
        async with self.semaphore:
            try:
                logger.info(f"Processing event: {{event_id}}")
                await asyncio.sleep(0.05)
                return True
            except Exception as e:
                logger.error(f"Error handling event {{event_id}}: {{e}}")
                return False

async def main_pipeline():
    processor = ResilientEventProcessor(max_concurrency=3)
    tasks = [
        processor.execute_task(f"evt_{{i}}", {{"data": f"payload_{{i}}"}} )
        for i in range(5)
    ]
    results = await asyncio.gather(*tasks)
    logger.info(f"Pipeline completed. Total tasks: {{sum(results)}}")

if __name__ == "__main__":
    asyncio.run(main_pipeline())
{TICK}

## 적용 시 고려사항 및 장단점

- **장점**:
  - 높은 수평 확장성(Scalability) 및 리소스 활용률 최적화
  - 결합도 감소로 인한 컴포넌트 배포 및 롤백 유연성 확보
  - 격리된 서브시스템 구조를 통한 고가용성 유지
- **고려사항**:
  - 분산 트랜잭션 관리(Saga 패턴 등)로 인한 설계 및 디버깅 복잡도 증가
  - 실시간 분산 추적 및 메트릭 수집 인프라 운영 비용 수반
"""

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
2. 시스템 아키텍처 / 데이터 흐름을 설명하는 Mermaid 다이어그램 작성 ({TICK}mermaid 코드 블록 사용).
3. 기술 개요 및 핵심 원리 설명.
4. 실무에서 검증된 코드 구현체(Python 등)와 가이드 작성.
5. 적용 시 장단점 및 고려사항 명시.
"""

    user_prompt = f"오늘 날짜: {date_dash}\n주제: {category}\n해당 분야의 핵심 기술을 선정하여 실무 중심의 기술 문서를 작성하라."

    content = query_github_models_via_curl(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        model="gpt-4o",
        temperature=0.3,
        max_tokens=3500
    )

    if not content or len(content.strip()) < 150 or "---" not in content:
        print("⚠️ API 호출 결과가 유효하지 않아 내장 고품질 기술 아티클로 자동 전환합니다.")
        content = generate_fallback_article(category, safe_title, first_tag)

    return content

def clean_markdown_output(text):
    text = text.strip()
    if text.startswith(f"{TICK}markdown"):
        text = text[11:].lstrip()
    elif text.startswith(TICK):
        text = text[3:].lstrip()
    
    if text.endswith(TICK):
        text = text[:-3].rstrip()
        
    return text.strip()

def convert_mermaid_to_image_tag(text):
    def replace_match(match):
        mermaid_code = match.group(1).strip()
        encoded_bytes = base64.b64encode(mermaid_code.encode("utf-8"))
        base64_str = encoded_bytes.decode("utf-8")
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
    
    filename = os.path.join(posts_dir, f"{date_dash}-{date_compact}.md")
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(final_content)
        
    print(f"✅ 포스팅 생성 완벽 종료 ({len(final_content)}자 저장됨): {filename}")

if __name__ == "__main__":
    main()
