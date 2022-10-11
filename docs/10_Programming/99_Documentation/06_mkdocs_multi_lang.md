---
title: mkdocsで複数言語に対応する
tags:
    - mkdocs
    - python
    - ドキュメント作成
description:
---

基本日本語で書いているドキュメントですが、
USD 関連などはとくに英語のコミュニティがメインになるため
英語でもページを書けるように環境を構築することにしました。

## mkdocs-static-i18n 導入

まず、mkdocs にマルチ言語を入れる場合
すでに static-i18n プラグインというものがあるのでそれを入れることで
複数言語切り替えが可能になります。

```bat
pip install mkdocs-static-i18n
```

まず、pip でプラグインをインストールして mkdocs.yml に追記します。

```yml
- plugins:
      - i18n:
            default_language: ja
            languages:
                ja: Japanese
                en: English
```

注意点として、Git のタイムスタンププラグインなど他プラグインにも関係する処理のため
plugins の先頭に書いておかないとエラーになることがあります。

これで準備は完了です。

![](https://gyazo.com/fa55a3ed9f10d6abe9df7b6a0ae4fc96.png)

あとは、作成する Markdown に .言語名.md というファイルを作ると

![](https://gyazo.com/9942b3b4fd6fe4bbce8a3dd5e9b849b4.png)

ページの検索左にあるボタンで「English」など言語を選ぶことで
言語名の Markdown に内容を表示できます。
他言語名が入らないものについては、default_language 扱いになります。
導入は簡単でした。

ただし、ページ単位で言語切り替えがうまく動かないらしく
トップページに戻ってしまうので、デフォルト言語も .ja.md のように
用意したほうがいいのかもしれません。

## 1 ファイルで編集したい

導入は簡単だったものの、1 つ大きな問題があります。
それは、自分一人で記事を書いている場合などは
可能ならば 1 つのファイルで英語も日本語も同時にかけたほうが嬉しいです。
ので、1 ファイルで書けるように 1 ファイルから個別の言語 Markdown に切り出すような処理を作ってみます。

### 仕様を決める

まず、複数言語を各ファイルは

![](https://gyazo.com/19d49718bb13528770c24fc6fafada03.png)

md ではなく mdlang という拡張子にしておきます。
これは、同じ名前の markdown（デフォルト）と ja ファイルがあった場合は
デフォルトの名無しのほうが使用されるようなので、
編集前の元 Markdown をビルド対象から外すためです。

```yml
---
title: マルチ言語対応サンプル（日本語）
tags:
    - bcde
description: 日本語の説明です
multi_lang:
    en:
        title: EnglishTitleSample
        description: EnglishDescription
        tags:
            - aaa
            - bbb
---
```

そして、タイトルや説明などを書く部分に multi_lang を追加して
その下に指定の言語での表記を書けるようにしておきます。

あとは、メインの記事部分に、どの言語でも表示したいもの（画像やコードなど）と
言語ごとに切り替えたいものを書けるようにします。

```markdown
<!---lang:ja--->

日本語

<!---lang:end--->
```

どうしようか考えた結果、指定言語でのみ表示したい物は
上のようなコメントタグを用意して
そのタグの間にある文章は、指定タグでのみ表示するようにします。

{{'59b31294a847c7c9b8b7f1f66942b9c8'|gist}}

あとはこんな感じで mdlang という拡張子のファイルがあったら
ヘッダー部分をいい感じに処理して、個別の言語 Markdown ファイルを生成します。

```yml
- name: Create LangPages
  run: docker exec mkdocs python scripts/multi_langpage.py
```

このスクリプトを、GithubAction で呼び出してビルド時に Markdown を作成します。

この結果できあがったページが :fa-external-link: [日本語はこちら](https://fereria.github.io/reincarnation_tech/10_Programming/99_Documentation/mult_lang/) :fa-external-link: [英語はこちら](https://fereria.github.io/reincarnation_tech/en/10_Programming/99_Documentation/mult_lang/) です。

これで 1 ファイルに複数言語を記述できる環境ができたので
あとは記事を書くだけではありますが…英語記事を書くほうが大変なので
実際に活用するまではもう少しかかりそうです。
