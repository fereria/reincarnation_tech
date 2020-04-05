---
title: VSCodeでノートをつける
---

# VSCodeでノートをつける

近頃、できるかぎり環境をVSCodeにまとめていこうと色々カスタマイズしてるのですが、  
ノート周りも全部VSCodeに入れたい！ということで、  
VSNoteをためしてみました。  
  
https://marketplace.visualstudio.com/items?itemName=patricklee.vsnotes

使用したのはこちら。  
  
![](https://gyazo.com/a5cbc744119780a6db03dfeba2ea6ab1.png)

使い方は非常に簡単。  
拡張を入れると、メニューの所にアイコンが追加されます。  
  
![](https://gyazo.com/cf9785474f6000936e93ab884574225d.png)    

この下がノートの表示場所になります。  
  
## 初期設定

![](https://gyazo.com/df0514d64779e5c0b96b60cf10b59640.png)

設定はかんたんで、VSNotes:Run setupを実行して、  
ノートの初期保存場所を指定するだけです。  

![](https://gyazo.com/63d64e13a0d5ffdf52149edaf7e64c9e.png)

ノートを追加する場合は、Create a New Noteを選択します。  
  
![](https://gyazo.com/6f51915d31d29bf547cdf70ea7279e1f.png)

あとはノート名を入れると、Markdownファイルが作成されます。  
  
```markdown
---
tags:
  - tagA
  - tagB
---
# HogeHoge

はろーわーるど
```
ノートにはタグを入れることができて、  
ここでいれたタグで

![](https://gyazo.com/5ec6dc031e105cc5ad1aeaed45578295.png)

タグでグループ分けすることができます。  
  
## 自分用にカスタム

デフォルトのファイル名が、{dt}_{title}.{ext}だったのですが、  
それだとフォルダがカオスりそうなので、参考の画像にあるように  
  
Year_month/###.md　の階層になるように変更しました。  

```json
  "vsnotes.tokens":[
    {
      "type": "datetime",
      "token": "{year}",
      "format": "YYYY",
      "description": "Insert formatted Year."
    },    
    {
      "type": "datetime",
      "token": "{month}",
      "format": "MM",
      "description": "Insert formatted Month."
    },    
    {
      "type": "datetime",
      "token": "{dt}",
      "format": "YYYY-MM-DD_HH-mm",
      "description": "Insert formatted datetime."
    },
    {
      "type": "title",
      "token": "{title}",
      "description": "Insert note title from input box.",
      "format": "Untitled"
    },
    {
      "type": "extension",
      "token": "{ext}",
      "description": "Insert file vsnotes.",
      "format": "md"
    }
  ],
```

{dt} のような置換できる文字列は、自分で追加することができます。  
ので、yearとmonthを手動で追加して  
  
```markdown
"vsnotes.defaultNoteTitle": "{year}_{month}/{title}_{dt}.{ext}"
```
こんな感じでTitle名のデフォルト設定を変更しました。  

## Gitに保存

このノート自体は、自宅のGitLabにリポジトリを作成して  
そこにアップするようにしました。  

![](https://gyazo.com/20155190a495fe2b9877656cf8b89908.png)

そういう使い方を想定しているのか、  
CommitしてPushするコマンドがデフォルトで用意されています。  
  
## Cacherに送る

[Cacher](vscode_cacher.md) でも紹介した、Snippet共有ツールは  
Markdownをアップすると、HTMLで出力して共有する機能があります。  
  
https://snippets.cacher.io/snippet/07347332049fdeef6e06

ので、Noteで作成したもの（基本自分専用のクローズドなメモ）を  
人に公開したい！みたいな場合があっても  
CacherにPublicでアップしてURLを公開すれば、すぐに共有することが出来ます。  

![](https://gyazo.com/1eafc08f4a6b576dcca500d359af21be.png)

アップしたノートもタグ付けしておけば整理できるのもGood。  
  
自分の場合、画像関係は、 [Gyazo](https://gyazo.com/captures)というサービスのキャプチャを  
主に使用して記事を作成しているので、  
Cacherに送っても画像は普通に表示されます。  
超便利。  
  
## 用途とか

### Tech記事の下書き

このTechノートにアップする前の下書きやらメモやら用。  
Techのほうに下書きを書くと、別記事投下時に一緒にUPされてしまうのでよろしくない。  
ので、別途メモって置く場所が欲しかった。  
こちらもMarkdownだし、画像はGyazoなのでまるまるコピーすれば本体に移せる。  
  
### 非公開のメモ

仕事関係の調べ物とかで表には出せないようなものをこっちに書く。  

### 脳内整理用

考えてることとかをだらだらと書き残したい。  
  
## 感想

多機能ではないけれど、正直クローズドでメモするのならこれぐらいで良いです。  
  
近頃Wikiなんかも記述はMarkdownというのが多いのですが  
いかんせん改行の末尾スペースが面倒くさい。超めんどくさい。  
けど、VSCodeならスニペットでスペース改行を設定しておけば  
Markdownも苦にならないしプレビューも表示出来るので  
こっちで下書きしてあとでコピペできるようになるのは素晴らしいです。
  
あと、Taskのときもそうですが  
VSCodeはほぼ常時起動しているツールなので、そのVSCodeにメモ関係も統合できるのが  
非常にありがたいです。  
エディタから動きたくない派には最高です。  
  
以前テストしたときだとそこまで魅力的ではなかったのですが  
画像関係の貼り付けの簡略化（Gyazo）と、公開の手軽さ（Cacher）と  
ノート本体をMkdocs化した事によって、一気にうまみが出てきた気がします。  
  
しばらくはこれで運用しつつ、調整していこうとおもいます。  
  

## 参考

* https://www.karelie.net/vscode-notes/