---
title: QThreadでマルチスレッドを使う(Signalの注意点)
---
# QThreadでマルチスレッドを使う(Signalの注意点)

GUIに表示する内容を、一定時間ごとにアップデートしたい時や  
GUIをクリックしたときに実行する内容が重くて、実行するごとにGUIが止まってしまうのを  
なんとかしたい場合、QThreadを使用して処理を別スレッド化してあげます。  
  
## サンプルコード

```python
#!python3
# -*- coding: utf-8 -*-
 
import sys
import os.path
 
import time
 
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtUiTools import QUiLoader
 
CURRENT_PATH = os.path.dirname(os.path.abspath(sys.argv[0]))
 
 
class TextEdit(QtWidgets.QWidget):
    count   = 0
    maxLine = 10
    def __init__(self, parent=None):
 
        super(TextEdit, self).__init__(parent)
        self.ui = QUiLoader().load(os.path.join(CURRENT_PATH, 'thread_sample.ui'))
        layout  = QtWidgets.QVBoxLayout()
        layout.addWidget(self.ui)
 
        self.setLayout(layout)
 
        # Signal
        self.ui.start.clicked.connect(self.startBtnClicked)
        self.ui.stop.clicked.connect(self.finishBtnClicked)
        self.ui.isrunning.clicked.connect(self.isThreadRunningBtn)
 
        self.p = TestProcess()
        self.p.printThread.connect(self.printLog)
        self.p.finished.connect(self.processFinished)
        
        self.logModel = QtCore.QStringListModel()
        self.ui.logView.setModel(self.logModel)
 
    def startBtnClicked(self):
        
        if not self.p.isRunning():
            self.p.restart()
        self.p.start()
 
    def finishBtnClicked(self):
        self.p.stop()
        
    def processFinished(self):
        self.printLog("finish.")
        
    def isThreadRunningBtn(self):
        self.printLog(str(self.p.isRunning()))
 
    def printLog(self, line):
        logs = self.logModel.stringList()
        logs.append(line)
        if len(logs) > self.maxLine:
            logs.pop(0)
        self.logModel.setStringList(logs)
        self.ui.logView.scrollToBottom()
 
 
class TestProcess(QtCore.QThread):
 
    printThread = QtCore.Signal(str)
 
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
 
        self.mutex = QtCore.QMutex()
        self.stopped = False
        
    def __del__(self):
        # Threadオブジェクトが削除されたときにThreadを停止する(念のため)
        self.stop()
        self.wait()
 
    def stop(self):
        with QtCore.QMutexLocker(self.mutex):
            self.stopped = True
            
    def restart(self):
        
        with QtCore.QMutexLocker(self.mutex):
            self.stopped = False
 
    def run(self):
        
        countNum = 0
        while not self.stopped:
            self.printThread.emit(str(countNum))
            countNum += 1
            time.sleep(1)
 
 
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dlg = TextEdit()
    dlg.show()
    sys.exit(app.exec_())
```

