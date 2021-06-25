---
title: VSCodeでCacherを使う
---

# VSCode で Cacher を使う

Cacher とは、各種言語のスニペットを管理するためのサービスです。  
かつてあった、Gists の内容をタグ管理できる GistBox の後継サービスになっています。

https://www.cacher.io/

基本無料で使用できますが、無料の場合 Private でアップできるコードの数に制限があるので  
クローズドで使用するのであれば、有料必須です。  
お値段は月額 6 ドル、お試しもできるので気になる人は試してみるのをお勧め。

## 使ってみる

Cacher は、WindowsApp や Web 上で動くページなどいくつかの表示方法がありますが  
基本どれを使用しても同じです。

![](https://gyazo.com/241cce95cda534a9545fc0fc24c20e7f.png)

UI はこんなかんじで、スニペットのリストとタグ管理等々の機能が一通りそろっています。

![](https://gyazo.com/4e302ee6aec54669a6832e74f70af36b.png)

NEW SNIPPET をクリックすることで、新しいスニペットを登録することができます。

追加したスニペットは、

https://snippets.cacher.io/snippet/39b432127fd0785d6d3d

こんな感じで URL を共有することができます。

![](https://gyazo.com/73f4464c4d45d9d458328a1966d89bdb.png)

さらに、SharePage のところを EMBED にすると、  
Blog にコードを張り付けるための URL を取得することができます。

<script src="https://embed.cacher.io/d35f6a840f30ab42aefc40930d251ff32d5faa15.js?a=7421a7ec6d9fce1698b029ef2cb9473a"></script>

mkdocs でも使用することができました。

## Tag をつける

![](https://gyazo.com/d39b7d34415d5aa0961d9f339ed4e7c8.png)

タグは、登録するところからだと新しく増やせない（ここだけ不満）ので、  
LABELS の＋ボタンをクリックして New Label を追加します。

![](https://gyazo.com/9c011b8122318c7d63885cdde956c363.png)

右上の LABELS から、ラベルを選択 → 追加することができます。

と、ここまでが前座になります。

## VSCode から使用する

![](https://gyazo.com/d8e150dc5ba7094822b1a9c7fb65298b.png)

Cacher は、主要なエディタに対応していて  
私が今メインで使用している VSCode でも使用することができます。

![](https://gyazo.com/665c604df1840e7600c81a3a6eade3fc.png)

まず、マケプレから Cacher の拡張を追加します。

![](https://gyazo.com/a999202f4360475d4fff25b315533c39.png)

Cacher:Setup を実行して、

![](https://gyazo.com/779c97bcdeaaa6ea0b88d86f75600aa3.png)

API KEY と、API TOKEN を入力します。

準備ができたら、

![](https://gyazo.com/b51d3e85414008f9bee8f9addf1927ec.png)

Insert Snippet を実行すると、

![](https://gyazo.com/0a23e1732757fe4a73ccb35972c614bf.png)

Cacher に登録されているスニペットが表示されます。  
検索もけっこう早い。

もちろん、VSCode のコードを Cacher に登録することもできる。

![](https://gyazo.com/15b1a8be0ff4e53db6881a3511a6f8f4.png)

選択していれば、選択範囲を　なにも選択していなければ  
全コードを Cacher に UP してくれる。

![](https://gyazo.com/7cf42484d96435f2d9f36f002b34e8ff.png)

VSCode 側からも Tag をつけられる。

VSCode にもユーザースニペットはあるし、よく使う 1 行の物とかはそれで良いのですが  
複数行のものなんかは VSCode のスニペット登録は死ぬほどめんどいし  
もうちっとなんとかしたかったのですが  
Cacher を使えば、管理するのも楽だし、VSCode に貼り付けるのも楽だし  
登録するのも楽なので、ストレスがなくなりました。

## その他便利機能

### Markdown のページを作る

![](https://gyazo.com/ecea8dded6430007c3a48c1497366d36.png)

NEW SNIPPET から Markdown を呼び出すと、

![](https://gyazo.com/ac83538d5650709929e602ab60c747db.png)

プレビュー付きの Markdown エディタになる。

![](https://gyazo.com/2e3023310bf54a5a2a07c9c4b5253f9c.gif)

しかし、なぜかエフェクトがエグすぎてつかいものにならんです。  
なので、Markdown も VSCode で作成して、  
CreateSnippets で Cacher に登録するのがベターです。

https://snippets.cacher.io/snippet/22deabec535e53cd0ad6

作成したページを共有すると、プレビュー状態になるので  
簡易的な文章共有に使えます。

![](https://gyazo.com/fa452d4031d1aee8ea0b2ad91b56937f.png)

あと、HTML と PDF を DOWNLOAD する機能があります。

![](https://gyazo.com/b25148a603df7fb6e7ddf2edb95bdca7.png)

しかし、非常に残念なことに日本語非対応...

## Chrome などで、サンプルコードを Cacher に送る

![](https://gyazo.com/7c55f50ac0c2af5c50df07b8f5e39460.png)

GistBox の拡張機能のように、Chrome の拡張機能で HP 上のソースコードを  
Cacher に送ることができます。  
ただし、できるものと出来ないものがあるようなので  
完全に頼ることは出来ません。  
残念。

## そんなかんじで...

コレを使う前は、自前の GitLab スニペットに登録していたり、  
BoostNote を使ってみたりしてたのですが  
エディタから直登録・呼び出しできないと非常に辛いので使用が遠のいてました。  
ですが、Cacher と VSCode をがっつり連携させたら、  
かなりストレスが減ったので、  
小ネタの登録だとかテンプレ登録関係は  
がんがん使っていこうと思います。
