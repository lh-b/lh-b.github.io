import os
import re
import json
import urllib.request
from datetime import datetime, timezone, timedelta
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

# 1. 한국 시간대(KST = UTC+9) 설정
KST = timezone(timedelta(hours=9))
now = datetime.now(KST)
date_str = now.strftime("%Y-%m-%d")
date_compact = now.strftime("%Y%m%d")

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

# 4. 프롬프트 정의 및 글 생성
def generate_article():
    trends = get_latest_it_trends()
    
    system_prompt = f"""
너는 IT 기술 블로그를 운영하는 전문 엔지니어 겸 아키텍트이다.
주어진 최신 IT 트렌드를 주제로 깊이 있는 기술 블로그 포스팅을 작성하라.

[Frontmatter 및 작성 규칙]
1. 문서 최상단에 반드시 아래와 같은 포맷의 YAML Frontmatter를 작성할 것:
---
title: "제목 입력"
tags:
  - 태그1
  - 태그2
  - 태그3
header:
  teaser: assets/images/{date_compact}/teaser.png
toc: true
toc_sticky: true
excerpt_separator: <!--more-->
---

2. 본문 작성 규칙:
- 개요(Introduction) 작성 직후 반드시 `<!--more-->` 주석을 넣을 것.
- 가독성을 위해 H4(####), H5(#####) 등 적절한 마크다운 헤더를 활용할 것.
- 단순 뉴스 요약이 아닌, 백엔드/AI 엔지니어 관점의 시사점, 장단점, 실제 적용 방안 등 전문적인 생각을 상세히 서술할 것.
- 이미지를 삽입할 경우 반드시 `/assets/images/{date_compact}/` 경로를 기준으로 작성할 것. (예: ![](/assets/images/{date_compact}/1.png))
- 부드러우면서도 기술적인 전문성을 가진 톤앤매너 유지.
"""

    user_prompt = f"""
오늘 날짜: {date_str}

아래 트렌드 소식을 바탕으로 블로그 포스팅을 작성해줘:
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

# 5. 티저 이미지 생성 및 저장
def generate_teaser_image(article_title):
    try:
        # 이미지 생성을 위한 프롬프트 작성
        image_prompt = f"A high-quality, professional teaser image for a tech blog post titled '{article_title}'. The image should be visually appealing and represent the themes of technology, innovation, and the future. It should be suitable for use as a social media share image or a blog post header."
        
        # GitHub Models API를 통해 이미지 생성 (DALL-E 3 모델 사용)
        image_response = client.complete(
            messages=[
                UserMessage(content=image_prompt),
            ],
            model="dall-e-3",
            max_tokens=1
        )
        
        # 생성된 이미지 URL 가져오기
        image_url = image_response.choices[0].message.content
        
        # 이미지 다운로드 및 저장
        img_dir = f"assets/images/{date_compact}"
        os.makedirs(img_dir, exist_ok=True)
        img_filename = f"{img_dir}/teaser.png"
        urllib.request.urlretrieve(image_url, img_filename)
        
        print(f"✅ 티저 이미지가 성공적으로 생성되었습니다: {img_filename}")
    except Exception as e:
        print(f"[경고] 티저 이미지 생성 중 오류 발생: {e}")

# 6. 응답 정제 및 파일 저장
def clean_markdown_output(text):
    # LLM이 출력물 앞뒤로 ```markdown ... ``` 펜스를 씌우는 경우 제거
    text = re.sub(r"^```markdown\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"^```\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"```$", "", text, flags=re.MULTILINE)
    return text.strip()

def main():
    content = generate_article()
    cleaned_content = clean_markdown_output(content)
    
    # 생성된 글의 제목 가져오기
    title_match = re.search(r"^title:\s*\"(.*)\"", cleaned_content, flags=re.MULTILINE)
    if title_match:
        article_title = title_match.group(1)
    else:
        article_title = "IT Tech Trends"
    
    # 티저 이미지 생성
    generate_teaser_image(article_title)
    
    # 저장 경로 설정 (_posts 디렉토리 준비)
    posts_dir = "_posts"
    os.makedirs(posts_dir, exist_ok=True)
    
    # 영어/숫자 위주의 안전한 파일명 생성 (예: _posts/2026-07-21-it-tech-trends.md)
    filename = os.path.join(posts_dir, f"{date_str}-it-tech-trends.md")
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(cleaned_content)
        
    print(f"✅ 포스팅이 성공적으로 생성되었습니다: {filename}")

if __name__ == "__main__":
    main()
