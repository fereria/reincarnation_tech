---
title: Notionの記事をMkdocsに投稿する
tags:
    - Notion
    - Python
    - mkdocs
description: python＋notion2mdを使って記事を投稿する
---

基本は markdown+VSCode で記事を書いている当 Blog ですが、
自宅の環境で記事を書くのではなく、ちょっとしたメモとかを自宅外で書いておきたいということがままあります。

そういったときは、Notion であったり Cacher だったりといったサービスを活用しているのですが
そういった記事を検索するときに、個別に検索するのは面倒なので
Notion の記事を mkdocs で記事として公開できるものは自分のサイトに公開できるようにしました。

## Notion のページを用意する

![](https://gyazo.com/e4a2450ba24f827a507395766a4c977d.png)

まずは、公開用のデータベースを作っておきます。
Blog のヘッダーに入れておきたいタイトルやタグ、説明、ページ化した時の階層構造等を
カスタムプロパティとして追加しておきます。

https://developers.notion.com

![](https://gyazo.com/643555eaa97e351d6d9e60ce3b9fb8b6.png)

事前に Developers から NotionAPI へアクセスするための　 Integration を作っておきます。

![](https://gyazo.com/840e2975fae0eb4a38d055884b239507.png)

Integration の Secrets の Token を今後のためにメモっておきます。

![](https://gyazo.com/3e3c2ee739cab1ba08d8fea3060713ad.png)

作ったら、コネクトの追加で作っておいた Integration を選びます。

これで準備完了です。

## 記事の一覧を取得する

アクセスする準備ができたら、記事の一覧を取得してから
指定の記事を markdown としてダウンロードしていきます。

```python
from notion_client import Client

notion = Client(auth="<TOKEN>")
```

データベースから、記事の一覧を取得するために、notion_client から Client を作ります。
この TOKEN は、Integration の TOKEN を入れます。

記事を取得するには、Client からデータベースに対してクエリを実行します。

```python
db = notion.databases.query(
    **{
        'database_id' : 'b7deece2ae104498ac2a932f39ffcfc7'  # データベースID
       }
)
```

![](https://gyazo.com/d549c40fc873bdeb81d7be0d975f7d86.png)

今回の場合は、データベースにある記事の一覧を取得したいので、
database_id を使用して一覧を取得します。

クエリ結果は、json 形式で帰ってきます。
結果は、 results に配列で取得できます。

## markdown のダウンロード

一覧が取れたので、そこから markdown をダウンロードしてきます。

https://github.com/echo724/notion2md

使うのは notion2md。
コマンドラインとしても使用できますが、Python のモジュールとしても使えるので
今回はモジュールとして使います。

記事を markdown でダウンロードするのに必要なのはページ ID と
ヘッダーに記述するのに必要なプロパティです。

```python
import os
os.environ['NOTION_TOKEN'] = '<TOKEN>'

from notion2md.exporter.block import MarkdownExporter
MarkdownExporter(block_id='03ce4d5f-f0f7-417a-a068-b46d1bd5eae8',output_path="./sample",download=True,unzipped=True).export()
```

notion2md は、 MarkdownExporter が用意されているので、これを利用してダウンロードします。
notion2md 用の TOKEN 指定は、指定の環境変数を指定しておく必要があるので、
environ で指定するか、Windows の環境変数で指定しておきます。
block_id は、データベース内の各記事に対して割り振られた ID を指定します。

![](https://gyazo.com/e76b30192afd5390599c2f0a2d4e342b.png)

これは、クエリの結果の id で指定できるので、
実際に扱う際はこの id を指定します。

## ヘッダー部分を追加する

あとは、プロパティを取得してヘッダー部分をダウンロードした markdown に追加します。
NotionAPI で取得したプロパティは、 properties['Name'] （Name は Notion の Property 名）で取得できます。
各プロパティ以下は、Notion のプロパティ形式によって形式が変わりますが、
https://developers.notion.com/reference/page-property-values
API ドキュメントに構造がまとめられています。
これをもとにして、必要に応じて加工します。

```python
for i in db['results']:
    title = i['properties']['Name']['title'][0]['plain_text']
    tags = [x['name'] for x in i['properties']['Tags']['multi_select']]
    subdir = i['properties']['dir']['rich_text']

    # Publishオフの場合はなにもしない
    if not i['properties']['publish']['checkbox']:
        continue

    header = ["---"]
    header.append(f'title: {title}')
    if len(tags):
        header.append('tags:')
    for tag in tags:
        header.append(f"    - {tag}")
    header.append('---')

    outputPath = "./sample"
    if len(subdir):
        outputPath += "/" + subdir[0]['plain_text']

    MarkdownExporter(block_id=i['id'],output_path=outputPath,download=True,unzipped=True).export()

    markdownName = f"{outputPath}/{i['id']}.md"

    with codecs.open(markdownName,'r','utf-8') as f:
        lines = [x + "\n" for x in header] + f.readlines()

    with codecs.open(markdownName,'w','utf-8') as f:
        f.write("".join(lines))

    fname = i['properties']['filename']['rich_text']
    if len(fname):
        os.rename(markdownName,f"{outputPath}/{fname[0]['plain_text']}.md")
```

ダウンロードしたファイルに対して、ヘッダーを書き足して
ファイル名が指定されていたら、そのファイル名にリネームして完了です。

https://github.com/fereria/reincarnation_tech/blob/master/scripts/create_notion_page.py

いろいろ形を整えて、mkdocs のリポジトリに入れておきます。

## Actions で実行

準備ができたら GithubActions に仕込みを追加します。
従来の記事の更新は、markdown をプッシュしたタイミングでビルドが実行されるようになっていますが
Notion の場合はそうもいきません。
ただ、そこまでリアルタイムである必要もないので、毎日夜に記事をビルドするようにしておきます。

```yaml
on:
    push:
        branches:
            - master
    repository_dispatch:
        types:
            - submodule_update
    schedule:
        - cron: "0 16 * * *"
```

定期実行するには schedule を指定します。
上の場合夜の 1 時頃に処理が走るようにしました。

```yml
- name: Create NotionPages
  run: docker exec mkdocs python scripts/create_notion_page.py TOKEN DATABASEID
```

さらに、作成した Python を実行するようにステップを足します。
env で環境変数を足せば OK だとおもってたのですが、それだとうまくいかなかったので
Github で TOKEN を保存しておいて、引数で Python 側で environ を入れるようにしておきました。

https://fereria.github.io/reincarnation_tech/70_Memo/samplepage/

できあがったのがこちら。

https://zenn.dev/dashboard/scraps

今まで似たようなことは Zenn のスクラップを使っていたのですが
今後は Notion ＋ mkdocs 側にまとめていこうと思います。
