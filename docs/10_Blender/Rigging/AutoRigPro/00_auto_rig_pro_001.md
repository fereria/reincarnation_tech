# AutoRigPro でセットアップをする 1 とりあえずの使い方

<!-- SUMMARY:AutoRigProのとりあえずの使い方 -->

## インストール

![](https://gyazo.com/1fd776bc848d7a52cc399fce431dec6f.png)

まずはインストール。

![](https://gyazo.com/bcfa00bbbfea9cd9d0644443a409d5e9.png)

マーケットでダウンロードした zip を解凍すると zip と py ファイルの 2 つがあるので  
本体の zip 側をプリファレンスの Add-ons の Install ボタンを押して出てくるダイアログで  
選択する。

![](https://gyazo.com/27a9c0ae003974b335407dd667e72aa3.png)

Addon のなかから「AutoRigPro」を選択する。  
▲ がついてるけども、これは 2.8 の対応が β 版だからなので無視して OK。

![](https://gyazo.com/366e6fe668c95752f19e392432a30580.png)

Addon を読み込むと、サイドバーに AutoRig の UI が追加される。

## ジョイントを作成する

準備ができたら、まずジョイントを作成していきます。  
今回は  
![](https://gyazo.com/8f782c1a2562d2a2efde60bd904f8dd3.png)

https://www.blendswap.com/blends/view/81455  
こちらのモデルを利用しました。
(RIG つきだったので、この中の Mesh_BMR_Orang のみ抜き出して使用)

![](https://gyazo.com/dc40ba2d0f176835527e90f81b7c7132.png)

まず、モデルを選択して Auto-Rig Pro:Smart の　 GetSelectedObjects を選択します。  
ここは、オブジェクトを選択しないと、ボタンが ON にならないのに注意。  
ボタンを押すと、ビューが Front になります。

![](https://gyazo.com/5768e0863d04f50a3ebd865bf2c08266.png)

ウィンドウがこんなかんじに Joint の配置位置を決める画面になるので  
順番に主要な位置を選択していきます。

順番は　首 → 顎（首の付け根）→ 肩 → 手首 → 腰 → 足首 → 顔  
顔はいらない場合は選択しないでも OK です。

![](https://gyazo.com/fd3645bcc8b67a06db064c12f824ac50.png)

選択すると、こんな感じになります。  
各パーツを選択するときに、このみどりの丸が表示され  
左右対称にうごかせるようになっています。  
そして、各部位に適切な位置で選択していきます。

![](https://gyazo.com/63fae7ecfd8dc084ed6edb5ece92a316.png)

終わったら　 Go!　を押します。

![](https://gyazo.com/c4e3da3d74ab38c0e4ed44a74c9ec080.png)

実行すると、こんな感じでジョイントが作成される。

![](https://gyazo.com/7c8472ce393c3c2229332bfa7a18246f.png)

Mesh の形状である程度判定しているのか  
ひざとかも Mesh の形状内の位置に配置されている。  
ただし位置は中間点なのかずれてはいるので調整は必要。

![](https://gyazo.com/38a42a5e50465661732558b810ab70a4.gif)

作成したジョイントは、左右対称に動くので  
スクリプトで生成後、位置を微調整すれば OK っぽいです。

ジョイントの調整が終わったら、スキニングをしておきます。（今回は省略）

![](https://gyazo.com/0c5bf52dd64c7cf121fc798655bac453.png)

調整が終わったら、「Match to Rig」を押すと

![](https://gyazo.com/aaf9f6d9c7db1fda1f06474e33e379dd.png)

コントローラーが作成できました。

![](https://gyazo.com/26f0fc7e4a81210d7ac05c4d4e7674d5.png)

Collection はこんな感じになっています。  
キャラモデルのように、ショット作成は Collection の Link ＋プロクシ
というのが前提としてあるのか、キャラ名コレクション下に Rig と Rig に使用するパーツの cs コレクション  
が出来る構造になっていますね。

![](https://gyazo.com/3b27bc88ac63d3bdc6a83eb804265679.png)

一緒に読み込めるようにモデルのコレクションもキャラフォルダ下に入れておきます。

とりあえず、基本を組むだけならものすごく楽ですね。  
ユレモノつくったり、高度なことをやるには物足りないかもしれないですが  
とりあえずサクッと RIG つけてアニメーションさせるのには十分なのではないでしょうか。

ダウンロードは  
https://blendermarket.com/products/auto-rig-pro  
こちらから。
