


# React学習ノート


## ⭐作業環境

<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [React学習ノート](#react学習ノート)
  - [⭐作業環境](#作業環境)
  - [⭐用語の整理](#用語の整理)
    - [Store](#store)
    - [Action](#action)
    - [dispathcer](#dispathcer)
    - [Reducer](#reducer)
  - [⭐コンポーネント](#コンポーネント)
    - [クラスコンポーネント](#クラスコンポーネント)
    - [関数コンポーネント](#関数コンポーネント)
    - [コンポーネントのレンダリング](#コンポーネントのレンダリング)
    - [stateとpropsを用いたライフサイクル](#stateとpropsを用いたライフサイクル)
  - [⭐React hooks](#react-hooks)
    - [ルール](#ルール)
    - [メリット](#メリット)
    - [hooksの種類](#hooksの種類)
    - [カスタムフック](#カスタムフック)
  - [⭐React Router](#react-router)
  - [⭐Context API](#context-api)
    - [API](#api)
  - [⭐Material-UI](#material-ui)
  - [⭐インストールした](#インストールした)
  - [⭐TIPS](#tips)

<!-- /code_chunk_output -->

yarn含めすべてグローバルインストール

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
  - 初期Reactアプリのテンプレを構築する。プロキシ下のみ`--user-npm`が必要
- `npm install @material-ui/core`
  - [material-ui](https://material-ui.com/ja/)のインストール
- `npm start`
  - [localhost:3000](localhost:3000)にアクセスすることでReactアプリ起動

## ⭐用語の整理

### Store

Storeの役割

- stateの管理
  - コンポーネントごとのstateはprops, stateにてコンポーネントが管理するため、グローバルなstateを管理することが多い。そのため、Contextと組み合わせて使われる。
- reducerの適用
  - reducerが適用されることで、stateの状態が変更される。

### Action

Actionの役割

- Storeに対して変更したい内容を伝える指示書

```ts
// action

// 指示書が格納されたオブジェクト
const action = {
    type : 'ADD_COUNT'
}
```

### dispathcer

dispatcherの役割

- ActionをStoreに届ける

```ts
// dispatcher

// @param action 変更内容
    dispatch : function (action) {
        // reducer を使って、state を変更する.
        this.state = this.reducer(this.state, action)
    }
```

### Reducer

Reducerの役割

- 元々は、２つの値を取り１つの値を返す関数という意味
- Actionの内容を判断し、Stateを変更する

```ts
// reducer.

// @param state 現在のステート
// @param action 変更内容
function myReducer(state, action) {

    // actionのタイプごとに、処理を分ける
    switch (action.type) {

        // ADD_COUNTの場合は、countを1増やす.
        case 'ADD_COUNT':
            state = {
                ...state,
                count : state.count + 1
            }
            return state

        default:
            return state
    }
}
```

## ⭐コンポーネント

Reactは定義されたコンポーネントを用いて画面描画を行う。コンポーネントの定義方法は以下の2パターンあり、Reactから見た際には等価である。

### クラスコンポーネント

`React.Component`を継承することでReactにコンポーネントとして認識させる。

```ts
import React from 'react';

class SampleClass extends React.Component {
  render() {
    // JSX
    return <h1>Hello, {props.name}</h1>;
  }
}
```

### 関数コンポーネント

`props`を引数として受け取り、Reactの要素を返却する。

```ts
function SampleFunc(props) {
  // JSX
    return <h1>Hello, {props.name}</h1>;
}
```

### コンポーネントのレンダリング

通常は以下のように一般的なHTMLタグにてReact要素を構築する。

```ts
const element = <div />;
```

以下のような記載を行うことで、コンポーネントから返却されるReact要素を用いてDOMが構築される。

```ts
const funcComponentElement = <SampleFunc />;
const classComponentElement = <SampleClass />;
```

なおコンポーネントがDOMに初回レンダリングされることをマウント`mounting`と呼び、コンポーネントがDOMから削除されることをアンマウント`unmounting`と呼ぶ。

### stateとpropsを用いたライフサイクル

コンポーネント内部で保持する変数には2種類存在し、各変数に複数の値を保持することで、コンポーネントのライフサイクルを管理する。

- state
  - そのコンポーネント内部で保持する状態、変数
  - mutable
  - プライベートである
- props
  - 親コンポーネントから渡されたプロパティ
  - immutable

## ⭐React hooks

React 16.8にて追加された機能。関数コンポーネント内にhookを記載することで、クラスを書かなくてもstate等のReact機能を扱うことが可能となった。言い換えると、「関数コンポーネントがstate, props操作を簡単に行えるようにする機能」とも言える。

### ルール

- 上記で述べている通り、React関数コンポーネント内でのみコール可能
- 例外として、自作カスタムフック内ではコール可能
- 関数内トップレベルでのみコール可能。ネストや条件分岐の中ではコール不可能

### メリット

- クラスを書かなくてもコンポーネントのstate操作を簡単に行える
- コンポーネント間で処理の共有が容易
  - これまでは[高階コンポーネントの作成](https://ja.reactjs.org/docs/higher-order-components.html)や、[レンダープロップ](https://ja.reactjs.org/docs/render-props.html)（propsへの関数渡し）にて共通化していた

### hooksの種類

- useState(初期値)
  - `const [state, setState] = useState(initialState);`
  - その名の通り、stateを関数から簡単に操作可能とするためのhook
  - ステートフルな値と、それを更新するための関数を返す
  - コンポーネント内でstateの変更を可能とする
  - setStateを呼び出さない場合は、initialStateとstateの値は等しくなる
- useEffect(関数, ?依存変数配列)
  - 関数を引数とし、そのコンポーネントのレンダー後に動作する操作を定義するhook。副作用とも呼ぶ
  - これまでは最初にDOMへレンダリングされた際に呼ばれる`componentDidMount`メソッド及び、その後DOM上でコンポーネントがUpdateされる際に呼ばれる`componentDidUpdate`メソッドを用いて同様の処理を実装していた
  - 第二引数に依存変数配列を任意で渡すことで、その変数が変更された場合のみ副作用を生じさせる
  - コンポーネントがアンマウントされた場合に、そのコンポーネントに登録されていたイベントを削除する（クリーンアップ）ための`componentWillUnmount`については、クリーンアップ関数をreturnすることで代用する
- useContext
  - Reactコンポーネントツリーに対して、グローバルとみなすデータについて利用する
  - 引数をpropsバケツリレーしなくても、Contextに収容されているデータにアクセス可能
- userReducer
  - `(state, action) => newState` という型のリデューサ (reducer) を受け取り、現在の state を dispatch メソッドとペアにして返す
  - 下位コンポーネントにdispatcherを渡すことが可能となる
  - 複数の値にまたがるような複雑なstateを扱う場合に有用
  - 前のstateの変更に伴って次のstateを決める場合に有用

### カスタムフック
メリットで述べた、`コンポーネント間で処理の共有が容易`については、[カスタムフック](https://ja.reactjs.org/docs/hooks-custom.html)を利用する。

- カスタムフックはReact hooksの機能ではなく、「hooksを用いてコンポーネント間で処理を共通化する関数」である
- 機能ではないので慣習が必要で、頭に`use`が付いた関数についてはカスタムフックとみなす

## ⭐React Router
[React Router](https://github.com/ReactTraining/react-router/tree/master/packages/react-router-dom)は、SPAにURLを簡単に与えることができるReactのライブラリ。通常SPAではDOM操作を行ったとしても、URLが変わらず1つのページとしてしか認識できない。つまり、ブラウザバックやURL指定してページ遷移ができない。そういった問題を解消するために、コンポーネントとURLのマッピングを行うのがReact Router。

一番簡単なルーティングの記載は以下の通り。

- Appコンポーネントが一番最初に表示される前提
- `/`へアクセスすると、LoginとTestへのリンク先が表示される
- `Login`をクリックすることで、Loginコンポーネントが呼び出される。かつ`/login`へ遷移する。
- `Test`をクリックすることで、Testコンポーネントが呼び出される。かつ`/test`へ遷移する。

```ts
const App: React.FC = (): JSX.Element => {
  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li>
              <Link to='/login'>Login</Link>
            </li>
            <li>
              <Link to='/test'>Test</Link>
            </li>
          </ul>
        </nav>

        <Switch>
          <Route path='/login'>
            <Login />
          </Route>
          <Route path='/test'>
            <Counter />
          </Route>
        </Switch>
      </div>
    </Router>
  );
}
```

## ⭐Context API
Reactが用意している、グローバルなStateを扱うためのAPI群。（参照：[Context API](https://ja.reactjs.org/docs/context.html#contextprovider)）

```ts
const ThemeContext = React.createContext('light');

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
  - コンテクストオブジェクトを作成する。コンポーネントがContextを読む際には、一番近い上位層からProviderされたコンテキストを購読する。
- Context.Provider
  - すべてのコンテキストにはProviderが付属しており、配下のコンポーネントにContextを提供可能。
- Context.displayName
  - 開発ツールにて表示される、コンテキストの名称（description）を付与することができる。
- Context.Consumer
  - コンテクストの変更を購読する。関数コンポーネント内でコンテクストを今度くすることができる。



## ⭐Material-UI



## ⭐インストールした

- `$ npm i --save-dev @types/react-router-dom`
- `$ npm i --save-dev @types/react-dom`
- `$ npm i --save-dev typescript @types/react @types/node`
- `$ npm i --save-dev @material-ui/core`

## ⭐TIPS

Node.jsの管理はnodistに任せる。以下リポジトリよりインストール。

- [nodist](https://github.com/nullivex/nodist/releases)

- インストールできるバージョンの確認
  - `$ nodist dist`
- バージョンを指定してインストール
  - `$ nodist + X.X.X`
- インストール済みのnodeのバージョンの指定
  - `$ nodist X.X.X`
- 正しいnodeがインストールできているかの確認
  - `$ node -v`

npmについても、バージョンを指定してインストールを行う。nodeとnpmのバージョンがずれていると実行できないため、[Node.js release](https://nodejs.org/ja/download/releases/)を参照して、利用するNodeと一致するnpmに変更する。

- 現在のバージョンを確認
  - `$ nodist npm`
- 利用するnpmバージョンの指定
  - `$ nodist npm Y.Y.Y`
  
storybookのインストール

- `$ npx -p @storybook/cli sb init`

既にインストールされている場合は、storybookの依存ライブラリをリセットする

- `$ npx sb init -f`
