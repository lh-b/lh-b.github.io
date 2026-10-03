import os
import re
import json
import random
import time
import socket
import ssl
import urllib.request
import urllib.parse
import urllib.error
import base64
from datetime import datetime, timezone, timedelta
from PIL import Image, ImageDraw

# ====================================================
# 0. DoH 기반 DNS 자동 해석 (Errno -2 및 SSL 불일치 원천 해결)
# ====================================================
TARGET_HOST = "models.inference.ai.azure.com"

def resolve_azure_models_ip():
    """
    러너 환경의 로컬 DNS CNAME 버그를 우회하기 위해
    Cloudflare/Google DoH 엔드포인트를 IP로 직접 호출하여 A 레코드를 획득합니다.
    """
    # 1. 기본 시스템 DNS 시도
    try:
        infos = socket.getaddrinfo(TARGET_HOST, 443, socket.AF_INET, socket.SOCK_STREAM)
        if infos:
            ip = infos[0][4][0]
            print(f"🌐 [시스템 DNS 확인 성공] {TARGET_HOST} -> {ip}")
            return ip
    except Exception:
        pass

    # 2. DoH IP 직접 질의 (SSL 인증서 검증 비활성화하여 IP 직접 접속 통과)
    doh_endpoints = [
        ("https://1.1.1.1/dns-query?name=" + TARGET_HOST, {"Accept": "application/dns-json"}),
        ("https://8.8.8.8/resolve?name=" + TARGET_HOST + "&type=A", {"Accept": "application/json"}),
    ]

    insecure_ctx = ssl.create_default_context()
    insecure_ctx.check_hostname = False
    insecure_ctx.verify_mode = ssl.CERT_NONE

    for url, headers in doh_endpoints:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=4, context=insecure_ctx) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                answers = data.get("Answer", [])
                for ans in answers:
                    if ans.get("type") == 1:  # IPv4 A Record
                        ip = ans["data"]
                        print(f"🌐 [DoH 해석 성공] {TARGET_HOST} -> {ip}")
                        return ip
                for ans in reversed(answers):
                    val = ans.get("data", "")
                    if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", val):
                        print(f"🌐 [DoH 체인 해석 성공] {TARGET_HOST} -> {val}")
                        return val
        except Exception as e:
            print(f"⚠️ DoH 조회 건너뜀 ({url[:18]}...): {e}")

    return None

resolved_ip = resolve_azure_models_ip()

if resolved_ip:
    orig_getaddrinfo = socket.getaddrinfo
    def patched_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
        if host == TARGET_HOST:
            p = int(port) if port else 443
            return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (resolved_ip, p))]
        return orig_getaddrinfo(host, port, family, type, proto, flags)
    socket.getaddrinfo = patched_getaddrinfo
    print(f"🚀 [소켓 매핑 활성화] {TARGET_HOST} -> {resolved_ip}")

# ====================================================
# 1. 한국 시간대(KST = UTC+9) 및 날짜 포맷 설정
# ====================================================
KST = timezone(timedelta(hours=9))
now = datetime.now(KST)
date_dash = now.strftime("%Y-%m-%d")    # YYYY-MM-DD
date_compact = now.strftime("%Y%m%d")   # YYYYMMDD
date_full = now.strftime("%Y-%m-%d %H:%M:%S +0900")

# ====================================================
# 2. 토큰 및 REST API 통신 로직
# ====================================================
token = os.environ.get("GH_MODELS_TOKEN")
if not token:
    raise ValueError("GH_MODELS_TOKEN 환경 변수가 설정되지 않았습니다.")

