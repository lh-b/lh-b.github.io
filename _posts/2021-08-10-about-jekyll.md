---
title: "Jekyll에 대하여"
tags:
  - jekyll
  - 지킬
header:
  image: assets/images/3/0.png
  caption: "Photo credit by **Jekyll**"
toc: true
excerpt_separator: <!--more-->
---
---
## Jekyll이란?

Jekyll은 동적 객체 지향 스크립트 언어인 루비(*Ruby*) 기반으로 개발된 하나의 라이브러리 즉 루비젬(*RubyGem*)이다.
루비는 인터프리터(*Interpreter*) 언어의 특성에 따라 C 또는 C++과 같은 컴파일러 언어에 비해 실행 속도가 느리지만 매번 html 태그를 작성하지 않고 콘텐츠에 초점을 맞춘 Markdown 언어로 작성하여 보다 쉽게 정적 웹사이트를 생성하는 편리한 도구이다.

Markdown 언어에 대한 내용은 [여기](../about-markdown)에서 확인할 수 있다.

## 파일/디렉토리 구조

Jekyll의 일반적인 파일 및 디렉토리 구조와 각 항목에 대한 설명은 다음과 같이 구성된다.

```
┌─_config.yml
├─_data
│  └─navigation.yml
├─_drafts
│  ├─begin-with-the-crazy-ideas.md
│  └─on-simplicity-in-technology.md
├─_includes
│  ├─footer.html
│  └─head.html
├─_layouts
│  ├─default.html
│  └─posts.html
├─_posts
│  ├─2021-08-06-start.md
│  └─2021-08-07-build.md
├─_sass
│  ├─_base.scss
│  └─_page.scss
└─index.html # index.md도 사용 가능
```

{% raw %}
파일/디렉토리|설명
---|---
`_config.yml`|파일로 환경 구성 정보를 담는다. 정적 웹사이트 생성 시 환경 구성에 활용되며, `title`, `url` 등 요소를 `{{ site.title }}`와 같이 Liquid 태그를 이용하여 접근할 수 있다.
`_drafts`|디렉토리로 아직 게시하지 않은 초안 포스트를 담는다. 초안 포스트에 파일명은 포스트와 다르게 날짜 형식을 따르지 않는다.
`_includes`|디렉토리로 재사용하기 위한 파일을 담는다. 파일 사용시 `{% include 파일명 %}`와 같이 Liquid 태그를 이용하여 접근할 수 있다.
`_layouts`|디렉토리로 콘텐츠를 포장하는 템플릿을 담는다. 각 콘텐츠마다 YAML 형식의 머리말을 기준으로 레이아웃을 선택한다. 기본 규칙으로 `default.html` 템플릿을 호출한다. `{{ content }}`와 같이 Liquid 태그를 이용하여 접근할 수 있다.
`_posts`|디렉토리로 동적 콘텐츠를 담는다. 포스트에 파일명은 `YEAR-MONTH-DAY-title.MARKUP`와 같이 날짜 형식으로 생성한다.
`_data`|디렉토리로 사이트에서 사용할 데이터를 담는다. 디렉토리 내 `.yml`, `.yaml`, `.json`, `.csv`, `.tsv` 형식의 모든 데이터 파일을 자동으로 로드하고 `site.data` 변수로 접근할 수 있다. 디렉토리에 `navigation.yml`라는 파일이 있을 경우 `site.data.navigation`라고 입력하여 해당 콘텐츠를 사용한다.
`_sass`|디렉토리로 스타일시트 조각을 담는다. 정적 웹사이트 생성 시 sass 조각들이 모여 스타일을 정의하는 하나의 `main.css` 파일로 가공된다.
`index.html` 또는 `index.md`|웹사이트에 접속 시 가장 먼저 접근하는 파일이다.
{% endraw %}

## 환경 구성

Jekyll은 정적 웹사이트 생성 과정에서 루트 디렉토리의 `_config.yml` 또는 `_config.toml` 파일에 정의된 요소를 로드하여 웹사이트 환경을 구성한다.
아래 목록의 정의된 요소는 기본값으로 파일 내용에 정의되어 있지 않은 경우 기본값을 사용한다.

