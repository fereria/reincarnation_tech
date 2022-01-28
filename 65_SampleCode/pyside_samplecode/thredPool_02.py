# -*- coding: utf-8 -*-
import sys
import time
import datetime
import random

from PySide2 import QtCore, QtWidgets


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


class SampleDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.view = QtWidgets.QListView(self)
        layout.addWidget(self.view)
        self.model = QtCore.QStringListModel()
        self.view.setModel(self.model)

        self.line = QtWidgets.QLabel()
        layout.addWidget(self.line)

        btn = QtWidgets.QPushButton("Start")
        btn.clicked.connect(self.push)
        layout.addWidget(btn)

        self.pool = QtCore.QThreadPool()
        self.pool.setMaxThreadCount(5)
        self.workers = {}

    def closeEvent(self, e):

        for i in self.workers:
            self.workers[i].stopThread()
        self.pool.waitForDone()

    def updateThreadCountUI(self):

        activeThreadCount = self.pool.activeThreadCount()
        message = f"実行中のスレッド数 {str(activeThreadCount)} 待機スレッド {str(len(self.workers) - activeThreadCount)}"
        self.line.setText(message)

    def showMessage(self, message):

        messages = self.model.stringList()
        messages.append(message)
        self.model.setStringList(messages)

    def push(self):

        for i in range(10):

            threadID = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S_%f_') + str(i)  # 今の日付をKeyにする

            self.workers[threadID] = Worker(threadID, random.randint(1, 10))
            self.workers[threadID].signals.finished.connect(self.finishTask)
            self.workers[threadID].signals.sendLog.connect(self.showMessage)
            self.workers[threadID].setAutoDelete(True)
            self.pool.start(self.workers[threadID])

        self.updateThreadCountUI()

    def finishTask(self, worker):

        self.showMessage(f'finish task -> {worker.threadId}')
        self.workers.pop(worker.threadId)
        self.updateThreadCountUI()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    ui = SampleDialog()
    ui.show()

    sys.exit(app.exec_())
