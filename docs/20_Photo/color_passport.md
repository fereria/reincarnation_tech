---
title: color passport で lightroom のプロファイルを作る
---
# color passport で lightroom のプロファイルを作る

## ColorPassport とは？

撮影したときの色を再現するための Lightroom 用（だったりそれ以外の現像ソフト用の）  
プロファイルを作成してくれるチャート＋ソフトウェアの事です。

https://xritephoto.com/colorchecker-passport-photo

今回は、わりと一般的に使用されている X-Rite の

![](https://i.gyazo.com/56b2f1055baa077077c722d5e6aac592.png)

パスポートを使用しました。

## 撮影する

![](https://gyazo.com/7487e160240ef7ea43e069bccbb4e6ed.jpg)

まず、パスポートのチェッカー部分をカメラで撮影します。  
このとき撮影は JPG ではなく RAW 撮影します。

撮影した RAW を LightRoom で読み込み、DNG に変換をします。

チェッカーは、写真のように横に置いた状態にして撮影します。  
縦でも一応 OK ですが、横の場合は自動で認識してくれます。

DNG ファイルの準備ができたら、付属の　 ColorChecker Passport 　をインストールし、  
起動します。

![](https://i.gyazo.com/3c27294c6a063c912105d09df8d97aa7.png)

ツールを起動したら、「DNG 画像をここにドラッグ＆ドロップします」に入れます。

注意点？でもないですが、最新の Lightroom で取り込んだ DNG で  
パスポート付属の CD からインストールした ColorChecker Passport とだと  
DNG が読み込めない形式というエラーが発生して読めませんでした。  
最新の 1.1.1 では問題なくロードできました。

![](https://i.gyazo.com/11e65049588dc7faa9da7f5ae7ab6ff5.png)

正しく認識されると、自動でこのようにカラーチャートがピックアップされます。  
旨く認識されない場合は、手動でチャートの四隅を選択することで  
指定することができました。

読み込みできたら「プロファイルの作成」を行います。

![](https://i.gyazo.com/103ccaf17d242f552b29b288145e9679.png)

デフォルトで LightRoom のカメラプロファイルの保存フォルダにいるので  
名前をつけて dcp ファイルを保存します。

![](https://i.gyazo.com/25ae439ae86b79a66c99833a1bbf6b90.png)

Lightroom を再起動し、プロファイル → 参照を選択

![](https://i.gyazo.com/5ac64c8fff33777bf19a35cef5ee555d.png)

一覧に、先ほど保存した dcp ファイル名があるので、それを選択すれば完了です。

撮影開始前にパスポートを撮影 → 現像前にプロファイルを作る → プリセットを作る

プロファイルを作るだけならばものすごい楽でした。  
(ドキュメントを起こすまでもない Lv...)

この手順でやれば、色調整周りの手間が大分減りそうです。