```yml
# Where things are
source              : .
destination         : ./_site
collections_dir     : .
plugins_dir         : _plugins # takes an array of strings and loads plugins in that order
layouts_dir         : _layouts
data_dir            : _data
includes_dir        : _includes
sass:
  sass_dir: _sass
collections:
  posts:
    output          : true

# Handling Reading
safe                : false
include             : [".htaccess"]
exclude             : ["Gemfile", "Gemfile.lock", "node_modules", "vendor/bundle/", "vendor/cache/", "vendor/gems/", "vendor/ruby/"]
keep_files          : [".git", ".svn"]
encoding            : "utf-8"
markdown_ext        : "markdown,mkdown,mkdn,mkd,md"
strict_front_matter : false

# Filtering Content
show_drafts         : null
limit_posts         : 0
future              : false
unpublished         : false

# Plugins
whitelist           : []
plugins             : []

# Conversion
markdown            : kramdown
highlighter         : rouge
lsi                 : false
excerpt_separator   : "\n\n"
incremental         : false

# Serving
detach              : false
port                : 4000
host                : 127.0.0.1
baseurl             : "" # does not include hostname
show_dir_listing    : false

# Outputting
permalink           : date
paginate_path       : /page:num
timezone            : null

quiet               : false
verbose             : false
defaults            : []

liquid:
  error_mode        : warn
  strict_filters    : false
  strict_variables  : false

# Markdown Processors
kramdown:
  auto_ids          : true
  entity_output     : as_char
  toc_levels        : [1, 2, 3, 4, 5, 6]
  smart_quotes      : lsquo,rsquo,ldquo,rdquo
  input             : GFM
  hard_wrap         : false
  footnote_nr       : 1
  show_warnings     : false
```

