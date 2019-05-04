path: docs/98_Other
source: mkdocs_setting.md

# mkdocs を設定する

<!-- SUMMARY: mkdocsを設定する -->

テクニカル系の内容をまとめるための記事作成用に  
静的サイト生成ツールの mkdocs を使用してみました。

## インストール

mkdocs は、python で作成されているので  
まず Python をインストールして、pip を使用してインストールをします。

```bat
pip install mkdocs
pip install pip install mkdocs-material
```

インストールのときに、テンプレートも一緒にインストールしておきます。

## リポジトリ作成～コミット

今回は GitHubPages を使用するので、  
まず、GitHub にリポジトリを作成してクローンします。

今回はこちらで作成。
https://github.com/fereria/reincarnation_tech/tree/master

作成されたフォルダの中に、基本の構成を作ります。

1 つめが、 docs フォルダ。  
この中に markdown ファイルを入れていきます。  
次に、mkdocs の設定ファイルである mkdocs.yml を、フォルダ直下に作ります。  
中身は

```yml
site_name: My Docs
```

デフォルトだとサイトの名前のみで設定はとくにありません。

最後に docs フォルダ直下に index.md を作成します。  
このあたりは

![](https://gyazo.com/2dc2ce3d62c83f461cd2a4cd4e6e163e.png)

```
mkdocs new my-project
```

を使用しても作れますが  
あえてコマンドを使うまでもないので、手動でつくりました。

以上ができたら、GitHub にデータをプッシュしつつ

```
mkdocs gh-deploy
```

専用の GitHub 公開用コマンドを実行すれば作業は完了です。  
おしまい。

## 設定ファイルを編集する

ただ公開するだけだと一瞬でおわりますが、それだけだとアレなので  
細かい設定を加えていきます。

### テーマを設定する

見やすさ・機能両方とも、とても優秀な [Material Theme](https://squidfunk.github.io/mkdocs-material/) を使用します。

```yml
theme:
  feature:
    tabs: true
  language: ja
  name: material
  palette:
    accent: Green
    primary: Green
```

最近はじめてこの YML 形式を知りましたが、シンプルで編集しやすいのが良いです。  
theme:material でテーマを変更し、それ以外はそのテーマの各種オプションをセットしています。  
palette がテーマの色。  
tabs は後に追加する pages の 1 階層目をタブで切り替えできるようにするオプションです。

## Extension を追加する

MkDocs にはいろいろな拡張機能がありますので、  
使いやすそうな物をいれていきます。

```yml
markdown_extensions:
  - meta
  - pymdownx.mark
  - pymdownx.magiclink
  - pymdownx.emoji
  - fontawesome_markdown
  - pymdownx.keys
  - def_list
  - admonition
  - codehilite:
      linenums: true
      use_pygments: true
```

#### meta

md ファイルの頭に

```
path: docs/98_Other
source: mkdocs_setting.md
```

このように、GitHub 上でのパスとファイル名を書いておくと、  
![](https://gyazo.com/1cc193efac3fb6c7c98be22a86a6c5b4.png)

ページの末に、ソースコードまでのパスのリンクを追加してくれます。

#### pymdownx.mark

```
==Mark==
```

このように == で囲むと ==こうなります==

#### pymdownx.magiclink

URL を書くだけで、リンク扱いにしてくれます。（デフォルトだとできない）

#### pymdownx.emoji/fontawesome_markdown

絵文字 :smile: やアイコンフォント :fa-external-link: を使用できるようにします。

#### pymdownx.keys

```
++alt+shift+space++
```

こうすると、
++alt+shift+space++
こんなかんじに、ショートカット表示ができます。

#### admonition

```
!!! note
    hogehoge
```

!!! note
hogehoge

こんな感じで、Note や Warning を作成できます。

#### codehilite

コードを張り付けた時に、行数やコピペボタンを追加してくれます。  
このサイト的には必須。

読み込んだ Extension は、

```
  - codehilite:
      linenums: true
      use_pygments: true
```

こんな感じで、１つ下のインデントにオプションを追加すれば OK です。

## ローカルで確認する

書きながら結果を確認したい場合は、

```
mkdocs serve
```

を実行して、サーバーを起動します。

が、毎度サーバーを起動するためにコンソールを開くのはめんどくさいので  
VSCode のタスクを作成しておきます。

```tasks.json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "start_serve",
      "type": "shell",
      "command": "mkdocs serve",
      "group": {
        "kind": "build",
        "isDefault": true
      }
    }
}
```

.vscode/tasks.json に ↑ を追加しておきます。

![](https://gyazo.com/36f624879ebf4fbcb9b045996fb9a76b.png)

あとは、ビルドタスクで設定したタスクを選択すると

![](https://gyazo.com/c5f18cabe6fa35fcf4f485463684bcca.png)

コンソールでサーバーが起動します。  
あとは  
http://127.0.0.1:8000  
ブラウザでページを確認すれば OK です。  
md を編集したら、随時ページ側も更新されるのでらくちんです。

## 自動でメニューを作る

mkdocs は、特に何も指定しないと、docs 下の構成が自動でメニューツリーに追加されます。  
しかしそれだといろいろと問題があるので、  
自動でいい感じに生成してくれるスクリプトを作りました。  
長いので本体は
https://github.com/fereria/reincarnation_tech/blob/master/create_mkdocs_pages.py
こちらから。

設定は、mkdocs.yml に追加する必要があるので  
今回はテキスト処理ではなく yaml モジュールを使用して処理をします。

```python
def get_mkdocs_yml():
    # Jsonのように扱える
    with codecs.open(MKDOCS, 'r', 'utf-8') as file:
        yml = yaml.load(file)
    return yml
```

読み込むと、json と同じように、Dict と List 形式に展開してくれるので  
とても扱いやすいです。

このスクリプトを書くときに、素直に YML に持っていける Dict と配列を構成しようと  
いろいろテストしてたのですが、地味に苦戦したので  
実際のコードでは

1. まずはテキストの YML ファイルを生成
2. いったん読み込んで
3. get_mkdocs_yml()で取得したメインの設定に pages を追加する

という方法で処理をしました。

```
<!-- SUMMARY:メニューに表示される名前 -->
```

md ファイル名は英語、メニューは日本語にするのには、  
というコメントを追加しておいて  
この行をメニュー扱いにして置きかえるようにしています。

最後に、毎度スクリプトを実行しにいくのはめんどくさいので  
VSCode のビルドタスクを作成しておきます。

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "update_summary",
      "type": "shell",
      "command": "deploy.bat",
      "group": {
        "kind": "build",
        "isDefault": true
      }
    }
  ]
}
```

```bat
create_mkdocs_pages.py
mkdocs gh-deploy
```

メニューの更新とデプロイコマンドをセットにしたバッチを  
ビルドタスクに登録しておけば  
とくに意識しないでもメニューの更新ができるようになりました。

## レイアウトを調整する

Material テーマはおおむね満足なのですが、  
メニューの幅が狭すぎるのと、どれがフォルダなのか記事へのリンクなのかわかりにくかったので  
CSS を調整して幅を広げました。

カスタムな CSS を入れたい場合は

```yml
extra_css:
  - stylesheets/extra.css
```

extra_css: で、読み込みたい CSS を指定します。  
（docs 以下のパスで指定）

```css
@media only screen and (min-width: 100em) {
  label.md-nav__link {
    background-color: #3cb34057;
    padding: 2px 2px 2px 10px;
    font-size: 1.3rem;
  }
  a.md-nav__link {
    font-size: 1.3rem;
  }

  .md-grid {
    max-width: 142rem;
    margin-right: auto;
    margin-left: auto;
  }

  .md-content {
    margin-left: 34.2rem;
  }

  .md-sidebar--secondary {
    margin-left: 142rem;
  }

  .md-sidebar--primary {
    width: 34.2rem;
  }

  .md-nav__title {
    font-size: 1.7rem;
  }
}
```

CSS はほとんど知らないので苦戦しました。  
==@media only screen and (min-width: 100em) {==
この行で、デスクトップ用の時の時のみ設定が反映されるようにしています。  
（ブラウザの幅が指定ピクセル以上のときという設定）  
これがないと、スマホで見た時にレイアウトが壊れます。  
あとは、ブラウザの解析機能で、CSS の Class を探しつつ  
数値を調整しました。

## メニューのタブをすべてオープンにする

GitBook でもそうですが、全部のタブをチクチク開いて探していかないといけないのは  
けっこうな苦行なので  
デフォルトで全部オープンしておくようにしました。

```yml
extra_javascript:
  - javascripts/extra.js
```

まず、シーンに読み込みたい JS を追加して

```js
document.addEventListener("DOMContentLoaded", function() {
  var nav = document.getElementsByClassName("md-nav");
  for (var i = 0; i < nav.length; i++) {
    if (nav.item(i).getAttribute("data-md-level")) {
      nav.item(i).style.display = "block";
      nav.item(i).style.overflow = "visible";
    }
  }

  var nav = document.getElementsByClassName("md-nav__toggle");
  for (var i = 0; i < nav.length; i++) {
    nav.item(i).checked = true;
  }
});
```

このコードをコピペします。

![](https://gyazo.com/245531c7d601c2a24bba5946f5b0d49b.png)

設定の結果。  
折り返さない程度の広さに拡張し、フォルダは BG の色を変更しました。

https://fereria.github.io/reincarnation_tech/

以上の結果がこちらのサイト。  
Gitbook も悪くなかったのですが、表示するたびにそこそこ大きなラグがあるのと  
公式版だと自分でのカスタムがしにくい。  
かといって自分で GitLab でやるにはめんどくさい...  
ということもありほかの静的ページ生成ツールをテストしていましたが

軽いし、公開も楽だし、今までかいたドキュメントをほぼ丸々持ち込み可能だった  
ということもあり  
mkdocs+GitHubPages に落ち着きそうです。  
(python でできているというのも Good！)

というわけで、以降もこのサイトで  
いろいろと調べた内容を公開していこうとおもいます。  
がんばるぞー

## 参考

- https://qiita.com/mebiusbox2/items/a61d42878266af969e3c
