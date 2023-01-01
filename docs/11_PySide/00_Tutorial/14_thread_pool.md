---
title: ThreadPool でスレッド作成
tags:
    - PySide
    - Python
description: ThreadPoolとQRunnableを使用した並列処理の書き方
---

以前 {{markdown_link('06_qthread_01')}} という記事で、 QThread を継承して Thread を使用するサンプルを紹介しましたが、
これとは別にもう１つ「QThreadPool」を使用してスレッドを作成する処理のやり方があるので
紹介します。

## Thread とは

PySide で GUI を作るときに、重い処理（ファイルのコピー等）を実行すると
実行中は GUI が操作できなくなり、プログレスバーなども進行を正しく表示できないなどの
問題が発生します。

そういった場合は、GUI とは別に処理を Thread 化して GUI を止めないようにします。
そのようなコードを書くときには QThread を継承したクラスを用意して、その run に
スレッド化したい処理を書く...といった事が可能ですが、
もっと細かいタスクを、大量に実行したいような場合には、 :fa-external-link: [ThreadPool](https://doc.qt.io/qtforpython/PySide6/QtCore/QThreadPool.html#qthreadpool) というクラスを使用した
スレッドの書き方をするのが有効です。

## サンプル

全コードは {{markdown_link('thredPool_02')}} こちらから。

![](https://gyazo.com/f966a2327ffb974f871f13e244fd2994.png)

処理は非常にシンプルで、Start ボタンを押すと、ランダムな秒数だけプリント分を実行し
終わったら finish task とプリントするスレッドを１０個追加し、
スレッドは最大５個同時に処理する...といったサンプルコードになります。

ThreadPool をつかった場合の特徴は、Thread を管理するための QThreadPool クラスと、
実際のプロセスを実装するための QRunnable クラスで構成されています。

```python
class WorkerSignal(QtCore.QObject):

    finished = QtCore.Signal(object)
    sendLog = QtCore.Signal(str)

    def __init__(self):
        super().__init__()


class Worker(QtCore.QRunnable):

    def __init__(self, threadId, count=10):
        super().__init__()

        self.threadId = threadId
        self.count = count
        self.signals = WorkerSignal()
        self._stop = False

    def stopThread(self):

        self._stop = True

    def run(self):

        if self._stop:
            return

        for i in range(self.count):
            self.signals.sendLog.emit(f"{self.threadId} -> 残り{str(self.count - i)}")
            time.sleep(1)
            if self._stop:
                break

        self.signals.finished.emit(self)
```

QRunnable は、QThread と基本共通で、
run 関数をオーバーライドすることで、Thread 化する処理を実装します。

QRunnable は、QObject の子クラスではないため、Signal は使用できません。
ので、Thread 内で Signal を使うために Signal 用のクラスを作成していますが
それ以外は非常にシンプルな構成になっています。

```python
class SampleDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        # 略

        self.pool = QtCore.QThreadPool()
        self.pool.setMaxThreadCount(5)
        self.workers = {}
```

この QRunnable を使用するには、QThreadPool を作成し、pool.start(worker) で
実行する Runnable オブジェクトを渡します。
こうすると、指定の上限（setMaxThreadCount）だけ、別スレッドで処理が実行されます。

```python
    def push(self):

        for i in range(10):

            threadID = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S_%f_') + str(i)  # 今の日付をKeyにする

            self.workers[threadID] = Worker(threadID, random.randint(1, 10))
            self.workers[threadID].signals.finished.connect(self.finishTask)
            self.workers[threadID].signals.sendLog.connect(self.showMessage)
            self.workers[threadID].setAutoDelete(True)
            self.pool.start(self.workers[threadID])

        self.updateThreadCountUI()
```

実行例。
終了時やコメントの Signal を Runnable 側に作成してあるので
このように Signal-Slot を接続し、スレッドから Signal を受け取れるようにします。
この辺りは普通の PySide と同じです。

## Close 時の処理

これでも一応動くのですが、このままだとツールを終了したときに
Thread が残ってしまうので、終了時にはのこりの Thread を終了するようにしておきます。

```python
    def closeEvent(self, e):

        for i in self.workers:
            self.workers[i].stopThread()
        self.pool.waitForDone()
```

ThreadPool の場合どうするのが良いか迷いましたが、
QRunnable に終了する関数を追加しておき、Pool で実行中のスレッドがすべて終了するのを
待つようにします。
こうすることで、CloseEvent 時に実行中の Thread も待機中の Thread も
すべて終了してからツールが閉じるようになります。

## まとめ

１つのスレッドのみで裏で実行するとかであれば、QThread を継承するのでもよいですが
ファイルコピーだったりといった処理は
この ThreadPool を使用するほうが、綺麗に書けることがあります。

また、定期的に実行するようなものも、Thread で実行する内容が複雑ならば、
細かく QRunnable に分けて実装し、
QTimer と組み合わせて ThreadPool に Runnable な Worker を投げる等する
といった使い方も便利だと思います。
