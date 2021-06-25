---
title: VSCodeでタスク管理
---
# VSCodeでタスク管理

VSCodeの拡張TODO+がタスク管理に良さそうだったので  
色々と設定してみました。  
  
使用したのは  
https://marketplace.visualstudio.com/items?itemName=fabiospampinato.vscode-todo-plus  
これ。  
  
## 使い方  
  
まず、現在のプロジェクトごとのタスク管理をします。  
  
![](https://gyazo.com/23041534f929b19e24868e006811fcc4.png)

コマンドで Todo: Openを選択します。  
  
![](https://gyazo.com/cb5984ac27e1ef619fb4d439d6448c18.png)

実行すると、VSCodeのプロジェクト直下に  
TODOファイルが作成されます。  
  
![](https://gyazo.com/09e245e2a3f2624d991b59d29ee37706.png)

エンコードがアレなので、UTF-8に変更して保存します。  
  
![](https://gyazo.com/1fdf8028f1dd40715f44d1c6b75fe495.gif)

できたTODOファイルに、
```
Group:
```
このように、###: でタスクのグループ（プロジェクト？）を作成します。  
あとは、インデントした次の行で Ctrl+Enterを押すと  
チェックボックスが追加されるので、タスクの内容を記入します。  

![](https://gyazo.com/5d63a2461ef26075a7c08012a3760c19.gif)

タスクを終了したい場合は、Todo: Toggle Doneを実行すると終了＋終了時間を記録してくれます。

![](https://gyazo.com/388b3e6c936cf596d47b90fe8a60cdc9.png)

記入したタスクは、メニューの☑アイコンを押すと、一覧で確認することができます。  


## 便利な機能

## タグをつける

![](https://gyazo.com/ee78138e2a6be028baee18a3b3164658.gif)

@### でタスクに対してタグ付けすることができます。  

![](https://gyazo.com/d452f9447d184eb3defa2eae8b17abf5.png)

@マークを入れれば、予測変換もでてきます。  

## 予定時間を入れる

![](https://gyazo.com/9ec08c1e8884bd6d11038347727b5c68.png)

タスクの後ろに @時間　を入れると、予定時間を入れることができます。  
プロジェクトには、その予定時間の合計が表示されます。  
  
![](https://gyazo.com/dd691eeb6784b319bd12c89ee7e4c7be.png)

その状態で、Todo:ToggleStartを実行すると、  
  
![](https://gyazo.com/cd949a0530e1f42bad98fabb335af92a.png)

開始時間が記録されて  
  
![](https://gyazo.com/ecd8ada0b740cbb83d63fad76e07623c.gif)

残り時間がタスクバーに表示されます。  
これは怖い。  
  
![](https://gyazo.com/1a8d0e87a80c451efec8d315140c9ea8.png)

この状態で、タスクを終了すると  
終了時間と実際にかかった時間も記録することが出来ます。  

## アーカイブする
  
![](https://gyazo.com/5d63fd27f24da9eaaf48f13de9b536c1.gif)

終了したタスクは、アーカイブを実行することで  
アーカイブプロジェクトに移動することができます。  

こんな感じで、タスク記録としてはほしい機能がそろってるので  
VSCodeで完結できる都合、この方法で実践してみようかとおもいます。  
  
VSCodeのスクリプトプロジェクト以外のタスクについては、  
  
```json
 "todo.embedded.include": ["**/*", "C:/Users/remir/CloudStation/TODO"],
```
こんなかんじで、Synologyのフォルダ同期フォルダを（DropboxやOneDriveのようなもの）  
TODO+のパースフォルダ下に指定しておいて  

![](https://gyazo.com/2736c27e89e7dcf6a6f84dfa271aebdc.png)

その下にTODOファイルを配置して、そっち側にタスクを記入するようにしました。  
こうしておけば、他のPCでも同期することができます。  
  
各種作業しているときにしても、ドキュメントを書いてるときにしても  
最近はVSCodeは必ず起動しているので  
あえてアプリでやるよりも自分には合っている気がします。  
  
## スクリプト内のタスクを確認する  
  
普通のTODO管理だけでもけっこう便利でしたが、それより便利なのが
スクリプト内のコメントでTODOやらDEBUGやらFIXMEやらを書いておいたときに  
その内容を抽出して表示する機能。  
  
![](https://gyazo.com/d66365b03f51f05e279f8319d247ea70.png)

プロジェクト内のコード内に、こんな感じのコードを書いておくと  
  
![](https://gyazo.com/ed0b408c620af29a29590620cf1dd20e.png)

こんな感じで、TODOのメニュー内の「EMBEDDED」内に  
現状書かれているTODOやらFIXMEのようなタグが表示され  
その該当行を開くことができます。  
  
![](https://gyazo.com/e62a5292ca2373f65774e4ad996f8962.png)

書くタスクに書かれているタスクをテキストにリストしたい場合は  
「Todo:Open Embedded」を実行すると  

![](https://gyazo.com/c774a620fc5d1e208246d7e69300e44f.png)

タスクをリストして、テキストに落とし込むことができます。  
  
## コード内のTODOなどの行をハイライトさせる  
  
コード内にTODOをメモっていると  
見落としたりすることがありそうなので、指定のタグが付いている場合は  
その行をハイライトするようにしました。  
  
https://marketplace.visualstudio.com/items?itemName=wayou.vscode-todo-highlight

使用しているのは、この　TODO Highlight。  
  
```json
  "todohighlight.keywords": [
    {
      "text": "DEBUG:",
      "color": "#FFFFFF",
      "backgroundColor": "#dd5706"
    },
    {
      "text": "NOTE:",
      "color": "#FFFFFF",
      "backgroundColor": "#2741a0"
    },
    {
      "text": "HACK:",
      "color": "#FFFFFF",
      "backgroundColor": "#a0275d"
    },
    {
      "text": "TODO:",
      "color": "#FFF",
      "backgroundColor": "#30730f"
    },
    {
      "text": "FIXME",
      "color": "#FFF",
      "backgroundColor": "#e808ab"
    }
  ],
  "todohighlight.defaultStyle": {
    "isWholeLine": true
  },
```
setting.json内に↑の設定を追加して  
目立つようにしています。  
  
![](https://gyazo.com/c0af9b3db469aa1ec6960437bb31f8e6.png)

このタグを入れておくと、スクロールバーにも色が残るのがなかなか良いです。  
  
とりあえずこれで設定完了。  
TODO+はこれ以外にももっとカスタマイズできるので、色々調整しつつ  
運用してみようと思います。  
  
