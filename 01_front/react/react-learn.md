# React学習ノート

## ⭐作業環境

yarn含めすべてグローバルインストール

```console
PS D:\workspace\my-hooks> npm -v
6.14.10
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
  - その名の通り、stateを関数から簡単に操作可能とするためのhook
- useEffect(関数, ?依存変数配列)
  - 関数を引数とし、そのコンポーネントのレンダー後に動作する操作を定義するhook。副作用とも呼ぶ
  - これまでは最初にDOMへレンダリングされた際に呼ばれる`componentDidMount`メソッド及び、その後DOM上でコンポーネントがUpdateされる際に呼ばれる`componentDidUpdate`メソッドを用いて同様の処理を実装していた
  - 第二引数に依存変数配列を任意で渡すことで、その変数が変更された場合のみ副作用を生じさせる
  - コンポーネントがアンマウントされた場合に、そのコンポーネントに登録されていたイベントを削除する（クリーンアップ）ための`componentWillUnmount`については、クリーンアップ関数をreturnすることで代用する
- useContext
  - TODO
- userReducer
  - TODO

### カスタムフック
メリットで述べた、`コンポーネント間で処理の共有が容易`については、[カスタムフック](https://ja.reactjs.org/docs/hooks-custom.html)を利用する。

- カスタムフックはReact hooksの機能ではなく、「hooksを用いてコンポーネント間で処理を共通化する関数」である
- 機能ではないので慣習が必要で、頭に`use`が付いた関数についてはカスタムフックとみなす

## ⭐Context API

Reactアプリケーションでは、propsを介してトップダウンでパラメータを渡される。これは、多くのコンポーネントから必要とされるプロパティにとっては厄介である。そのため、コンテクストという機能が提供される。

- ツリーの各階層ごとに保持するプロパティを、コンポーネントの外から定義できる
- あるReactコンポーネントツリーに対して、グローバルとみなすことができる情報を共有するために利用する

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


## ⭐Material-UI



## ⭐インストールした

- `$ npm i --save-dev @types/react-router-dom`
- `$ npm i --save-dev @types/react-dom`
- `$ npm i --save-dev typescript @types/react @types/node`
- `$ npm i --save-dev @material-ui/core`