def query_github_models(messages, model="gpt-4o", temperature=0.7, max_tokens=2500, max_retries=3):
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
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
        "User-Agent": "GitHubAction-PostGenerator/1.0"
    }

    for attempt in range(1, max_retries + 1):
        try:
            req = urllib.request.Request(url, data=json_bytes, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=90) as resp:
                raw_body = resp.read().decode("utf-8")
                
                if not raw_body or raw_body.strip().upper() == "OK":
                    raise ValueError(f"비정상 게이트웨이 응답: '{raw_body[:50]}'")

                parsed = json.loads(raw_body)
                if "choices" in parsed and len(parsed["choices"]) > 0:
                    content = parsed["choices"][0].get("message", {}).get("content", "")
                    if content and len(content.strip()) > 10 and content.strip().upper() != "OK":
                        return content.strip()
                raise ValueError("응답 내 본문 content 데이터 누락")

        except urllib.error.HTTPError as http_err:
            err_msg = http_err.read().decode("utf-8", errors="ignore")
            print(f"[시도 {attempt}/{max_retries}] HTTP 오류 {http_err.code}: {err_msg[:120]}")
        except Exception as e:
            print(f"[시도 {attempt}/{max_retries}] API 연결 실패: {e}")

        if attempt < max_retries:
            time.sleep(attempt * 3)

    return None

# ====================================================
# 3. 최신 IT 주제 동적 선정
# ====================================================
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

def get_latest_tech_topic():
    system_prompt = """
너는 글로벌 IT 기술 트렌드 분석가이자 최고 기술 책임자(CTO)이다.
현재 최신 IT/소프트웨어 엔지니어링 분야에서 가장 중요한 실무 아키텍처 및 트렌드 주제 1개를 선정하라.

[선정 조건]
1. 실제 코드 및 기술 아키텍처로 구현 가능한 구체적인 엔지니어링 주제일 것.
2. 영문 제목으로 명확하고 간결하게 출력할 것 (예: "Agentic Multi-Agent Workflows with LangGraph", "eBPF-driven Zero Trust Network Security").
3. 따옴표, 설명, 번호 등의 부연 설명 없이 오직 '주제명 텍스트'만 단 한 줄로 출력할 것.
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
        if topic_raw:
            topic = topic_raw.strip().strip('"').strip("'")
            if len(topic) > 3 and topic.upper() != "OK":
                print(f"✨ 동적 생성된 최신 IT 주제: {topic}")
                return topic
    except Exception as e:
        print(f"⚠️ 주제 질의 중 예외 발생: {e}")

    selected = random.choice(fallback_categories)
    print(f"📋 예비 카테고리에서 선택된 주제: {selected}")
    return selected

# ====================================================
# 4. 이미지 생성 및 대체 이미지 처리
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

        print(f"✅ AI 이미지 생성 및 저장 완료: {img_path}")
        return True

    except Exception as e:
        print(f"[경고] 이미지 생성 중 오류 발생: {e}")
        if os.path.exists(temp_download_path):
            os.remove(temp_download_path)
            
        create_fallback_image(img_path, category)
        return False

# ====================================================
# 5. 기술 포스팅 생성 (API 및 Fail-Safe 내장 엔진)
# ====================================================
def generate_fallback_article(category):
    safe_title = json.dumps(category, ensure_ascii=False)
    first_tag = re.sub(r'[^a-zA-Z0-9]', '', category.split()[0])
    
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

최신 엔지니어링 패러다임에서 **{category}**는 분산 환경의 확장성과 운영 안정성을 동시에 달성하기 위한 핵심 설계 아키텍처이다. 인프라의 복잡도가 증가함에 따라 단일 장애점(SPOF)을 제거하고 비동기 데이터 처리 효율을 극대화하는 패턴이 필수적으로 요구됨.
<!--more-->

## 1. 시스템 아키텍처 개요

다음 다이어그램은 {category}의 코어 데이터 파이프라인과 트래픽 라우팅 구조를 도식화한 엔지니어링 아키텍처이다.

```mermaid
graph TD
    Client[Ingestion Client / Edge] --> Gateway[API Gateway / Ingress Router]
    Gateway --> Dispatcher[Distributed Event Dispatcher]
    Dispatcher --> WorkerA[Core Processing Worker 1]
    Dispatcher --> WorkerB[Core Processing Worker 2]
    WorkerA --> Cache[(In-Memory Distributed Cache)]
    WorkerB --> Cache
    WorkerA --> Storage[(Persistent Lakehouse / Partitioned DB)]
    WorkerB --> Storage
    WorkerA -.-> Observability[OpenTelemetry & Prometheus Engine]
    WorkerB -.-> Observability
