# VSCode でアドオン開発

<!-- SUMMARY:VSCodeでアドオン開発-->

## Extension を導入する

![](https://gyazo.com/b1569bfa995692541966ac681db7d4e3.png)

まず、Blender のアドインを開発できるように Extension を追加する。  
拡張機能で**「Blender Development」**を追加する。

![](https://gyazo.com/ba04120fde1f00d08dd084b10443be67.png)

追加したら、コマンドパレットから　 Blender:NewAdon を選択する。

![](https://gyazo.com/d8f785e838a83e1b65635921b89cf3d0.png)

テンプレートを選択（With Auto Load）し、アドオン名と開発者目にを入力し、  
アドオンを保存するフォルダを選択する。

![](https://gyazo.com/46784bef2aaf8f82e9491f85f8bb4a44.png)

作成タイプを **init**.py にすると、  
本体にあたる auto_load.py と、レジスト処理を行う **init**.py ファイルが  
作成される。

## 実際に実行する

![](https://gyazo.com/45c027f904a3cc1ba6b5a03e7a91cc9a.png)

まず、コマンドパレットで Blender:Start を実行する。

![](https://gyazo.com/82536c4166ba820db68f79a903853a61.png)

その後、初回時は Blender の exe を選択する画面が出てくるので  
Choose a new Blender executable を選んで、exe を選択する。

exe を選択すると、指定の Blender が起動する。  
このとき、指定フォルダ以下の Blender に psvsd モジュールがない場合は  
自動で pip が走り、必要なモジュールのインストールが始まる。  
その間 Blender がフリーズしてしばらく帰ってこなくなるが  
焦らず終わるまでまつ。（待てずに強制終了した人）

![](https://gyazo.com/b91dcd38da7dc447ee9009612fe758ec.png)

準備が終わると、BlenderServer が起動して、DebugClient がアタッチされる。

![](https://gyazo.com/a423274e479898819dc2e47def554958.png)

無事に起動すると、SideBar に Development 画面が追加される。

この状態だと、ブレークポイントを追加したり自動更新をしたりしながら  
VSCode 上で開発することができる。（はず）
