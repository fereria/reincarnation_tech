#!python3
# -*- coding: utf-8 -*-
 
import os.path
import sys
 
from PySide2.QtCore import QAbstractItemModel, QModelIndex, Qt
from PySide2.QtWidgets import QApplication, QDialog, QTreeView, QVBoxLayout, QMenu
 
 
class BaseItem(object):
    def __init__(self, data=None, parent=None):
 
        self.parentItem = parent
        self.itemData = data
        self.childItems = []
 
    def appendChild(self, item):
 
        self.childItems.append(item)
 
    def removeChild(self, row):
        self.childItems.pop(row)
 
    def child(self, row):
        if len(self.childItems) > row:
            return self.childItems[row]
        else:
            return None
 
    def childCount(self):
        return len(self.childItems)
 
    def columnCount(self):
        return 1
 
    def data(self, column):
        if self.itemData is None:
            return ""
        return self.itemData['key']
 
    def parent(self):
        return self.parentItem
 
    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)
        return 0
 
    def clear(self):
        self.childItems = []
 
 
class TreeItem(BaseItem):
 
    def __init__(self, data, parent=None):
        super(TreeItem, self).__init__(data=data, parent=parent)
 
 
class TreeModel(QAbstractItemModel):
    def __init__(self, items=[], parent=None):
        super(TreeModel, self).__init__(parent)
 
        self.__items = items
        self.rootItem = BaseItem()
        # 現在のページ
        self.setItems(items)
 
    def setItems(self, items):
 
        self.__items = items
        self.setupModelData()
 
    def addItem(self, parent, text):
 
        item = parent.internalPointer()
        self.beginInsertRows(parent, item.childCount(), item.childCount())
        i = TreeItem(data={"key": text}, parent=item)
        item.appendChild(i)
        self.endInsertRows()
 
    def removeItem(self, item):
 
        parent = self.parent(item)
        if parent.isValid():
            pItem = parent.internalPointer()
            self.beginRemoveRows(parent, item.row(), item.row())
            pItem.removeChild(item.row())
            self.endRemoveRows()
 
    def columnCount(self, parent):
 
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()
 
    def data(self, index, role):
 
        if not index.isValid():
            return None
        if role != Qt.DisplayRole:
            return None
        item = index.internalPointer()
        return item.data(index.column())
 
    def flags(self, index):
 
        if not index.isValid():
            return Qt.NoItemFlags
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable
 
    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.rootItem.data(section)
        return None
 
    def index(self, row, column, parent):
 
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()
 
    def parent(self, index):
 
        if not index.isValid():
            return QModelIndex()
        childItem = index.internalPointer()
        parentItem = childItem.parent()
        if parentItem == self.rootItem:
            return QModelIndex()
        return self.createIndex(parentItem.row(), 0, parentItem)
 
    def rowCount(self, parent):
 
        if parent.column() > 0:
            return 0
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()
        return parentItem.childCount()
 
    def setupModelData(self):
        """
        表示用のItemを再構築する
        """
        self.rootItem.clear()
        parents = {}
        self.beginResetModel()
        for item in self.__items:
            if item['parent'] in parents:
                p = parents[item['parent']]
            else:
                p = TreeItem(item, self.rootItem)
                self.rootItem.appendChild(p)
                parents[item['parent']] = p
            treeItem = TreeItem(item, p)
            p.appendChild(treeItem)
        self.endResetModel()
 
 
class UISample(QDialog):
 
    def __init__(self, parent=None):
        super(UISample, self).__init__(parent)
 
        layout = QVBoxLayout()
        # カスタムUIを作成
        self.view = QTreeView()
        layout.addWidget(self.view)
 
        # てきとうにListに表示するItemの配列を作る
        data = []
        for i in range(5):
            data.append({'parent': 'hogehoge', 'key': 'homuhomu_' + str(i).zfill(3)})
        for i in range(5):
            data.append({'parent': 'fugafuga', 'key': 'homuhomu_' + str(i).zfill(3)})
 
        self.model = TreeModel(data)
        self.view.setModel(self.model)
 
        self.setLayout(layout)
 
        self.view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.view.customContextMenuRequested.connect(self.listContext)
 
    def listContext(self, pos):
 
        menu = QMenu(self.view)
        add = menu.addAction("Add")
        remove = menu.addAction("Remove")
        add.triggered.connect(self.addItem)
        remove.triggered.connect(self.removeItem)
        menu.exec_(self.view.mapToGlobal(pos))
 
    def addItem(self):
 
        index = self.view.currentIndex()
        self.model.addItem(index, "HOGEHOGE")
 
    def removeItem(self):
 
        index = self.view.currentIndex()
        self.model.removeItem(index)
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = UISample()
    a.show()
    sys.exit(app.exec_())