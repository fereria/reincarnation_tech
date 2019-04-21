# Maya2017 以降での PySide の使い方

<!-- SUMMARY: aya2017以降でのPySideの使い方-->

## .ui を .py に変換する

変換する場合は、Maya/bin 　下にある ==pyside2-uic== を使用する。  
ただしそのままではコマンドとして認識されないので  
以下のように変換をする。

```bat
cd /d "C:\Program Files\Autodesk\Maya2018\bin"
mayapy pyside2-uic -o <出力先>\main_ui.py <コンバート前の置き場>\main.ui
cd /d %~dp0
```

## Qt.py のインストール

PySide と PySide2 の違いを吸収するために、　 Qt.py 　モジュールを使用する。

```
pip install qt.py -t <インストール先のPATH>
```

インストールは pip から行うことができる。  
pip の引数として -t ＜ PATH ＞　を使用すれば、指定の site-packages 以下以外にも  
インストールすることができる。

## PySide からのコード書き換え箇所

主な変更は、今まで QtGui に入っていた Widget 関係（Button、Window、Dialog 等）が QtWidgets に移動になった。  
QtGui は、Painter、Brush、Pen、Image、Event のような Widget を作成する上での Core 的な部分が  
QtGui になっている。

## それ以外に書き換えが必要だった箇所

```
QHeaderView.setResizemode -> setSectionResizeMode (Section を追加）
```