{% raw %}
요소/설명|옵션
---|---
**Site Source**<br>Jekyll이 읽어들일 파일의 경로를 변경한다.|`source: DIR`
**Site Destination**<br>Jekyll이 생성할 파일의 경로를 변경한다.|`destination: DIR`
**Safe**<br>whitelist에 없는 플러그인을 비활성화하고 디스크에 캐싱하며, 심볼릭 링크를 무시한다.|`safe: BOOL`
**Exclude**<br>특정 디렉토리나 파일을 제외하는 목록이다. Site Source를 기준으로 한 상대경로이다.|`exclude: [DIR,FILE,...]`
**Include**<br>특정 디렉토리나 파일을 포함하는 목록이다. Site Source를 기준으로 한 상대경로이다.|`include: [DIR,FILE,...]`
**Keep Files**<br>사이트 생성 전 Site Destination을 초기화할 때, 보관할 파일 목록이다. Jekyll에서 생성되는 않은 파일에 유용하다.|`keep_files: [DIR,FILE,...]`
**Time Zone**<br>사이트 생성 시간대를 설정한다. 사용 가능한 목록은 [여기](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones){:target="_blank"}에서 찾을 수 있다.|`timezone: TIMEZONE`
**Encoding**<br>파일의 인코딩을 지정한다. 사용 가능한 목록은 <abbr title="ASCII-8BIT UTF-8 US-ASCII UTF-16BE UTF-16LE UTF-32BE UTF-32LE UTF-16 UTF-32 UTF8-MAC EUC-JP Windows-31J Big5 Big5-HKSCS Big5-UAO CESU-8 CP949 Emacs-Mule EUC-KR EUC-TW GB18030 GBK ISO-8859-1 ISO-8859-2 ISO-8859-3 ISO-8859-4 ISO-8859-5 ISO-8859-6 ISO-8859-7 ISO-8859-8 ISO-8859-9 ISO-8859-10 ISO-8859-11 ISO-8859-13 ISO-8859-14 ISO-8859-15 ISO-8859-16 KOI8-R KOI8-U Shift_JIS Windows-1250 Windows-1251 Windows-1252 Windows-1253 Windows-1254 Windows-1257 IBM437 IBM720 IBM737 IBM775 CP850 IBM852 CP852 IBM855 CP855 IBM857 IBM860 IBM861 IBM862 IBM863 IBM864 IBM865 IBM866 IBM869 Windows-1258 GB1988 macCentEuro macCroatian macCyrillic macGreek macIceland macRoman macRomania macThai macTurkish macUkraine CP950 CP951 IBM037 stateless-ISO-2022-JP eucJP-ms CP51932 EUC-JIS-2004 GB2312 GB12345 ISO-2022-JP ISO-2022-JP-2 CP50220 CP50221 Windows-1256 Windows-1255 TIS-620 Windows-874 MacJapanese UTF-7 UTF8-DoCoMo SJIS-DoCoMo UTF8-KDDI SJIS-KDDI ISO-2022-JP-KDDI stateless-ISO-2022-JP-KDDI UTF8-SoftBank SJIS-SoftBank">여기</abbr>에서 찾을 수 있다.|`encoding: ENCODING`
**Plugins**<br>플러그인 경로를 변경한다.|`plugins_dir: [DIR1,...]`
**Layouts**<br>레이아웃 경로를 변경한다.|`layouts_dir: DIR`
**Drafts**<br>초안 콘텐츠를 표현한다.|`show_drafts: BOOL`
**Future**<br>현재 시간 이후의 콘텐츠를 게시한다.|`future: BOOL`
**Unpublished**<br>미개시로 지정된 콘텐츠를 처리한다.|`unpublished: BOOL`
**LSI**<br>관련 콘텐츠에 대한 색인을 생성한다. classifier-reborn 플러그인이 필요하다.|`lsi: BOOL`
**Limit Posts**<br>구문 분석 및 게시할 콘텐츠 수를 제한한다.|`limit_posts: NUM`
**Incremental Build**<br>실험 기능인 증분 빌드를 활성화한다. 증분 빌드는 변경된 파일만 다시 빌드하여 대규모 사이트인 경우 성능이 크게 향상되지만 경우에 따라 사이트 생성이 중단될 수 있다.|`incremental: BOOL`
**Strict Front Matter**<br>페이지의 머리말에 YAML 문법 오류가 있으면 빌드를 중단한다.|`strict_front_matter: BOOL`
**Base URL**<br>지정된 URL로 웹사이트를 제공한다.|`baseurl: URL`
**Limit Posts**<br>구문 분석 및 게시할 콘텐츠 수를 제한한다.|`limit_posts: NUM`
**Local Server Port**<br>지정된 포트에서 수신한다.|`port: PORT`
**Local Server Hostname**<br>주어진 호스트 이름에서 수신한다.|`host: HOSTNAME`
**Detach**<br>터미널에서 서버를 분리한다.|`detach: BOOL`
**Show Directory Listing**<br>색인 파일을 로드하는 대신 디렉토리 목록을 표시한다.|`show_dir_listing: BOOL`
{% endraw %}

## 페이지

페이지는 콘텐츠를 구성하는 가장 기본적인 요소이다.
단독 콘텐츠(*날짜별로 구성되거나, 스태프 맴버 또는 레시피와 같이 그룹이 아닌 콘텐츠*)를 구성하는데 유용하다.

페이지를 추가하는 방법은 루트 디렉토리 내 원하는 경로와 파일명으로 `.html` 또는 `.md` 파일을 생성한다.

```
┌─page1.md      # -> http://example.com/page1.html
├─pets          # folder containing pages
│  └─cat.html   # -> http://example.com/pets/cat.html
├─cooks         # folder containing pages
│  ├─ramen.md   # -> http://example.com/cooks/ramen.html
│  └─curry.md   # -> http://example.com/cooks/curry.html
└─page2.html    # -> http://example.com/page2.html
```

또한 특정 폴더에서 출력 URL을 제어할 수 있는 Permalinks를 활용하면 지정된 경로로 접근한다.
`page1.md` 머리말에 permalink를 추가하면

```md
---
permalink: /test1/test2/test3/page1/
---
```

다음과 같이 `page1.md`의 URL이 변경됨을 확인할 수 있다.

```
page1.md      # -> http://example.com/test1/test2/test3/page1.html
```

## 포스트

#### 파일명

포스트는 핵심 콘텐츠로서 날짜 형식의 파일명(`YEAR-MONTH-DAY-title.MARKUP`)으로 작성한다.
또한 `_posts` 디렉토리 내 생성한다.
파일명을 예로 들면 다음과 같다.

