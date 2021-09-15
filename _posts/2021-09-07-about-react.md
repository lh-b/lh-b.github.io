---
title: "React에 대하여"
tags:
  - React
  - JSX
  - UI
header:
  image: assets/images/5/0.png
  caption: "Credit by **Jordan Walke**"
  teaser: assets/images/5/0_.png
toc: true
toc_sticky: true
excerpt_separator: <!--more-->
---
---
## React

리엑트(*React*)는 자바스크립트(*Javascript*) 라이브러리의 하나로서 사용자 인터페이스[^1](*User Interface:UI*)를 만들기 위해 사용된다.
React의 특징으로 선언형 프로그래밍[^2](*Declarative Programming*)을 제공하여 복잡한 UI를 만들 때 생기는 어려움을 줄여준다.
또한 싱글 페이지 애플리케이션(Single Page Application:SPA)이나 모바일 애플리케이션 개발에 사용된다.
다중 페이지를 개발하고자 할 때는 추가 라이브러리인 *React Router*를 활용하여 사용이 가능하다.
React의 동작 방식은 다음과 같이 효율적으로 데이터 갱신(*Refresh*) 및 컴포넌트 렌더링(*Rendering*)을 수행한다.

1. JSX(*Javascript eXtension*)와 CSS(*Cascading Style Sheets*)로 애플리케이션의 각 상태에 대한 뷰 설계.
2. 가상 DOM(*Virtual Document Object Model:Virtual DOM*)을 업데이트하고 프레임워크에서 이전 Virtual DOM과 현재 Virtual DOM 간의 데이터가 변경되는 부분 검출.
3. 실제 DOM(*Document Object Model*)에서 최종 업데이트.

#### JSX

React는 Javascript와 JSX를 지원한다.
HTML을 Javascript 문법으로 표현이 가능하지만 React에서는 Javascript 확장 문법인 JSX를 권장한다.
아래의 두 코드를 비교하여 JSX의 장점을 확인할 수 있다.

```javascript
// Javascript
class HelloMessage extends React.Component {
  render() {
    return React.createElement(
      "div", null,
      React.createElement("span", null, "Hello"),
      React.createElement("span", null, this.props.name)
    );
  }}

ReactDOM.render(
  React.createElement(HelloMessage, { name: "Guest" }),
  document.getElementById('hello-example')
);
```

```jsx
// JSX
class HelloMessage extends React.Component {
  render() {
    return (
      <div>
        <span>Hello</span>
        <span>{this.props.name}</span>
      </div>
    );
  }}

ReactDOM.render(
  <HelloMessage name="Guest" />,
  document.getElementById('hello-example')
);
```

위 코드의 결과는 동일하게 아래와 같이 출력된다.

```html
HelloGuest
```

JSX 코드를 보면 HTML 문법과 같이 `<div></div>`와 `<span></span>` 태그를 이용하여 구조를 만들고 구조 안에 텍스트나 `{}`로 감싼 변수를 입력한다.
하지만 Javascript 코드는 태그를 이용하기 위해 `React.createElement`를 반복으로 사용하여 한눈에 구조가 보이지 않는다.
Javascript 코드를 HTML 처럼 표현할 수 있기 때문에 용이한 개발이 가능히다.
HTML과 흡사하지만, Javascript 내부에서 사용하기 때문에 다음과 같이 HTML과 다른 차이점이 있다.

- HTML 요소에 `class` 값을 정의할 때, `class`라는 단어가 ECMAScript6의 클래스 문법과 겹치는 예약어이기 때문에 `className`으로 대체한다.
- 마찬가지 이유로 루프문 예약어와 겹치는 `for`는 `htmlFor`로 대체한다.
- 또한 요소에서 이벤트를 핸들링하는 `onclick` 등의 단어들은 `onClick` 처럼 카멜표기법으로 표기한다.
- 기존의 HTML에서 주석은 `<!-- code -->`로 사용하나 `/* code */`로 대체한다.
- HTML Custom-Element는 `<my_element>`와 같이 사용하나 `<MyElement />`와 같이 Pascal Case로 표기한다. 닫는 태그에는 명시적으로 `/>` 표기한다.
- JSX 내부에서도 JS를 사용할 수 있다. `{console.log('ok')}`와 같이 표기한다.

