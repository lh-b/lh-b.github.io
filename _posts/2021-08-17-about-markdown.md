---
title: "Markdown에 대하여"
tags:
  - markdown language
header:
  image: assets/images/4/0.jpg
  caption: "Credit by **John Gruber**"
  teaser: assets/images/4/0_.jpg
toc: true
toc_sticky: true
excerpt_separator: <!--more-->
---
---
## Markdown

마크다운(*Markdown*)은 일반 텍스트 기반의 경량 마크업(*Markup*) 언어다.
일반 텍스트로 서식이 있는 문서를 작성하는데 사용되며, 일반 마크업 언어에 비해 문법이 쉽고 간단한 것이 특징이다.
HTML과 리치 텍스트(*RTF*) 등 서식 문서로 쉽게 변환되기 때문에 온라인 콘텐츠 등에서 `.md` 또는 `.markdown` 확장자로 사용한다.

**Tips**  
온라인 마크다운 편집기 사이트를 방문하려면 [여기](https://pandao.github.io/editor.md/en.html){:target="_blank"}를 클릭한다.
{: .notice--success}

Jekyll에서 지원하는 Markdown 문법의 요소는 다음과 같다.

### 제목

Markdown|HTML|출력
---|---|---
# Heading level 1<br><small style="display:inline-block;width: 95%;text-align:center;">또는</small><br>Heading level 1<br>===|<h1>Heading level 1</h1>|<span style="font-weight:bold;font-size:2.0em;">Heading level 1</span>
## Heading level 2<br><small style="display:inline-block;width: 95%;text-align:center;">또는</small><br>Heading level 2<br>---|<h2>Heading level 2</h2>|<span style="font-weight:bold; font-size: 1.7em;">Heading level 2</span>
### Heading level 3|<h3>Heading level 3</h3>|<span style="font-weight:bold;font-size:1.5em;">Heading level 3</span>
#### Heading level 4|<h4>Heading level 4</h4>|<span style="font-weight:bold;font-size:1.42em;">Heading level 4</span>
##### Heading level 5|<h5>Heading level 5</h5>|<span style="font-weight:bold;font-size:1.36em;">Heading level 5</span>
###### Heading level 6|<h6>Heading level 6</h6>|<span style="font-weight:bold;font-size:1.3em;">Heading level 6</span>

### 수평선

한줄에 3개 이상의 \*\*\*, \-\-\-, \_\_\_를 사용하여 수평선을 그린다.

```
***

---

___
```

---

### 단락

빈 줄을 추가하거나 <p></p> 태그를 이용하여 단락을 구분한다.

Markdown|HTML
---|---
I really like using Markdown.<br><br>I think I'll use it to format all of my documents from now on.|<p>I really like using Markdown.</p><p>I think I'll use it to format all of my documents from now on.</p>

```
I really like using Markdown.

I think I'll use it to format all of my documents from now on.
```

### 줄 바꿈

두 개 이상의 띄어쓰기와 엔터(*enter*)를 입력하거나 \<br\> 태그를 이용하여 줄을 바꾼다.

Markdown|HTML
---|---
This is the first line.&nbsp;&nbsp;<br>And this is the second line.|This is the first line.\<br\>And this is the second line.

```
This is the first line.  
And this is the second line.
```

### 강조

텍스트 스타일을 굵게 또는 기울임꼴로 변경한다.

Markdown|HTML|출력
---|---|---
I love \*it\*.<br><small style="display:inline-block;width: 95%;text-align:center;">또는</small><br>I love \_it\_.|I love \<em\>it\</em\>.|I love *it*.
I love \*\*it\*\*.<br><small style="display:inline-block;width: 95%;text-align:center;">또는</small><br>I love \_\_it\_\_.|I love \<strong\>it\</strong\>.|I love **it**.
I love \*\*\*it\*\*\*.<br><small style="display:inline-block;width: 95%;text-align:center;">또는</small><br>I love \_\_\_it\_\_\_.|I love \<strong\>\<em\>it\</em\>\</strong\>.|I love ***it***.

### 취소선

단어 가운데에 수평선을 넣어 취소선을 표현하려면 \~\~를 단어의 앞 뒤에 사용한다.

```
~~The world is flat.~~ We now know that the world is round.
```

~~The world is flat.~~ We now know that the world is round.

### 인용구

문장 앞에 >를 입력하여 인용구를 만든다.
인용 부호는 중첩하여 사용할 수 있으며 다른 Markdown 요소와 동시에 사용이 가능하다.

```
> #### The quarterly results look great!
>
> - Revenue was off the chart.
> - Profits were higher than ever.
>
> *Everything* is going according to **plan**.
>> But we should not forget about prudence.
```

> *** The quarterly results look great!***
>
> - Revenue was off the chart.
> - Profits were higher than ever.
>
> *Everything* is going according to **plan**.
>> But we should not forget about prudence.

### 목록

순서가 지정된 목록을 만드는 방법은 문장 앞에 숫자와 마침표를 입력한다.
숫자는 1부터 입력해야 하며 다음 입력하는 숫자가 무엇이든 순서대로 목록이 지정된다.
순서가 지정되지 않은 목록을 만드는 방법은 문장 앞에 \-, \*, \+ 기호를 입력한다.

Markdown|HTML|출력
---|---|---
1. First item<br>2. Second item<br>3. Third item<br>4. Fourth item|<ol><br><li>First item</li><br><li>Second item</li><br><li>Third item</li><br><li>Fourth item</li><br></ol>|1. First item<br>2. Second item<br>3. Third item<br>4. Fourth item
1. First item<br>1. Second item<br>1. Third item<br>1. Fourth item|<ol><br><li>First item</li><br><li>Second item</li><br><li>Third item</li><br><li>Fourth item</li><br></ol>|1. First item<br>2. Second item<br>3. Third item<br>4. Fourth item
1. First item<br>8. Second item<br>3. Third item<br>5. Fourth item|<ol><br><li>First item</li><br><li>Second item</li><br><li>Third item</li><br><li>Fourth item</li><br></ol>|1. First item<br>2. Second item<br>3. Third item<br>4. Fourth item
- First item<br>- Second item<br>- Third item<br>- Fourth item|<ol><br><li>First item</li><br><li>Second item</li><br><li>Third item</li><br><li>Fourth item</li><br></ol>|· First item<br>· Second item<br>· Third item<br>· Fourth item
* First item<br>* Second item<br>* Third item<br>* Fourth item|<ol><br><li>First item</li><br><li>Second item</li><br><li>Third item</li><br><li>Fourth item</li><br></ol>|· First item<br>· Second item<br>· Third item<br>· Fourth item
+ First item<br>+ Second item<br>+ Third item<br>+ Fourth item|<ol><br><li>First item</li><br><li>Second item</li><br><li>Third item</li><br><li>Fourth item</li><br></ol>|· First item<br>· Second item<br>· Third item<br>· Fourth item

### 블록

블록의 모든 행을 최소 4개의 띄어쓰기 또는 하나의 탭만큼 들여쓰거나 <pre></pre> 태그를 이용하여 코드 블록을 생성한다.

```
    <
        Code Block
    >
```

```
<pre>
public class OutputFunction
{
  public static void main(String[] args)
  {
     System.out.println("Hello, World!");
  }
}
</pre>
```

<pre>
public class OutputFunction
{
  public static void main(String[] args)
  {
     System.out.println("Hello, World!");
  }
}
</pre>

또다른 방법으로 단락의 앞과 뒤에 \`\`\` 또는 \~\~\~ 줄을 추가하여 코드 블록을 생성한다.
시작점에 사용하는 언어를 선언하여 구문 강조(*Syntax Highlighting*)가 가능하다.

~~~
```java
public class OutputFunction
{
  public static void main(String[] args)
  {
     System.out.println("Hello, World!");
  }
}
```
~~~

```java
public class OutputFunction
{
  public static void main(String[] args)
  {
     System.out.println("Hello, World!");
  }
}
```

~~~
```json
{
  "firstName": "John",
  "lastName": "Smith",
  "age": 25
}
```
~~~

```json
{
  "firstName": "John",
  "lastName": "Smith",
  "age": 25
}
```

### 코드

단어나 구를 \`로 감싸 코드로 표현한다.

Markdown|HTML|출력
---|---|---
At the command prompt, type \`nano\`.|At the command prompt, type \<code\>nano\</code\>.|At the command prompt, type `nano`.

### 링크

링크 텍스트를 []로 묶고 바로 뒤에 URL을 ()로 묶는다.

```
My favorite search engine is [Google](https://google.com).
```

My favorite search engine is [Google](https://google.com).

### 툴팁

URL 뒤에 툴팁 정보를 ""로 감싸 넣는다.
마우스를 링크 위로 가져가면 툴팁 정보가 나타난다.

```
My favorite search engine is [Google](https://google.com "The best search engine for privacy").
```

My favorite search engine is [Google](https://google.com "The best search engine for privacy").

### URL 및 Email 링크

URL이나 이메일 주소를 <>로 감싼다.

```
<https://google.com>
<no-reply@google.com>
```
<https://google.com>  
<no-reply@google.com>

### 이미지

먼저 !와 이미지 텍스트를 []로 묶고 바로 뒤에 URL을 ()로 묶는다.
추가로 툴팁 정보를 나타내려면 URL 뒤에 툴팁 정보를 ""로 감싸 넣는다.
또다른 방법으로 \<img/\> 또는 \<image/\> 태그를 이용하여 크기 조절이 가능한 이미지를 추가한다.

```html
![Photo Caption #1](/assets/images/4/1.jpg "Ocean Sunrise Dawn Peninsula France Landscape")

<img width="50%" src="/assets/images/4/1.jpg" alt="Photo Caption #2" title="Ocean Sunrise Dawn Peninsula France Landscape" />
```

![Photo Caption #1](/assets/images/4/1.jpg "Ocean Sunrise Dawn Peninsula France Landscape")

<img width="50%" src="/assets/images/4/1.jpg" alt="Photo Caption #2" title="Ocean Sunrise Dawn Peninsula France Landscape" />

### 동영상

\<video\>\</video\> 태그나 \<iframe\>\</iframe\> 태그를 이용하여 크기 조절이 가능한 동영상을 추가한다.
Liquid 태그가 지원되는 경우 `youtube`, `vimeo`, `google-drive`, `bilibili`에서 제공하는 동영상인 경우 아이디를 입력하여 동영상을 추가한다.

{% raw %}
```html
<video width="500" height="375" controls>
    <source src="/assets/images/4/2.mp4" type="video/mp4">
    Your browser does not support the video tag.
</video>

<iframe width="956" height="538" src="https://www.youtube.com/embed/HUBNt18RFbo" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

{% include video id="HUBNt18RFbo" provider="youtube" %}
```
{% endraw %}

<video width="500" height="375" controls>
    <source src="/assets/images/4/2.mp4" type="video/mp4">
    Your browser does not support the video tag.
</video>

{% include video id="HUBNt18RFbo" provider="youtube" %}

### 이스케이프 문자

텍스트 서식을 지정하는데 사용되는 리터럴 문자를 표시하려면 문자 앞에 \를 추가한다.
이스케이프 문자가 적용되는 리터럴 문자 목록은 다음과 같다.

문자|이름
---|---
\\ |백슬래시
\` |백틱
\* |별표
\_ |밑줄
\{\}|중괄호
\[\]|대괄호
\<\>|꺽쇠 괄호
\(\)|괄호
\# |파운드 기호
\+ |더하기 기호
\- |빼기 기호
\. |점
\! |느낌표
\| |파이프

```
\* Without the backslash, this would be a bullet in an unordered list.
```

\* Without the backslash, this would be a bullet in an unordered list.

### 테이블

표를 추가하려면 \-\-\-을 사용하여 각 열의 헤더를 만들고 \|를 사용하여 각 열을 구분한다.
행의 양쪽 끝에 |를 추가하여 호환성을 향상시킨다.
추가로 각 열의 헤더에 왼쪽, 가운데, 오른쪽으로 :를 사용하여 텍스트 정렬을 지정한다.

```
| Syntax      | Description | Test Text     |
| :---------- | :---------: | ------------: |
| Header      | Title       | Here's this   |
| Paragraph   | Text        | And more      |
```

| Syntax      | Description | Test Text     |
| :---------- | :---------: | ------------: |
| Header      | Title       | Here's this   |
| Paragraph   | Text        | And more      |

### 작업 목록

작업 목록을 사용하여 확인란이 있는 항목 목록을 만든다.
작업 목록 항목 앞에 \-와 \[ \]를 공백으로 추가하고 빈 공백에 x를 입력하여 선택 항목을 지정한다.

```
- [x] Write the press release
- [ ] Update the website
- [ ] Contact the media
```

- [x] Write the press release
- [ ] Update the website
- [ ] Contact the media

### 각주

각주를 사용하면 문서 본문을 복잡하게 만들지 않고 참조를 추가할 수 있다.
각주를 생성할 때 각주 참조를 추가한 위치에 링크가 있는 위 첨자 번호가 나타나고 링크를 통해 페이지 하단의 각주 내용으로 이동이 가능하다.
각주 사용의 대표적인 예로 [위키백과](https://ko.wikipedia.org/wiki/%EB%A7%88%ED%81%AC%EB%8B%A4%EC%9A%B4)가 있다.

```
Here's a simple footnote,[^1] and here's a longer one.[^bignote]

[^1]: This is the first footnote.

[^bignote]: Here's one with multiple paragraphs and code.

    Indent paragraphs to include them in the footnote.

    `{ my code }`

    Add as many paragraphs as you like.
```

Here's a simple footnote,[^1] and here's a longer one.[^bignote]

[^1]: This is the first footnote.

[^bignote]: Here's one with multiple paragraphs and code.

    Indent paragraphs to include them in the footnote.

    `{ my code }`

    Add as many paragraphs as you like.

<!--more-->