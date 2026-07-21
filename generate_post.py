import os
import re
import json
import random
import urllib.request
from datetime import datetime, timezone, timedelta
from PIL import Image, ImageDraw, ImageFont
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

# 1. 한국 시간대(KST = UTC+9) 및 날짜 포맷 설정
KST = timezone(timedelta(hours=9))
now = datetime.now(KST)
date_dash = now.strftime("%Y-%m-%d")    # YYYY-MM-DD
date_compact = now.strftime("%Y%m%d")   # YYYYMMDD

# 2. GitHub Models Client 설정
token = os.environ.get("GH_MODELS_TOKEN")
if not token:
    raise ValueError("GH_MODELS_TOKEN 환경 변수가 설정되지 않았습니다.")

client = ChatCompletionsClient(
    endpoint="https://models.inference.ai.azure.com",
    credential=AzureKeyCredential(token),
)

# 3. IT 핵심 기술 주제 후보군
CATEGORIES = [
    "Computer Vision & Image Processing",
    "Deep Learning & Artificial Intelligence",
    "Data Engineering & Analytics Pipeline",
    "Large Language Models & NLP",
    "MLOps & Distributed Systems"
]

selected_category = random.choice(CATEGORIES)

# 4. 예외 발생 시 손상된 이미지 대신 정식 500x300 대체 이미지를 만드는 함수
def create_fallback_image(img_path, category_text):
    width, height = 500, 300
    # 기술 블로그에 어울리는 다크 모드 배경
    img = Image.new('RGB', (width, height), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)
    
    # 테두리 선 추가
    draw.rectangle([5, 5, width - 6, height - 6], outline=(56, 189, 248), width=2)
    
    # 텍스트 그리기 (기본 폰트 사용)
    text = f"Tech Topic:\n{category_text}"
    draw.text((30, 120), text, fill=(241, 245, 249))
    
    img.save(img_path, "PNG")
    print(f"⚠️ API 이미지 생성 실패로 500x300 대체 이미지를 고화질로 생성했습니다: {img_path}")

# 5. 500x300 명확한 기술 개념 이미지 생성 및 저장
def generate_and_save_image(img_dir, category):
    img_path = os.path.join(img_dir, "0_.png")
    temp_download_path = os.path.join(img_dir, "temp_raw.png")
    
    prompt = f"A high quality, clear technical architecture diagram representing {category}. Professional tech blog style, modern infographic with clean node graphs and data flows, dark background."
    
    try:
        url = "https://models.inference.ai.azure.com/images/generations"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        # DALL-E-3 규격에 맞는 표준 해상도로 요청
        body = json.dumps({
            "prompt": prompt,
            "model": "dall-e-3",
            "n": 1,
            "size": "1024x1024"
        }).encode("utf-8")

        # 충분한 작업시간 부여 (timeout 90초)
        req = urllib.request.Request(url, data=body, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=90) as resp:
            res_data = json.loads(resp.read().decode())
            image_url = res_data["data"][0]["url"]

        # 1. 임시 파일로 원본 이미지 다운로드
        urllib.request.urlretrieve(image_url, temp_download_path)

        # 2. Pillow를 이용하여 정확한 500x300 비율로 가공 및 리사이징
        with Image.open(temp_download_path) as img:
            # 비율을 유지하며 중앙 크롭 및 500x300 리사이즈
            target_width, target_height = 500, 300
            
            # 비율 맞춤 계산
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

        # 임시 파일 삭제
        if os.path.exists(temp_download_path):
            os.remove(temp_download_path)

        print(f"✅ 500x300 유효 이미지 생성 및 저장 완료: {img_path}")
        return True

    except Exception as e:
        print(f"[경고] 이미지 생성 중 오류 발생: {e}")
        if os.path.exists(temp_download_path):
            os.remove(temp_download_path)
            
        # 67 Bytes 깨진 파일 대신 500x300 유효 그래픽 이미지 생성
        create_fallback_image(img_path, category)
        return False

# 6. 프롬프트 정의 및 기술 포스팅 생성 (존댓말 제거)
def generate_article(category):
    system_prompt = f"""
너는 IT 분야 수석 엔지니어이다.
주어진 주제에 맞춰 깊이 있는 기술 문서를 작성하라.

[어조 및 스타일 규칙 - 엄격 준수]
1. 존댓말(~해요, ~합니다, ~습니다)을 절대로 사용하지 말 것.
2. 개조식 표현(~함, ~임) 또는 서술용 평어/해라체(~다, ~한다)만 사용할 것.

[Frontmatter 규칙]
---
title: "[기술] {category} 핵심 원리 및 검증된 활용법"
tags:
  - IT기술
  - {category.split()[0]}
  - 엔지니어링
header:
  teaser: /assets/images/{date_compact}/0_.png
toc: true
toc_sticky: true
excerpt_separator: <!--more-->
---

[본문 필수 구조]
1. 개요 서술 후 `<!--more-->` 주석 필수 삽입.
2. 기술 개요 및 핵심 원리 설명.
3. 본문 내 시각 자료 참조 삽입: `![](/assets/images/{date_compact}/0_.png)`
4. 실무에서 검증된 코드 구현체(Python/PyTorch/Pandas 등)와 사용 가이드 작성.
5. 적용 시 장단점 및 고려사항 명시.
"""

    user_prompt = f"""
오늘 날짜: {date_dash}
주제: {category}

해당 분야의 핵심 기술을 선정하여 실무 중심의 기술 문서를 작성하라.
"""

    response = client.complete(
        messages=[
            SystemMessage(content=system_prompt),
            UserMessage(content=user_prompt),
        ],
        model="gpt-4o",
        temperature=0.3,
        max_tokens=3500
    )
    
    return response.choices[0].message.content

def clean_markdown_output(text):
    text = re.sub(r"^```markdown\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"^```\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"```$", "", text, flags=re.MULTILINE)
    return text.strip()

def main():
    posts_dir = "_posts"
    img_dir = f"assets/images/{date_compact}"
    
    os.makedirs(posts_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)

    print(f"🎯 작성 주제: {selected_category}")

    # 1. 500x300 이미지 안전 생성 및 검증
    generate_and_save_image(img_dir, selected_category)

    # 2. 마크다운 포스트 파일 생성 (_posts/YYYY-MM-DD-YYYYMMDD.md)
    content = generate_article(selected_category)
    cleaned_content = clean_markdown_output(content)
    
    filename = os.path.join(posts_dir, f"{date_dash}-{date_compact}.md")
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(cleaned_content)
        
    print(f"✅ 포스팅 생성 완벽 종료: {filename}")

if __name__ == "__main__":
    main()
