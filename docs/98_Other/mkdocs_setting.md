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
  
こんな感じで、NoteやWarningを作成できます。  
  
#### codehilite

コードを張り付けた時に、行数やコピペボタンを追加してくれます。  
このサイト的には必須。  
  
読み込んだExtensionは、
```
  - codehilite:
      linenums: true
      use_pygments: true
```

こんな感じで、１つ下のインデントにオプションを追加すればOKです。

## ローカルで確認する

書きながら結果を確認したい場合は、
```
mkdocs serve
```
を実行して、サーバーを起動します。  
  
が、毎度サーバーを起動するためにコンソールを開くのはめんどくさいので  
VSCodeのタスクを作成しておきます。  
  
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

.vscode/tasks.json に↑を追加しておきます。  

![](https://gyazo.com/36f624879ebf4fbcb9b045996fb9a76b.png)

あとは、ビルドタスクで設定したタスクを選択すると  
  
![](https://gyazo.com/c5f18cabe6fa35fcf4f485463684bcca.png)  

コンソールでサーバーが起動します。  
あとは  
http://127.0.0.1:8000  
ブラウザでページを確認すればOKです。  
mdを編集したら、随時ページ側も更新されるのでらくちんです。  
  


## 参考

- https://qiita.com/mebiusbox2/items/a61d42878266af969e3c
