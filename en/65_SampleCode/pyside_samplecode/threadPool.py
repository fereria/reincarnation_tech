# -*- coding: utf-8 -*-

title = "PySideのThreadPoolの使い方"
tags = ["PySide", "Python"]

import sys
import os.path
import time

from PySide2 import QtCore, QtGui, QtWidgets


class WorkerSignal(QtCore.QObject):

    finished = QtCore.Signal(object)

    def __init__(self):
        super().__init__()


class Worker(QtCore.QRunnable):

    def __init__(self, threadId):
        super().__init__()

        self.threadId = threadId
        self.signals = WorkerSignal()

    def run(self):

        for i in range(10):
            print(f"{self.threadId} -> {str(i)}\n")
            print(QtCore.QThread.currentThread())
            time.sleep(0.1)

        self.signals.finished.emit(self)


class Pool():

    def __init__(self):

        self.workers = {}

        self.pool = QtCore.QThreadPool()
        self.pool.setMaxThreadCount(5)

    def finishTask(self, worker):

        print(f'finish task -> {worker.threadId}')
        self.workers.pop(worker.threadId)

    def startWorkers(self, count):

        for i in range(count):
            self.workers[i] = Worker(i)
            self.workers[i].signals.finished.connect(self.finishTask)
            self.workers[i].setAutoDelete(True)
            self.pool.start(self.workers[i])

        # while self.pool.activeThreadCount() > 0:  # waitForDone と同じ。
        #     time.sleep(1)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    pool = Pool()
    pool.startWorkers(10)

    sys.exit(app.exec_())
