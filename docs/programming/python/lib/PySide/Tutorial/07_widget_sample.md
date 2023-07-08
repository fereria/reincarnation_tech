---
slug: /python/pyside/tutorial/07
title: 基本Widgetを使ってみる(3):ComboBox_基本編
tags:
    - PySide
sidebar_position: 7
---

# 基本 Widget を使ってみる(3):ComboBox\_基本編

![](https://gyazo.com/46ed1187e4b03d1fc1390b851ea50157.png)

複数の項目から 1 つを選びたい時などに使用する  
「POPUP を表示 → 選択する」ができるのが ComboBox。  
今回はその基本的な使い方を説明します。

!!! info
基本のみなので Model-View が絡む物はまたこんど。

## サンプルコード

<script src="https://embed.cacher.io/865138d20d30a842faab429b0c2a49a67a5aff48.js?a=a0dda4a847058f1775f1abbc859c6be7"></script>

実行すると、

![](https://gyazo.com/bf1e8e55b528cfd27a350b110850c2f1.PNG)

このような UI が表示されます。

## 基本的な使い方

### 新規追加

```python
self.combobox.addItems(['abc', 'def', 'gef'])
```

まず、Box のリストに項目を追加します。  
サンプルでは List で指定していますが、  
addItem('hogehoge')ならば、複数ではなく 1 つだけ追加することができます。

### 編集可能にする

デフォルトの場合は、ComboBox は編集不可になっていますが

```python
self.combobox.setEditable(True)
```

Editable を True にすることで、新しい項目をユーザーが追加できるようになります。

### 現在の選択項目を取得する

![](https://gyazo.com/034e8ac96ba26fcf741ef42a4d721f17.png)

現在の項目を選択するには「Current＃＃＃＃」を使用します。  
ComboBox のリストは「Index」を使用してアクセスすることができます。  
その場合は、0 番目からスタートし、下にいくにつれて+1 された Index で  
取得することが出来ます。

直接テキストを取得したい場合は、currentText でテキストを取得することができます。

Index を使用してなにかする例としては  
「現在選択している項目を削除したい」場合など。  
この場合は、removeItem の引数が

![](https://gyazo.com/d1cf903ffee46e606864896dabcc41b0.png)

index になっているので、currentIndex で Index を取得し  
その Index を使用して removeItem を実行することで  
現在の選択状態を削除することができます。

### 指定の文字列を ComboBox から探す

```python
self.combobox.findText(txt)
```

引数の文字列を含む項目を ComboBox 内から探したい場合は  
findText を使用します。  
このコマンドを実行すると、引数で与えた文字列を含む Index を  
しゅとくすることができます。

### 参考

ComboBox
https://doc.qt.io/qtforpython/PySide2/QtWidgets/QComboBox.html#PySide2.QtWidgets.PySide2.QtWidgets.QComboBox.removeItem

ComboBox については Model_View などを使用することで色々と拡張  
することもできますが、今のところは基本的な使い方と言うことでここまで。

今度解説する ListView にくらべて、UI の領域を使わずに  
選択する UI を追加できるので ComboBox はとても便利です。