```
2021-04-01-my-first-content.md
2021-08-10-hello-world.md
```

#### 머리말

모든 포스트 파일은 일반적으로 레이아웃이나 다른 메타 데이터를 설정할 수 있는 머리말로 시작되어야 한다.
간단한 예로 다음과 같이 작성한다.

```md
---
layout: post
title: "Hello World!"
---

# Welcome

**Hello world**, this is my second blog post.

I hope you like it!
```

머리말에 사용 가능한 요소는 다음과 같다.

요소명|설명
---|---
`layout`|사용할 레이아웃 파일을 지정한다. `_layouts` 디렉토리에 있는 파일을 확장자를 제외한 파일명으로 입력한다. `null` 또는 레이아웃을 입력하지 않을 경우 default 레이아웃을 사용하여 파일을 처리한다. `none`을 사용하는 경우 레이아웃을 사용하지 않고 파일을 처리한다.
`permalink`|콘텐츠에 접근하는 URL을 지정한다. 입력하지 않은 경우 디렉토리 구조를 따른다.
`published`|특정 포스트가 나타나지 않게 하려면 `false`로 설정한다.
`date`|콘텐츠에 날짜를 입력한다. 파일명에 날짜보다 우선순위가 높다. 포스트를 올바르게 정렬하기 위해 사용할 수 있는 기능이다. 날짜 형식은 `YYYY-MM-DD HH:MM:SS +/-TTTT`이며 시간, 분, 초, 시간대 오프셋은 선택 사항이다.
`tags`|하나 이상의 태그를 지정한다. 태그별 범주를 구성할 수 있다.
`category` 또는 `categories`|카테고리별 디렉토리에 콘텐츠를 배치하는 대신 하나 이상의 카테고리를 지정한다. 카테고리별 범주를 구성할 수 있다.

#### 포스트 색인 생성

Liquid와 html 태그를 이용하여 별도의 페이지에 포스트 색인을 생성할 수 있다.
다음은 블로그 포스트 색인을 출력하는 예시이다.

{% raw %}
```html
<ul>
  {% for post in site.posts %}
    <li>
      <a href="{{ post.url }}">{{ post.title }}</a>
    </li>
  {% endfor %}
</ul>
```
{% endraw %}

#### 태그 및 카테고리

Liquid와 html 태그를 이용하여 별도의 페이지에 태그 및 카테고리 색인을 생성할 수 있다.
다음은 태그 및 카테고리별 블로그 포스트 색인을 출력하는 예시이다.

##### 태그 색인 생성

{% raw %}
```html
{% for tag in site.tags %}
  <h3>{{ tag[0] }}</h3>
  <ul>
    {% for post in tag[1] %}
      <li><a href="{{ post.url }}">{{ post.title }}</a></li>
    {% endfor %}
  </ul>
{% endfor %}
```
{% endraw %}

##### 카테고리 색인 생성

{% raw %}
```html
{% for category in site.categories %}
  <h3>{{ category[0] }}</h3>
  <ul>
    {% for post in category[1] %}
      <li><a href="{{ post.url }}">{{ post.title }}</a></li>
    {% endfor %}
  </ul>
{% endfor %}
```
{% endraw %}

#### 포스트 발췌

기본적인 스니펫은 `_config.yml`에 설정된 `"\n\n"`이지만 머리말에 `excerpt_separator` 변수를 사용하여 콘텐츠의 단락을 변경할 수 있다.

```md
---
excerpt_separator: <!--more-->
---

Excerpt with multiple paragraphs

Here's another paragraph in the excerpt.
<!--more-->
Out-of-excerpt
```

다음은 발췌와 함께 블로그 포스트 색인을 출력하는 예시이다.

{% raw %}
```html
<ul>
  {% for post in site.posts %}
    <li>
      <a href="{{ post.url }}">{{ post.title }}</a>
      {{ post.excerpt }}
    </li>
  {% endfor %}
</ul>
```
{% endraw %}

#### 초안

초안이란 파일명에 날짜가 없는 포스트이다. 현재 작성중으로 아직은 게시하고 싶지 않은 포스트를 의미한다. 초안 기능을 사용하려면 `_drafts` 디렉토리 내 포스트를 작성한다.<!--more-->