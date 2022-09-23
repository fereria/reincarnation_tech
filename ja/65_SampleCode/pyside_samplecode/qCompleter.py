# -*- coding: utf-8 -*-

import sys
import os.path
import re
from PySide2.QtWidgets import (QApplication,
                               QDialog,
                               QTreeView,
                               QVBoxLayout,
                               QItemDelegate,
                               QStyle,
                               QLineEdit,
                               QVBoxLayout,
                               QCompleter,
                               QShortcut)
from PySide2.QtCore import (QModelIndex,
                            Qt,
                            QAbstractItemModel,
                            Signal,
                            QStringListModel)

from PySide2.QtGui import (QBrush,
                           QColor,

                           QKeySequence,
                           QCursor)

from pxr import Usd, Sdf

sample_usd = "D:/work/usd_py36/usd/tree_view_sample.usda"


class TestView(QTreeView):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setDragEnabled(False)
        self.setAcceptDrops(True)

        self.setDragDropOverwriteMode(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            super().dragEnterEvent(event)

    def dragMoveEvent(self, event):

        if event.mimeData().hasUrls():
            # USふファイルのDDか確認
            urls = [x.toLocalFile() for x in event.mimeData().urls()
                    if os.path.splitext(x.toLocalFile())[1] in ['.usda', '.usd', '.usdc']]
            index = self.indexAt(event.pos())
            if index.isValid() and len(urls) > 0:
                QApplication.setActiveWindow(self)
                self.setDropIndicatorShown(True)
                event.accept()
            else:
                event.ignore()
        else:
            super().dragMoveEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            index = self.indexAt(event.pos())
            for url in urls:
                file = url.toLocalFile()
                self.model().addUsdReference(file, index)
                self.expandAll()
            event.accept()
        else:
            super().dropEvent(event)
        self.setDropIndicatorShown(False)


class UISample(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.resize(600, 400)

        self.view = TestView()
        self.edit = QLineEdit()
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        layout.addWidget(self.edit)
        self.setLayout(layout)

        self.model = UsdStageModel(sample_usd)
        self.view.setModel(self.model)

        self.delegate = TableDelegate()
        self.view.setItemDelegate(self.delegate)

        self.completer = CustomQCompleter(self.edit)
        self.completer.setModel(self.model)
        self.edit.setCompleter(self.completer)

        QShortcut(QKeySequence(Qt.Key_Tab), self, self.showSearchEdit)

    def showSearchEdit(self):

        popup = PopupSerchEdit(self)
        popup.show()


class CustomQCompleter(QCompleter):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setCompletionMode(self.PopupCompletion)
        self.setCaseSensitivity(Qt.CaseInsensitive)

    def splitPath(self, path):
        return re.sub("^/", "", path).split("/")
        # super(CustomQCompleter, self).splitPath(path)

    def pathFromIndex(self, index):
        # SdfPatにに置き換える
        item = index.data(Qt.UserRole)
        return item.data(2)


class PrimItem(object):

    def __init__(self, prim=None, parentItem=None):
        self._prim = prim
        self._parentItem = parentItem
        self._childItems = []

    def addChild(self, item):
        self._childItems.append(item)

    def getChild(self, row):
        if row <= len(self._childItems):
            return self._childItems[row]
        return None

    def getChildren(self):

        return self._childItems

    def getParentItem(self):
        return self._parentItem

    def getPrim(self):
        return self._prim

    def getFontColor(self):

        if self._prim.HasAuthoredReferences():
            return QColor(255, 121, 0)
        else:
            return QColor(0, 0, 0)

    def row(self):
        if len(self._parentItem.getChildren()) == 0:
            return 0
        return self._parentItem.getChildren().index(self)

    def data(self, column):

        if column == 0:
            return self._prim.GetName()
        if column == 1:
            return self._prim.GetTypeName()
        if column == 2:
            return str(self._prim.GetPath())
        if column == 3:
            if self._prim.HasAuthoredReferences():
                # print(self._prim.GetName())
                for f in self._prim.GetPrimStack():
                    ref = f.referenceList.prependedItems
                    if len(ref) != 0:
                        return ref[0].assetPath
                return ""
            else:
                return ""


BACKGROUND_BASE = QColor(255, 255, 255)
BACKGROUND_SELECTED = QColor(204, 230, 255)
BACKGROUND_FOCUS = QColor(240, 248, 255)


class TableDelegate(QItemDelegate):

    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter, option, index):

        data = index.data(Qt.UserRole)

        bgColor = BACKGROUND_BASE
        if option.state & QStyle.State_Selected:
            bgColor = BACKGROUND_SELECTED
        if option.state & QStyle.State_HasFocus:
            bgColor = BACKGROUND_FOCUS

        brush = QBrush(bgColor)
        painter.fillRect(option.rect, brush)

        painter.setPen(data.getFontColor())
        painter.drawText(option.rect, Qt.TextWordWrap, data.data(index.column()))


class UsdStageModel(QAbstractItemModel):
    header = ["PrimName", "Type", "SdfPath", "ReferencePath"]

    def __init__(self, usdPath: str, parent=None):
        super().__init__(parent)

        # self.setupModelData(data.split('\n'), self.rootItem)
        self.stage = Usd.Stage.Open(usdPath)

        self.createModelTree()

    def createModelTree(self):

        # {SdfPath:Item}
        self.rootItem = PrimItem(self.stage.GetPrimAtPath("/"), None)
        self.prims = {Sdf.Path("/"): self.rootItem}
        for prim in self.stage.Traverse():
            parentPath = prim.GetParent().GetPath()
            item = PrimItem(prim, self.prims[parentPath])
            self.prims[parentPath].addChild(item)
            self.prims[prim.GetPath()] = item
        self.layoutChanged.emit()

    def columnCount(self, parent):
        return 4

    def data(self, index, role):

        if not index.isValid():
            return None

        item = index.internalPointer()

        if role == Qt.DisplayRole:
            return item.data(index.column())
        if role == Qt.UserRole:
            return item
        if role == Qt.EditRole:
            return item.data(0)
        return None

    def flags(self, index):

        if not index.isValid():
            return Qt.NoItemFlags
        return Qt.ItemIsEnabled | Qt.ItemIsDropEnabled | Qt.ItemIsDragEnabled | Qt.ItemIsSelectable

    def index(self, row, column, parent):

        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.getChild(row)

        if childItem:
            index = self.createIndex(row, column, childItem)
            return index
        else:
            return QModelIndex()

    def parent(self, index):

        if not index.isValid():
            return QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.getParentItem()

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
        return len(parentItem.getChildren())

    def headerData(self, section, orientation, role):

        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[section]

    def supportedDropActions(self):
        return Qt.MoveAction | Qt.CopyAction

    def addUsdReference(self, usdPath, index):

        item = index.data(Qt.UserRole)
        prim = item.getPrim()
        path = prim.GetPath()

        # DDしたUSDからDefaultPrimを取得
        ref_stage = Usd.Stage.Open(usdPath)
        defPrim = ref_stage.GetDefaultPrim()
        def_prim = self.stage.DefinePrim(path.AppendChild(defPrim.GetName()))
        def_prim.GetReferences().AddReference(usdPath)

        self.createModelTree()


class PopupSerchEdit(QDialog):

    send = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowFlags(Qt.Popup)
        self.setAttribute(Qt.WA_TranslucentBackground)

        layout = QVBoxLayout(self)

        self.edit = QLineEdit(self)
        layout.addWidget(self.edit)
        self.setLayout(layout)
        # 現在のマウス位置にGUIを出す
        size_x = 200
        size_y = 50
        pos = QCursor().pos()
        self.setGeometry(pos.x() - size_x,
                         pos.y() - size_y,
                         size_x,
                         size_y)

        self.edit.returnPressed.connect(self.Submit)
        self.edit.setFocus()

        # SimpleなAutoCompleteを作る
        comp = QCompleter(self)
        comp.setModel(QStringListModel(['hogehoge', 'fugafuga', 'foo', 'bar']))
        # 全部表示: UnfilteredPopupCompletion
        # Inlineに候補を表示: InlineCompletion
        # POPUP表示: PopupCompletion
        comp.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.edit.setCompleter(comp)

    def Submit(self):
        # Enterしたら文字をEmitして閉じる
        self.send.emit(self.edit.text())
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    QApplication.setFallbackSessionManagementEnabled(True)
    a = UISample()
    a.show()
    sys.exit(app.exec_())
