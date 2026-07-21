import os
import re
import json
import random
import urllib.request
from datetime import datetime, timezone, timedelta
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

# 3. IT 핵심 기술 주제 후보군 무작위 선정
CATEGORIES = [
    "영상처리(Computer Vision & Image Processing)",
    "인공지능 및 딥러닝(Artificial Intelligence & Deep Learning)",
    "데이터 분석 및 처리(Data Analysis & Pipeline Processing)",
    "대규모 언어 모델 및 자연어 처리(LLM & NLP)",
    "분산 데이터 베이스 및 머신러닝 파이프라인(MLOps & Data Engineering)"
]

selected_category = random.choice(CATEGORIES)

# 4. 주제에 맞는 명확한 개념 이미지 생성 및 저장 (티저 이미지 버그 완벽 방지)
def generate_and_save_image(img_dir, category):
    img_path = os.path.join(img_dir, "0_.png")
    
    # 주제별 시각적 이해도를 돕는 프롬프트 설계
    prompt = f"A highly detailed and clear technical diagram representing {category}. Professional tech blog style, modern infographic with clean node graphs, data flows, and neural networks, dark blue background."
    
    try:
        url = "https://models.inference.ai.azure.com/images/generations"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        body = json.dumps({
            "prompt": prompt,
            "model": "dall-e-3",
            "n": 1,
            "size": "1024x1024"
        }).encode("utf-8")

        req = urllib.request.Request(url, data=body, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=40) as resp:
            res_data = json.loads(resp.read().decode())
            image_url = res_data["data"][0]["url"]

        # 이미지 다운로드 및 바이너리 저장
        urllib.request.urlretrieve(image_url, img_path)
        print(f"✅ 유효한 티저 이미지 다운로드 및 저장 성공: {img_path}")
        return True
    except Exception as e:
        print(f"[경고] 이미지 생성 중 오류 발생: {e}")
        # 예외 상황 시 이미지 미출력으로 인한 깨짐 방지용 1x1 픽셀 이미지 대체 생성
        blank_png = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
        with open(img_path, "wb") as f:
            f.write(blank_png)
        return False

# 5. 프롬프트 정의 및 기술 문서 생성
def generate_article(category):
    system_prompt = f"""
너는 영상처리, 인공지능, 데이터 분석 분야의 수석 엔지니어이다.
제시된 IT 핵심 기술 분야 중 하나를 선정하여 전문적인 기술 문서를 작성하라.

[작성 포맷 및 어조 규칙]
1. 존댓말(~해요, ~합니다)을 절대로 사용하지 말 것.
2. 개조식 표현(~함, ~임) 또는 기술 서술용 평어/해라체(~다, ~한다)만 사용할 것.
3. 문서 상단 Frontmatter 규격을 엄격히 준수할 것:
---
title: "[기술명] 핵심 개념 및 검증된 실무 활용법"
tags:
  - IT기술
  - {category.split('(')[0].strip()}
  - 기술분석
header:
  teaser: /assets/images/{date_compact}/0_.png
toc: true
toc_sticky: true
excerpt_separator: <!--more-->
---

[본문 필수 구성 요소]
1. 개요 서술 후 즉시 `<!--more-->` 주석 배치.
2. 기술의 개요 및 핵심 원리 설명.
3. 본문 내 주제를 직관적으로 전달할 수 있는 이미지 매핑 포함: `![](/assets/images/{date_compact}/0_.png)`
4. 검증된 사용 방법 (실제 동작 가능한 Python / PyTorch / OpenCV / Pandas 등의 코드 예제 및 적용 가이드 포함).
5. 실제 실무 적용 시 고려해야 할 장단점 및 한계점 정리.
"""

    user_prompt = f"""
오늘 날짜: {date_dash}
이번 포스팅 주제 분야: {category}

해당 분야의 대표적인 핵심 기술 하나를 직접 선정한 후, 검증된 구현 코드 및 사용법을 포함하여 실무에 즉시 적용 가능한 깊이 있는 글을 작성하라.
"""

    response = client.complete(
        messages=[
            SystemMessage(content=system_prompt),
            UserMessage(content=user_prompt),
        ],
        model="gpt-4o",
        temperature=0.4,
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

    print(f"🎯 선정된 IT 핵심 분야: {selected_category}")

    # 1. 티저 및 본문 이미지 생성 (assets/images/YYYYMMDD/0_.png)
    generate_and_save_image(img_dir, selected_category)

    # 2. 기술 블로그 문서 생성 및 저장 (_posts/YYYY-MM-DD-YYYYMMDD.md)
    content = generate_article(selected_category)
    cleaned_content = clean_markdown_output(content)
    
    filename = os.path.join(posts_dir, f"{date_dash}-{date_compact}.md")
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(cleaned_content)
        
    print(f"✅ 포스팅 생성 완료: {filename}")

if __name__ == "__main__":
    main()
