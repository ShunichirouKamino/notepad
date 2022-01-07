# React 学習ノート

## ⭐ 作業環境

<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [React 学習ノート](#react学習ノート)
  - [⭐ 作業環境](#作業環境)
  - [⭐ 用語の整理](#用語の整理)
    - [Store](#store)
    - [Action](#action)
    - [dispathcer](#dispathcer)
    - [Reducer](#reducer)
  - [⭐ コンポーネント](#コンポーネント)
    - [クラスコンポーネント](#クラスコンポーネント)
    - [関数コンポーネント](#関数コンポーネント)
    - [コンポーネントのレンダリング](#コンポーネントのレンダリング)
    - [state と props を用いたライフサイクル](#stateとpropsを用いたライフサイクル)
  - [⭐React hooks](#react-hooks)
    - [ルール](#ルール)
    - [メリット](#メリット)
    - [hooks の種類](#hooksの種類)
    - [カスタムフック](#カスタムフック)
  - [⭐React Router](#react-router)
  - [⭐Context API](#context-api)
    - [API](#api)
  - [⭐Material-UI](#material-ui)
  - [⭐ インストールした](#インストールした)
  - [⭐TIPS](#tips)

<!-- /code_chunk_output -->

yarn 含めすべてグローバルインストール

```console
PS D:\workspace\my-hooks> npm -v
6.14.10v
PS D:\workspace\my-hooks> node -v
v14.15.3
PS D:\workspace\my-hooks> yarn -v
1.22.5
```

以降の手順

- `npx create-react-app my-hooks --user-npm`
  - 初期 React アプリのテンプレを構築する。プロキシ下のみ`--user-npm`が必要
- `npm install @material-ui/core`
  - [material-ui](https://material-ui.com/ja/)のインストール
- `npm start`
  - [localhost:3000](localhost:3000)にアクセスすることで React アプリ起動

## ⭐ 用語の整理

### Store

Store の役割

- state の管理
  - コンポーネントごとの state は props, state にてコンポーネントが管理するため、グローバルな state を管理することが多い。そのため、Context と組み合わせて使われる。
- reducer の適用
  - reducer が適用されることで、state の状態が変更される。

### Action

Action の役割

- Store に対して変更したい内容を伝える指示書

```ts
// action

// 指示書が格納されたオブジェクト
const action = {
  type: "ADD_COUNT",
};
```

### dispathcer

dispatcher の役割

- Action を Store に届ける

```ts
// dispatcher

// @param action 変更内容
    dispatch : function (action) {
        // reducer を使って、state を変更する.
        this.state = this.reducer(this.state, action)
    }
```

### Reducer

Reducer の役割

- 元々は、２つの値を取り１つの値を返す関数という意味
- Action の内容を判断し、State を変更する

```ts
// reducer.

// @param state 現在のステート
// @param action 変更内容
function myReducer(state, action) {
  // actionのタイプごとに、処理を分ける
  switch (action.type) {
    // ADD_COUNTの場合は、countを1増やす.
    case "ADD_COUNT":
      state = {
        ...state,
        count: state.count + 1,
      };
      return state;

    default:
      return state;
  }
}
```

## ⭐ コンポーネント

React は定義されたコンポーネントを用いて画面描画を行う。コンポーネントの定義方法は以下の 2 パターンあり、React から見た際には等価である。

### クラスコンポーネント

`React.Component`を継承することで React にコンポーネントとして認識させる。

```ts
import React from "react";

class SampleClass extends React.Component {
  render() {
    // JSX
    return <h1>Hello, {props.name}</h1>;
  }
}
```

### 関数コンポーネント

`props`を引数として受け取り、React の要素を返却する。

```ts
function SampleFunc(props) {
  // JSX
  return <h1>Hello, {props.name}</h1>;
}
```

### コンポーネントのレンダリング

通常は以下のように一般的な HTML タグにて React 要素を構築する。

```ts
const element = <div />;
```

以下のような記載を行うことで、コンポーネントから返却される React 要素を用いて DOM が構築される。

```ts
const funcComponentElement = <SampleFunc />;
const classComponentElement = <SampleClass />;
```

なおコンポーネントが DOM に初回レンダリングされることをマウント`mounting`と呼び、コンポーネントが DOM から削除されることをアンマウント`unmounting`と呼ぶ。

### state と props を用いたライフサイクル

コンポーネント内部で保持する変数には 2 種類存在し、各変数に複数の値を保持することで、コンポーネントのライフサイクルを管理する。

- state
  - そのコンポーネント内部で保持する状態、変数
  - mutable
  - プライベートである
- props
  - 親コンポーネントから渡されたプロパティ
  - immutable

## ⭐React hooks

React 16.8 にて追加された機能。関数コンポーネント内に hook を記載することで、クラスを書かなくても state 等の React 機能を扱うことが可能となった。言い換えると、「関数コンポーネントが state, props 操作を簡単に行えるようにする機能」とも言える。

### ルール

- 上記で述べている通り、React 関数コンポーネント内でのみコール可能
- 例外として、自作カスタムフック内ではコール可能
- 関数内トップレベルでのみコール可能。ネストや条件分岐の中ではコール不可能

### メリット

- クラスを書かなくてもコンポーネントの state 操作を簡単に行える
- コンポーネント間で処理の共有が容易
  - これまでは[高階コンポーネントの作成](https://ja.reactjs.org/docs/higher-order-components.html)や、[レンダープロップ](https://ja.reactjs.org/docs/render-props.html)（props への関数渡し）にて共通化していた

### hooks の種類

- useState(初期値)
  - `const [state, setState] = useState(initialState);`
  - その名の通り、state を関数から簡単に操作可能とするための hook
  - ステートフルな値と、それを更新するための関数を返す
  - コンポーネント内で state の変更を可能とする
  - setState を呼び出さない場合は、initialState と state の値は等しくなる
- useEffect(関数, ?依存変数配列)
  - 関数を引数とし、そのコンポーネントのレンダー後に動作する操作を定義する hook。副作用とも呼ぶ
  - これまでは最初に DOM へレンダリングされた際に呼ばれる`componentDidMount`メソッド及び、その後 DOM 上でコンポーネントが Update される際に呼ばれる`componentDidUpdate`メソッドを用いて同様の処理を実装していた
  - 第二引数に依存変数配列を任意で渡すことで、その変数が変更された場合のみ副作用を生じさせる
  - コンポーネントがアンマウントされた場合に、そのコンポーネントに登録されていたイベントを削除する（クリーンアップ）ための`componentWillUnmount`については、クリーンアップ関数を return することで代用する
- useContext
  - React コンポーネントツリーに対して、グローバルとみなすデータについて利用する
  - 引数を props バケツリレーしなくても、Context に収容されているデータにアクセス可能
- userReducer
  - `(state, action) => newState` という型のリデューサ (reducer) を受け取り、現在の state を dispatch メソッドとペアにして返す
  - 下位コンポーネントに dispatcher を渡すことが可能となる
  - 複数の値にまたがるような複雑な state を扱う場合に有用
  - 前の state の変更に伴って次の state を決める場合に有用

### カスタムフック

メリットで述べた、`コンポーネント間で処理の共有が容易`については、[カスタムフック](https://ja.reactjs.org/docs/hooks-custom.html)を利用する。

- カスタムフックは React hooks の機能ではなく、「hooks を用いてコンポーネント間で処理を共通化する関数」である
- 機能ではないので慣習が必要で、頭に`use`が付いた関数についてはカスタムフックとみなす

## ⭐React Router

[React Router](https://github.com/ReactTraining/react-router/tree/master/packages/react-router-dom)は、SPA に URL を簡単に与えることができる React のライブラリ。通常 SPA では DOM 操作を行ったとしても、URL が変わらず 1 つのページとしてしか認識できない。つまり、ブラウザバックや URL 指定してページ遷移ができない。そういった問題を解消するために、コンポーネントと URL のマッピングを行うのが React Router。

一番簡単なルーティングの記載は以下の通り。

- App コンポーネントが一番最初に表示される前提
- `/`へアクセスすると、Login と Test へのリンク先が表示される
- `Login`をクリックすることで、Login コンポーネントが呼び出される。かつ`/login`へ遷移する。
- `Test`をクリックすることで、Test コンポーネントが呼び出される。かつ`/test`へ遷移する。

```ts
const App: React.FC = (): JSX.Element => {
  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li>
              <Link to="/login">Login</Link>
            </li>
            <li>
              <Link to="/test">Test</Link>
            </li>
          </ul>
        </nav>

        <Switch>
          <Route path="/login">
            <Login />
          </Route>
          <Route path="/test">
            <Counter />
          </Route>
        </Switch>
      </div>
    </Router>
  );
};
```

## ⭐Context API

React が用意している、グローバルな State を扱うための API 群。（参照：[Context API](https://ja.reactjs.org/docs/context.html#contextprovider)）

```ts
const ThemeContext = React.createContext("light");

// Providerにより、Propsとして渡さなくてもContextが配下のコンポーネントに連携される
class App extends React.Component {
  render() {
    return (
      <ThemeContext.Provider value="dark">
        <Toolbar />
      </ThemeContext.Provider>
    );
  }
}

// 明示的にPropsのリレーをしなくてもContextが配下のコンポーネントに連携される
function Toolbar() {
  return (
    <div>
      <ThemedButton />
    </div>
  );
}

// 現在のテーマのコンテクストを読むために、contextType に指定します。
// React は上位の最も近いテーマプロバイダを見つけ、その値を使用します。
// この例では、現在のテーマは "dark" です。
class ThemedButton extends React.Component {
  static contextType = ThemeContext;
  render() {
    return <Button theme={this.context} />;
  }
}
```

store

### API

- React.createContext
  - コンテクストオブジェクトを作成する。コンポーネントが Context を読む際には、一番近い上位層から Provider されたコンテキストを購読する。
- Context.Provider
  - すべてのコンテキストには Provider が付属しており、配下のコンポーネントに Context を提供可能。
- Context.displayName
  - 開発ツールにて表示される、コンテキストの名称（description）を付与することができる。
- Context.Consumer
  - コンテクストの変更を購読する。関数コンポーネント内でコンテクストを今度くすることができる。

## ⭐Material-UI

## ⭐ インストールした

- `$ npm i --save-dev @types/react-router-dom`
- `$ npm i --save-dev @types/react-dom`
- `$ npm i --save-dev typescript @types/react @types/node`
- `$ npm i --save-dev @material-ui/core`

## ⭐TIPS

Node.js の管理は nodist に任せる。以下リポジトリよりインストール。

- [nodist](https://github.com/nullivex/nodist/releases)

- インストールできるバージョンの確認
  - `$ nodist dist`
- バージョンを指定してインストール
  - `$ nodist + X.X.X`
- インストール済みの node のバージョンの指定
  - `$ nodist X.X.X`
- 正しい node がインストールできているかの確認
  - `$ node -v`

npm についても、バージョンを指定してインストールを行う。node と npm のバージョンがずれていると実行できないため、[Node.js release](https://nodejs.org/ja/download/releases/)を参照して、利用する Node と一致する npm に変更する。

- 現在のバージョンを確認
  - `$ nodist npm`
- 利用する npm バージョンの指定
  - `$ nodist npm Y.Y.Y`

storybook のインストール

- `$ npx -p @storybook/cli sb init`

既にインストールされている場合は、storybook の依存ライブラリをリセットする

- `$ npx sb init -f`
