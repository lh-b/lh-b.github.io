import os
import re
import json
import urllib.request
from datetime import datetime, timezone, timedelta
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from PIL import Image, ImageDraw, ImageFont

# 1. 한국 시간대(KST = UTC+9) 설정
KST = timezone(timedelta(hours=9))
now = datetime.now(KST)
date_dash = now.strftime("%Y-%m-%d")    # 예: 2026-07-21
date_compact = now.strftime("%Y%m%d")   # 예: 20260721

# 2. GitHub Models Client 설정
token = os.environ.get("GH_MODELS_TOKEN")
if not token:
    raise ValueError("GH_MODELS_TOKEN 환경 변수가 설정되지 않았습니다.")

client = ChatCompletionsClient(
    endpoint="https://models.inference.ai.azure.com",
    credential=AzureKeyCredential(token),
)

# 3. 실제 이미지 생성 함수 (teaser.png 및 본문 이미지 생성)
def generate_default_images(img_dir, compact_date):
    os.makedirs(img_dir, exist_ok=True)
    
    # 생성할 이미지 정보 (파일명, 배경색, 텍스트)
    images_to_create = [
        ("teaser.png", (41, 128, 185), f"TECH INSIGHT\n{compact_date}"),
        ("1.png", (52, 73, 94), f"Architecture Diagram\n{compact_date}"),
    ]
    
    for filename, bg_color, text in images_to_create:
        filepath = os.path.join(img_dir, filename)
        if not os.path.exists(filepath):
            # 800x450 크기의 썸네일/다이어그램 기본 이미지 생성
            img = Image.new("RGB", (800, 450), color=bg_color)
            draw = ImageDraw.Draw(img)
            
            # 기본 폰트 설정 및 중앙 텍스트 그리기
            draw.text((400, 225), text, fill=(255, 255, 255), anchor="mm")
            img.save(filepath, "PNG")
            print(f"🖼️ 이미지 생성 완료: {filepath}")

# 4. 최신 IT 이슈 수집 (Hacker News API)
def get_latest_it_trends():
    try:
        url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            top_ids = json.loads(response.read().decode())[:5]
        
        titles = []
        for item_id in top_ids:
            item_url = f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"
            with urllib.request.urlopen(item_url, timeout=5) as resp:
                data = json.loads(resp.read().decode())
                titles.append(f"- {data.get('title')} ({data.get('url', '')})")
        return "\n".join(titles)
    except Exception as e:
        print(f"[경고] 트렌드 수집 실패 (기본 주제 사용): {e}")
        return "- 최신 AI 기술 트렌드 및 대규모 언어 모델(LLM) 동향"

# 5. 프롬프트 작성 및 포스팅 생성
def generate_article():
    trends = get_latest_it_trends()
    
    system_prompt = f"""
너는 IT 전문 기술 블로거임.
주어진 최신 IT 트렌드를 주제로 깊이 있는 기술 포스팅을 작성할 것.

[문체/어조 규칙 - 매우 중요]
- 절대로 존댓말(~합니다, ~해요)을 사용하지 말 것.
- 반드시 '음슴체'(~함, ~임, ~하였음, ~할 필요가 있음, ~로 판단됨)로 작성할 것.

[Frontmatter 및 마크다운 규칙]
1. 최상단 Frontmatter 양식:
---
title: "최신 IT 및 AI 기술 트렌드 분석"
tags:
  - IT트렌드
  - AI
  - 백엔드
header:
  teaser: assets/images/{date_compact}/teaser.png
toc: true
toc_sticky: true
excerpt_separator: <!--more-->
---

2. 본문 작성 규칙:
- 개요 작성 후 반드시 `<!--more-->` 주석 삽입.
- H4(####), H5(#####) 등 헤더를 사용하여 구조화할 것.
- 본문 중간에 생성된 이미지를 참조하도록 `![](/assets/images/{date_compact}/1.png)` 태그를 최소 1개 이상 삽입할 것.
- 단순 요약이 아닌, 백엔드/AI 엔지니어 관점의 시사점 및 기술적 고찰을 음슴체로 명확히 작성할 것.
"""

    user_prompt = f"""
작성 날짜: {date_dash}

다음 트렌드 내용을 바탕으로 포스팅을 작성해줘:
{trends}
"""

    response = client.complete(
        messages=[
            SystemMessage(content=system_prompt),
            UserMessage(content=user_prompt),
        ],
        model="gpt-4o",
        temperature=0.7,
        max_tokens=3000
    )
    
    return response.choices[0].message.content

# 6. 마크다운 후처리
def clean_markdown_output(text):
    text = re.sub(r"^```markdown\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"^```\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"```$", "", text, flags=re.MULTILINE)
    return text.strip()

# 7. 메인 실행
def main():
    # 1) 이미지 경로 설정 및 실제 이미지 자동 생성/업로드 준비
    img_dir = f"assets/images/{date_compact}"
    generate_default_images(img_dir, date_compact)
    
    # 2) 글 생성 및 파일 저장
    content = generate_article()
    cleaned_content = clean_markdown_output(content)
    
    posts_dir = "_posts"
    os.makedirs(posts_dir, exist_ok=True)
    
    # 파일명 형식: 2024-05-28-20240528.md
    filename = os.path.join(posts_dir, f"{date_dash}-{date_compact}.md")
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(cleaned_content)
        
    print(f"✅ 포스팅 생성 완료: {filename}")

if __name__ == "__main__":
    main()
