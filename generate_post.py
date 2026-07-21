import os
import re
import json
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

# 3. 최신 IT 이슈 수집 (Hacker News API)
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
        print(f"[경고] 트렌드 수집 중 오류 발생 (기본 주제 사용): {e}")
        return "- 최신 인공지능, 딥러닝 기술 트렌드 및 대규모 언어 모델(LLM) 동향"

# 4. 이미지 자동 생성 및 저장 함수 (Teaser Image 생성)
def generate_and_save_image(img_dir):
    img_path = os.path.join(img_dir, "0_.png")
    prompt = "A high-tech digital illustration of deep learning and artificial intelligence, minimalist, modern tech blog teaser style"
    
    try:
        # GitHub Models DALL-E-3 API 호출
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
        with urllib.request.urlopen(req, timeout=30) as resp:
            res_data = json.loads(resp.read().decode())
            image_url = res_data["data"][0]["url"]

        # 생성된 이미지 다운로드 후 파일로 저장
        urllib.request.urlretrieve(image_url, img_path)
        print(f"✅ 이미지 생성 및 저장 완료: {img_path}")
        return True
    except Exception as e:
        print(f"[경고] 이미지 생성 실패: {e}")
        # 이미지 생성이 실패할 경우 디폴트 1x1 투명 PNG 이미지 파일 생성하여 에러 방지
        blank_png = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
        with open(img_path, "wb") as f:
            f.write(blank_png)
        print(f"⚠️ 임시 기본 이미지 대체 생성: {img_path}")
        return False

# 5. 프롬프트 정의 및 글 생성
def generate_article():
    trends = get_latest_it_trends()
    
    system_prompt = f"""
너는 IT 기술 블로그를 운영하는 전문 엔지니어이다.
주어진 IT 트렌드 소식을 바탕으로 깊이 있는 기술 문서를 작성하라.

[어조 및 문체 규칙 - 매우 중요]
- 존댓말(~해요, ~합니다, ~습니다)을 절대로 사용하지 말 것.
- 반드시 개조식 표현(~함, ~임) 또는 기술 서술용 평어/해라체(~다, ~한다)만 사용할 것.
- 예시: "딥러닝은 Deep Neural Network를 통해 학습하는 것을 말함.", "비선형 함수의 적용이 필수적이다."

[Frontmatter 작성 규칙]
문서 최상단에 아래 양식을 정확히 지켜서 출력할 것:
---
title: "최신 IT 트렌드 및 기술 분석"
tags:
  - 인공지능
  - AI 트렌드
  - 소프트웨어 공학
header:
  teaser: assets/images/{date_compact}/0_.png
toc: true
toc_sticky: true
excerpt_separator: <!--more-->
---

[본문 작성 규칙]
1. 개요 요약 작성 후 바로 아래에 `<!--more-->` 삽입할 것.
2. 가독성을 위해 H4(####), H5(#####) 헤더 위주로 목차 구조를 잡을 것.
3. 본문에 이미지를 참조할 경우 `![](/assets/images/{date_compact}/0_.png)` 형식을 적용할 것.
"""

    user_prompt = f"""
오늘 날짜: {date_dash}

아래 트렌드를 참조하여 기술 문서를 작성하라:
{trends}
"""

    response = client.complete(
        messages=[
            SystemMessage(content=system_prompt),
            UserMessage(content=user_prompt),
        ],
        model="gpt-4o",
        temperature=0.5,
        max_tokens=3000
    )
    
    return response.choices[0].message.content

def clean_markdown_output(text):
    text = re.sub(r"^```markdown\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"^```\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"```$", "", text, flags=re.MULTILINE)
    return text.strip()

def main():
    # 저장할 디렉터리 경로 설정
    posts_dir = "_posts"
    img_dir = f"assets/images/{date_compact}"
    
    os.makedirs(posts_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)

    # 1. 이미지 생성 및 저장 (assets/images/YYYYMMDD/0_.png)
    generate_and_save_image(img_dir)

    # 2. 마크다운 글 생성 및 저장 (_posts/YYYY-MM-DD-YYYYMMDD.md)
    content = generate_article()
    cleaned_content = clean_markdown_output(content)
    
    filename = os.path.join(posts_dir, f"{date_dash}-{date_compact}.md")
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(cleaned_content)
        
    print(f"✅ 포스팅 생성 완료: {filename}")

if __name__ == "__main__":
    main()
