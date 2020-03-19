---
title: PySideでStyleSheetを使って編集する(1)
---

PySideは、StyleSheetを使用して見た目を調整することができます。
今回は基本的な書き方（作り方）です。

## 基本書式

まず、PySideでStyleSheetを使用する場合は、

```css
QGroupBox {
    margin: 10px;
    padding 15px;
    border 1px solid #ccc;
}
```
この QGroupBox の部分がWidgetsの名になっていて、その中に書かれている内容が
CSSで指定することができるパラメーターです。

このようなフォーマットの文字列を
```
widgetObj.setStyleSheet("QGroupBox{～～～～}")
```
WidgetsのsetStyleSheetを使用してセットします。


![](https://gyazo.com/2df42ad721ca76ffca7ab71bec2cf425.jpg)

その場合、たとえば赤で囲っている所にStyleSheetを適応した場合、子にあるおなじタイプのWidget
（このばあい同じGroupBox）にもStyleSheetの編集結果が適応されます。

## 指定のWidgetsのみに適応したい

では、子のWidgetsには反映させずに自分自身にのみセットしたい場合はどうすればいいかというと

```css
QGroupBox#groupBox{
～パラメータ～
}
```
このように、#の後ろにWidgetのObject名を指定することで
指定のWidgetsのみStyleSheetを指定することができます。

## 外部ファイののStyleSheetを読み込む

setStyleSheetを使用してセットするのは良いですが
それだとまとめてStyleSheetを指定したり
StyleSheetの使い回しができません。

ので、その場合は、

```css
QGroupBox#groupBox{
  margin: 10px 10px 30px;
  padding: 15px;
  border: 5px solid #ccc;
}
QGroupBox#groupBox_2{
    border: 2px solid blue;
}
QGroupBox#groupBox_3{
    border: 2px solid red;
}
QGroupBox#groupBox_4{
  margin: 1px 1px 1px;
  padding: 5px;
  border: 5px solid green;
}
```
このような style.css ファイルを作り、
```python
win = toolUI()
with open("style.css","r") as f:
    win.setStyleSheet("".join(f.readlines()))
```
このように、一番親にあたるWindowに対して open で読み込んで、
setStyleSheetでセットすればOKです。