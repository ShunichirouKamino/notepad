---
marp: true
page_number: true
theme: default
paginate: true
class: lead
header: header
footer: footter
---

<!-- フォントのimport -->
<style>
@import url('https://fonts.googleapis.com/css?family=Noto+Serif+JP&display=swap');

</style>

<style>
h1 {
    font-size: 70px;
    font-weight: bold;
    color: #008080;
}
section {
    font-family: 'Noto Serif JP', serif;
}
section.agenda, section.text {
    justify-content: start;
}
section.subtitle {
    font-size: 50px;
    color: #008080;
}
</style>

<!-- _class: title -->

# 関数型プログラミングを理解する

---

<!-- _class: agenda -->

## 目次

- 関数型プログラミングとは
- なぜ今関数型プログラミングか？

---

<!-- _class: subtitle -->

## 関数型プログラミングとは

---

<!-- _class: text -->

## 手続き型プログラミング

手続き型プログラミングは、「順に処理を書いていく」プログラミング手法。

- 年齢が格納されたリストから 30 代の人数をカウントする

```java
Integer[] age = {38, 26, 40, 32, 36};
List＜Integer＞ list = Arrays.asList(age);

int count = 0;
for (int i = 0; i ＜ list.size(); i++) {
    int individualAge = list.get(i);
    if (individualAge ＞= 30 ＆＆ individualAge ＜= 39) {
        count++;
    }
System.out.println(count);
```

---

<!-- _class: text -->

## 手続き型プログラミング

手続き型プログラミングのメリット

- コードが追いやすい
  - 上から順に読めばいいだけなので
- 学習難易度が低い

手続き型プログラミングのデメリット

- 再利用がし辛い
- 現実の物体と紐づかない

---

<!-- _class: text -->

## 関数型プログラミング

- 年齢が格納されたリストから 30 代の人数をカウントする

```java
Integer[] age = {38, 26, 40, 32, 36};
List＜Integer＞ list = Arrays.asList(age);

System.out.println(list.stream()
                        .filter(x -＞ x ＞= 30 ＆＆ x ＜= 39)
                        .count());

```

---

<!-- _class: text -->

## 関数型プログラミング

関数型プログラミングのメリット

- 純粋関数化により、副作用を抑えることができる
- コードが追いやすい
  - 人間の思想とリンクした関数名称

関数型プログラミングのデメリット

- 学習難易度は高い

---

<!-- _class: text -->

## 純粋関数

関数型プログラミングのメリット

- 純粋関数化により、副作用を抑えることができる
- コードが追いやすい
  - 人間の思想とリンクした関数名称

関数型プログラミングのデメリット

- 学習難易度は高い

---

<!-- _class: subtitle -->

## なぜ今関数型プログラミングか？

---

```

```
