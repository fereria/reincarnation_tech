---
title: QSettingsを使用してUIの情報を保存する
---
# QSettingsを使用してUIの情報を保存する

UIの各種Widgetの情報を、終了時に保存しておきたい場合はQSettingクラスを使用します。  
サンプルに使用するuiファイルは [こちら](https://snippets.cacher.io/snippet/0021421020ef095007ce)

```python
#!python3
# -*- coding: utf-8 -*-

import sys
import os.path

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtUiTools import QUiLoader

CURRENT_PATH = os.path.dirname(os.path.abspath(sys.argv[0]))


class UISample(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(UISample, self).__init__(parent)

        self.ui = QUiLoader().load(os.path.join(CURRENT_PATH, 'qsettings.ui'))
        self.setCentralWidget(self.ui)

        self.radioButtonSetup()
        self.listViewSetup()

        self.loadSettings()

    def radioButtonSetup(self):

        self.btnGrp = QtWidgets.QButtonGroup()
        self.btnGrp.addButton(self.ui.ABtn, 1)
        self.btnGrp.addButton(self.ui.BBtn, 1)
        self.btnGrp.addButton(self.ui.CBtn, 1)
        self.btnGrp.button(1).setChecked(True)

    def listViewSetup(self):

        self.model = QtCore.QStringListModel()
        self.model.setStringList(['AAA', 'BBB', 'CCC'])
        self.ui.listView.setModel(self.model)

    def closeEvent(self, e):
        self.saveSettings()

    def loadSettings(self):

        setting = QtCore.QSettings("setting.ini", QtCore.QSettings.IniFormat)

        if setting.value(self.ui.comboBox.objectName()) is not None:
            self.ui.comboBox.setCurrentIndex(int(setting.value(self.ui.comboBox.objectName())))
        # LineEditの情報を復帰
        self.ui.lineEdit.setText(setting.value(self.ui.lineEdit.objectName()))
        # TextEditの情報を復帰
        self.ui.textEdit.setText(setting.value(self.ui.textEdit.objectName()))
        # Splitterの位置を復帰
        self.ui.splitter.restoreState(setting.value(self.ui.splitter.objectName()))
        # CheckBoxの選択を復帰
        if setting.value(self.ui.checkBox.objectName()) is not None:
            self.ui.checkBox.setChecked(str2bool(setting.value(self.ui.checkBox.objectName())))
        # RadioButtonの選択を復帰
        if setting.value("grp") is not None:
            self.btnGrp.button(int(setting.value("grp"))).setChecked(True)
        # Tabの選択位置を復帰
        if setting.value(self.ui.tabWidget.objectName()) is not None:
            self.ui.tabWidget.setCurrentIndex(int(setting.value(self.ui.tabWidget.objectName())))
            
        if setting.value(self.ui.listView.objectName()) is not None:
            index = self.model.index(int(setting.value(self.ui.listView.objectName())), 0)
            self.ui.listView.setCurrentIndex(index)
        # GUIの位置を復帰
        self.restoreGeometry(setting.value("geometry"))

    def saveSettings(self):

        setting = QtCore.QSettings("setting.ini", QtCore.QSettings.IniFormat)
        # ComboBoxの選択情報保存
        setting.setValue(self.ui.comboBox.objectName(), self.ui.comboBox.currentIndex())
        # LineEditの情報保存
        setting.setValue(self.ui.lineEdit.objectName(), self.ui.lineEdit.text())
        # TextEditの情報保存
        setting.setValue(self.ui.textEdit.objectName(), self.ui.textEdit.toPlainText())
        # CheckBoxの情報保存
        setting.setValue(self.ui.checkBox.objectName(), self.ui.checkBox.isChecked())
        # RadioButtonの情報保存
        setting.setValue("grp", self.btnGrp.checkedId())
        # Splitterの情報保存
        setting.setValue(self.ui.splitter.objectName(), self.ui.splitter.saveState())
        # Tabの選択情報の保存
        setting.setValue(self.ui.tabWidget.objectName(), self.ui.tabWidget.currentIndex())
        # ListViewの選択情報の保存
        setting.setValue(self.ui.listView.objectName(), self.ui.listView.currentIndex().row())
        # GUIの位置と大きさの保存
        setting.setValue("geometry", self.saveGeometry())


def str2bool(val):
    if val == 'true':
        return True
    return False


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    a = UISample()
    a.show()
    sys.exit(app.exec_())

```

実行結果は

![](https://gyazo.com/e7b3ed08d966e6d15eb4e107ca0ccae1.png)

こんな感じになります。  
  
## 基本的な使い方

まず、情報を保存したい場合は QSettingsオブジェクトを作成します。

```python
setting = QtCore.QSettings("setting.ini", QtCore.QSettings.IniFormat)
```
保存ファイルのフォーマットは、ini以外にもレジストリなども選べますが  
iniで出力するのが色々と楽なので今回はiniを使用します。  
引数の1つめがiniファイルのフルパス＋名前を指定します。  
  
### 保存する

作成したsettingに対して情報を追加する場合は setValue を使用します。  
指定方法は  
setting.setValue( **NAME** ,**VALUE** )  
のようになります。  
  
私は、このNAME部分はオブジェクトの名前を入れるようにしたいので  
self.ui.HOGEHOGE.objectName()  
のように、objectNameを入れていますが、普通に文字列 "hogehoge" のように入れてもOKです。  
この辺はお好みで。  
  
## 保存情報を取得する

保存した情報を取得したい場合は、 setting.value( **NAME** ) を使用します。  
iniに保存された情報がない場合はNoneが帰ってきます。  
また、int型やbool型はstrで帰ってくるので、必要に応じて対応した型にキャストします。  

## わかりにくい復帰方法のWidgetについて補足

いくつかぱっとはわかりにくいWidgetがあるので補足。  
  
### ListViewの場合  
  
ListViewの「選択を変える」コマンドの setCurrentIndex は、  
取得も設定も ModelIndexを使用します。  
そのため、  
```python
setting.setValue(self.ui.listView.objectName(), self.ui.listView.currentIndex().row())
```
保存時は、 indexのrow()でintを取得し保存します。

```python
        if setting.value(self.ui.listView.objectName()) is not None:
            index = self.model.index(int(setting.value(self.ui.listView.objectName())), 0)
            self.ui.listView.setCurrentIndex(index)
```

復帰してListViewを選択する場合は、  
ListViewにセットしているModelの index関数を使用して、ModelIndexを取得して  
その取得したModelIndexをsetCurrentINdexを使用してセットするようにします。  
  
### RadioButtonの場合

radioButtonは、ButtonGroupを使用して選択肢のグルーピングを行います。  
ので、選択情報も  
```python
setting.setValue("grp", self.btnGrp.checkedId())
```
ButtonGroupのcheckedIdを使用して保存します。  
  
復帰させる場合は

```python
        # RadioButtonの選択を復帰
        if setting.value("grp") is not None:
            self.btnGrp.button(int(setting.value("grp"))).setChecked(True)
```

ButtonGroupのbuttonでRadioButtonオブジェクトを取得できるので  
取得したオブジェクトに対してsetCheckedをすればOKです。  
  
### Splitter/Geometry（Window位置）の場合

SplitterやWindow位置は保存用の固有コマンドがあるのでソレを使用して保存します。  
```python
# Splitterの位置保存
setting.setValue(self.ui.splitter.objectName(), self.ui.splitter.saveState())
# UIの位置保存
setting.setValue("geometry", self.saveGeometry())
```
ほぞんされる値はバイナリ値になりますが  
その辺はあまり意識しないでもOKです。

```python
# Splitterの位置を復帰
self.ui.splitter.restoreState(setting.value(self.ui.splitter.objectName()))
# UIの位置復帰
self.restoreGeometry(setting.value("geometry"))
```
復帰するときは restore～を実行することで元に戻せます。

今回はGUIの値の復帰に使用していましたが  
  
```python
setting.setValue('hogehoge','fugafuga')
```
のようにすれば、Widgetの値にかかわらずに値を保存出来るので  
外部ファイルに書いておきたい物がある場合は  
使用すると便利かなぁと思います。