JSX를 빌드할 때 자바스크립트 컴파일러(*Javascript Compiler*)인 바벨(*Babel*)에서 코드 변환 처리를 수행하여 Javascript로 변환된다.

**Tips** 
JSX를 컴파일한 Javascript 코드를 확인하려면 [여기](https://babeljs.io/repl/#?browsers=defaults%2C%20not%20ie%2011%2C%20not%20ie_mob%2011&build=&builtIns=false&corejs=3.6&spec=false&loose=false&code_lz=MYGwhgzhAEASCmIQHsCy8pgOb2vAHgC7wB2AJjAErxjCEB0AwsgLYAOyJph0A3gFDRoAJ1Jl4wgBQBKPoKEj4hAK7CS0SfIXQAPGQCWANwB8W7bohswJYwiTIdAekvXT5hTpc3ehABb6IejZhZDZAkjAWeABfJy83cycDEzNpAG55aOj-fmpaQgARAHlUelFyCU0hHTsUdEwcaAiogF4AIgBxZQxCNuhHYwAaeTJkYGUokgYcQgBREHhJwgAhAE8ASTJJAHJfRBQAWgJItgXt6X50oA&debug=false&forceAllTransforms=false&shippedProposals=false&circleciRepo=&evaluate=false&fileSize=false&timeTravel=false&sourceType=module&lineWrap=true&presets=react&prettier=false&targets=&version=7.15.5&externalPlugins=&assumptions=%7B%7D){:target="_blank"}를 클릭한다.
{: .notice--success}

#### 준비 사항

- ~~NPM(*Node Package Manager*)[^3]~~(Include Node.JS)
- ~~Babel Compiler~~(Include Node.JS)
- [Node.JS](https://nodejs.org/en/){:target="_blank"}
- [Visual Studio Code](https://code.visualstudio.com/download){:target="_blank"}[^4]

#### 설치 및 실행

1. `Node.JS` 와 `VS Code`를 설치한다.
2. `window` + `R` 키를 누르고 `cmd`를 입력하여 명령 프롬프트를 실행한다.

![](/assets/images/5/1.jpg)

3. 원하는 경로에서 `npx create-react-app 폴더명`을 입력한뒤 `Enter` 키를 누른다.

![](/assets/images/5/2.jpg)

4. 다운로드가 완료되면 위와 같이 폴더명 내 React 관련 데이터를 확인할 수 있다.

![](/assets/images/5/3.jpg)

5. `VS Code`를 실행한 뒤 `폴더 열기`를 눌러 입력한 폴더(*ex: react_projects*)를 선택한다.

![](/assets/images/5/4.jpg)

6. `ctrl` + \` 키를 눌러 터미널을 활성화하고 `npm start`를 입력한다.

![](/assets/images/5/5.jpg)

7. 위와 같이 브라우저에 React 로고가 보이면 React를 사용하기 위한 환경 구성이 완료된다.

<!--more-->
#### 참조

[^1]: 사용자 인터페이스: 사용자가 조작하는 애플리케이션의 입력이나 입력에 따른 결과의 출력에 디자인을 적용하여 사용자가 애플리케이션과 상호작용을 위한 영역.
[^2]: 선언형 프로그래밍: 프로그래밍 패러다임(*Programming paradigm*) 중의 하나로 무엇(*What*)을 작업하기 위한 방법을 정의하는 것을 의미. 즉 제어 흐름을 설명하지 않고 계산 논리에 집중하여 동일한 코드를 다른 영역이나 애플리케이션에서 재사용하기 쉬움.
[^3]: NPM: 자바스크립트 프로그래밍 언어를 위한 패키지 관리자.
[^4]: Visual Studio Code: 편리한 React 프로그래밍을 위한 추천 도구.