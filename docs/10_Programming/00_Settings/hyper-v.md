---
title: Hpyer-V で仮想デスクトップを作成する
---

# Hpyer-V で仮想デスクトップを作成する

## Hyper-V の有効化

まず、仮想デスクトップを使用出来るようにするために、Hyper-V を有効化します。

![](https://gyazo.com/30cf582edce07f8943019ef6b067de27.png)

Windows の検索から、Windows の機能の有効化または無効化を選択します。
2
![](https://gyazo.com/d3e44f062bf954fc2ee57aef7ecf5f48.png)

一覧から「hyper-V」を選択します。  
選択後（たぶん）Windows の再起動がされます。

![](https://gyazo.com/439070bb455a1178cff8c6f9d7359302.png)

検索から、「Hyper-V マネージャー」を検索して、実行します。

!!! Note
    Windows の機能で Hyper-V が有効化されていないと、Hyper-V マネージャーは表示されません。

## 仮想 PC を作る

操作 → クリック作成...を選択します。

![](https://gyazo.com/5494adf458e0f5e0bd08ef894b570dcf.png)

オペレーティングシステムを Windows10 の DevEnviroment にします。
実行すると、あとは待つだけで仮想 PC 環境が作成されます。

![](https://gyazo.com/16e28445b59f4b49b9ccde1bad693394.png)

完了したら「接続」をします。

## 設定する

まず、作成した仮想環境を起動して、Windows の初期設定の前に  
仮想環境のネットワークを設定します。

操作 → 仮想スイッチマネージャーを実行します。

![](https://gyazo.com/840e7b4b953cdc50c092c0caf9bd5cda.png)

新しい仮想ネットワークスイッチを選択して、「外部」を選択 → 仮想スイッチの作成　をします。

![](https://gyazo.com/516f1a041ab3232c6a4d9336da760795.png)

選択を「外部ネットワーク」の管理ぺレーティングシステムに..　のチェックを ON にして「適応」します。  
次に、作成した仮想マシンに接続します。  
仮想マシンから設定を選んで、仮想環境の設定画面を開きます。

![](https://gyazo.com/1a803c6ae305a6a1ed4a697359c98938.png)

ネットワークアダプタから、仮想スイッチを ↑ で作成したものに変更します。  
この設定をしていなかった場合、Internet の LAN の設定が表示されず  
仮想環境内でインターネットが使用できませんでした。

## 日本語化

まずは設定から「Time&Language」を選択。  
Settings 内の「Language」を選択し、　 Add a launguage 　を選択。

![](https://gyazo.com/5eb17a5e97d02bd6361d894aae61438a.png)

その中から日本語を選択します。  
選択したあと再起動すると日本語になります。

## チェックポイントの作成

仮想環境の良いところは、「チェックポイント」を作成することで  
現在の仮想環境の設定を保存することができます。

今回のように、ツールのテストを完全な素の状態（何かしら設定がされている自分の環境以外）でチェックしたい  
ので、最低限のインストールだけした状態の「初期状態」を作っておいて  
必要に応じてそのタイミングにロールバックしたいわけです。  
  
作り方は簡単で、  

![](https://gyazo.com/da8c8d0d1838011b6b5da8cf7177b5e5.png)

仮想マシン接続画面の「操作」→「チェックポイント」  
を選択します。  
  
![](https://gyazo.com/d90cbd215d71c8ed180c4a1f79054929.png)

あとは名前を付けて「はい」にします。  

![](https://gyazo.com/08384cb96f73225a7f581ae3c0d5c56c.png)

チェックポイントは、そのタイミングごとにツリーが作成されていきます。  
なので、ある程度作業を分岐させたいタイミングでチェックポイントを作成したり  
することで、環境丸ごと戻したりある地点に変更したりできます。  
変更したタイミングからまた分岐させることもできるので  
いろいろなパターン・環境で状況を再現することができます。  
  
地味にすごい。  
  
さらに、チェックポイントを作成すると、PCの設定環境だけではなく  
そのタイミングで「起動していたアプリの状態」まで保存されます。  

たとえば、Maya を起動した状態で「チェックポイント」を作成した場合も  
Maya が起動した状態が保存されます。

![](https://gyazo.com/6769b487e83a630a0f3f9cc76af8745c.png)

以上で環境作りは完了。  
仮想マシン上での Maya は普通の PC と同じ感じで操作できました。  
雰囲気としてはリモートデスクトップ越しに Maya を操作している感じです。

Python の環境は pipenv 等である程度切り分けていたのですが  
Maya 周りの環境は Windows の設定含めても完全に切り分けてテストしたかったので  
お手軽＆高機能な仮想マシンでの構築はけっこういいかもしれません。

## 参考

- https://qiita.com/nomurasan/items/3c58b964943a24751802