UIファイルは [こちら](https://snippets.cacher.io/snippet/035519fdc7b704e93511)  

![](https://gyazo.com/0263ea3b0a4e578f51a53b74c05d6adc.png)

実行するとこんな感じになります。  

内容はシンプルで、サブのスレッドで何か処理をしていて、  
その結果のログとかをMainのUIに表示したい...みたいな状況を想定しています。  
  
ログを送信するのには、Signalを使用して  
SignalでメインのGUIに文字を送信する形にしています。  
  
これ自体は、ずいぶん昔に  
http://flame-blaze.net/archives/4477
Blogのほうに書いていたのですが、Thread周りが原因でUIがなにも言わずに落ちてしまったり  
Signal周りの挙動やらをちゃんと理解できてなくてうわああああになることがあったので  
改めて調べてみました。  
  
## Signalの挙動の注意点

サブプロセスからSignalで数値を渡すときに、どのように値が渡されているか確認してみます。

```python
    def run(self):
        
        countNum = 0
        while not self.stopped:
            send = str(countNum)
            print(id(send))
            self.printThread.emit(send)
            time.sleep(1)
```

Threadのrunを↑のように変更し  
  
```python
    def printLog(self, line):
        
        print(id(line))
```

メイン側をこうしてみます。

![](https://gyazo.com/527261b5759cd0e6f223bd612cfd2bb0.png)

実行結果がこちら。  
python の id関数は、変数のメモリID(参照先)を確認することができます。  
見ての通り、strの場合はSignalで渡される前と後とでは別のメモリを参照していることがわかります。  
  
次に、試しに渡すのをstrからlistに変更してみます。
```python
    printThread = QtCore.Signal(list)
```
まず、Signalをlistに変更し、

```python
    def run(self):
        
        hoge = []
        while not self.stopped:
            print(id(hoge))
            self.printThread.emit(hoge)
            time.sleep(1)
```
runを変更します。

![](https://gyazo.com/d357ea188831a2db1e29dcf409145ae4.png)

おわかりいただけるだろうか...
strの場合は別のメモリを参照していたのが、  
listの場合は同じメモリを参照しています。  
  
これでなにが起きるかというと

```python
    def run(self):
        
        hoge = []
        while not self.stopped:
            print(id(hoge))
            print(hoge)
            self.printThread.emit(hoge)
            time.sleep(1)
```

runをこうして、

```python

    def printLog(self, line):
        print(id(line))
        line.append("hoge")
```

printThreadをうけとるSlotをこうする。

![](https://gyazo.com/f66e5818fb32f2e3aefbcc0baa2fd75d.png)

見ての通り、おなじ場所を参照しているので、メインスレッド側で  
サブスレッド側の変数の内容を書き換えられてしまいます。  
まじかよ....  
  
## 自作クラスオブジェクトの場合

では、自分で作ったクラスオブジェクトをSignalで送った場合はどうなるのか。

```python
class TestObj:
    
    def __init__(self):
        self.value = "hoge"
```

単純なクラスを作成し、

```python
    printThread = QtCore.Signal(TestObj)
```
Signalで送れるようにして  
  
```python
    def run(self):
        
        hoge = TestObj()
        while not self.stopped:
            print(id(hoge))
            print(hoge.value)
            self.printThread.emit(hoge)
            time.sleep(1)
```

runを書き換えて  
  
```python
    def printLog(self, line):
        print(id(line))
        line.value = line.value + "_" + "hoge"
```

こうします。  
  
![](https://gyazo.com/0d975806e70507b363780b730577bb43.png)

結果。  
listと同じくメモリが共有されているので、書き換えができてしまいます。  
（やばい）  
  
どういうことかというと、Pythonは基本的に「参照渡し」によって値を渡す使用（らしい）です。  
ただし、渡された型によってimmutableな型とmutableな型が存在していて  
immutableなものは変更不可な型の場合はメモリは共有されません。  
(int,float,complex,string,tuple,bite等)  
逆を言えば、それ以外は参照渡しで渡されてしまうわけです。  
詳しいところは↓にわかりやすく書かれていました。
https://crimnut.hateblo.jp/entry/2018/09/05/070000

## じゃあどうすれば

意図している場合はOKですが、メインとサブのスレッドで書き換えは起きてほしくない  
あくまでも別物として実行したい場合は、 copyモジュールのdeepcopyを使っておくのが  
今のところ安パイなきがしました。  
  
```python
    def run(self):
        
        hoge = TestObj()
        while not self.stopped:
            print(id(hoge))
            print(hoge.value)
            self.printThread.emit(copy.deepcopy(hoge))
            time.sleep(1)
```

こんな感じで、別のメモリを参照するようにしてemitすれば  
  
![](https://gyazo.com/c9df2862746d3f926305bf52e587dbb2.png)

参照先は違うので、別の物として扱われます。  
  
これでいいのかは別にしても、このあたりはきちんと意識してやらないと  
へんなメモリ書き換えが起きてしまってよく分からないエラーの原因になってしまうなぁと  
思いました。  
大反省。  
  
ちゃんと挙動を理解してやらないとだめですね。

## 参考

* http://t2y.hatenablog.jp/entry/20100914/1284436133