---
title: VSCodeでSQL
tags:
    - SQL
    - VSCode
description:
---

## mssql の設定

まずは、MSSQL 側の設定をチェックします。

![](https://gyazo.com/7457c87e7a0b53d1774e209863b42403.png)

サーバープロパティのセキュリティで「SQLServer 認証モードと Windows 認証モード」を ON にします。

![](https://gyazo.com/6625e7dad27254758379227a096c7416.png)

そしてセキュリティから、ユーザーを追加し、ログイン用のアカウントを追加します。

![](https://gyazo.com/b222406034d6c0e2bae5321c6992a994.png)

SQLServer 認証で、ログイン名とパスワードを指定します。

![](https://gyazo.com/e9ff10c37f0240f7770026602ca7133d.png)

次に、SQLServer の構成マネージャーを開き、 SQLServer ネットワーク構成の
MSSQLSERVER のプロトコルを開き TCP/IP を有効化し、

![](https://gyazo.com/ae35767a76690cbf430719fa2d900a91.png)

プロパティで TCP ポートをチェックします。
チェックしたら PC を再起動しておきます。

## VSCode の指定

準備ができたら、VSCode 側の設定をします。

![](https://gyazo.com/6a8c57d6a8b0c6eb15bc20c518a033a1.png)

![](https://gyazo.com/808716438f1a1a1e8026efdbadbc9ffb.png)

インストールするのは SQLServer(msssql) と SQLNotebook の２つ。
SQLServer をインストールすると、一緒に必要な別のアドオンも追加されます。

接続の右にある　＋　を押して、mssql のサーバーを指定します。

![](https://gyazo.com/d26680787976f3646fce54b0364987c4.png)

指定すると、接続したデーターベースのテーブルなどが VSCode 側で確認することができます。
hogehoge.sql のようにファイルを作成して、
クエリの実行を実行すると、開いているファイルのクエリを実行することができます。

![](https://gyazo.com/123ae9884c8dc0822ed77e324ccd99f4.png)

デフォルトのショートカットは使いにくかったので Ctrl+Q Ctrl+Q で実行できるようにしました。

![](https://gyazo.com/3a9bdd6851d66ec0494d189d1304a15b.png)

実行すると、接続先を聞かれるのでEnter

![](https://gyazo.com/405246aa779b4d7df575eff840134562.png)

実行すると、別ウィンドウで結果が表示されます。

### Notebook

mssqlアドオンでもだいぶ便利なのですが、勉強中はNotebookみたいに実行できたらいいなー
と思って調べてみたらありました。
それがSQLNotebook

#### 設定する

![](https://gyazo.com/4a4a3bcb9e0f3f7739cd214398eafe2a.png)

SQLのアイコンから NEW SQL CONNECTION で、接続先のデータベースを指定します。
ポートは、
MSSQLSERVER のプロトコルの TCP/IPのプロパティに書かれていたTCPポートです。
（TCP/IPが無効だと接続できなかった）

![](https://gyazo.com/a09a0eaa48d5bf8be03bdfbe52f4d8cb.png)

エクスプローラーで sqlファイルを右クリックし、ファイルを開くアプリケーションの選択...
を選び、

![](https://gyazo.com/23dc7d773210b17badf4b855555790e8.png)

SQLNotebookを選びます。

![](https://gyazo.com/30036a2b96ce5ea1705a35e464fe0e4d.png)

開くと、Notebook形式で開けるので、あとは
セルにSQLを書いてShift+Enterで実行できます。