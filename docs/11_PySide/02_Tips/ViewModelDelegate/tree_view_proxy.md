---
title: TreeViewの中身を正規表現で検索する
---
# TreeViewの中身を正規表現で検索する

![](https://i.gyazo.com/fc6e532b3432ea0e6117821e0c539856.gif)

PySideの各種Viewは、ProxyModelを使用することでリスト内の絞り込み検索を  
追加することができます。  
  
ただ、TreeViewの場合などとくに顕著ですが  
文字列で「絞り込んでほしくないItem」、例としてGroup用の階層などがある場合は  
あえて検索文字で絞り込みたくない場合などもあります。  
  
ので、その辺踏まえてTreeViewで検索をするための構造を作ってみます。

## コード

まずはコード。

<script src="https://embed.cacher.io/d05431800560fe16f8fc16c7022f13f22a0caf47.js?a=f3a85e8a924aa2ce28a5cce93944af1a"></script>

## 解説

まずはQAbstractItemModelを使用してTreeViewとModelを作成します。  

![](https://gyazo.com/84c550cf2f3c2c8d24f1405bdbfd8712.png)

実行するとこんな感じのUIが表示されます。  
  
まず、このTreeViewの場合  
特になにもしない場合 GroupA GroupBも検索で引っかかってしまい  
「テスト」などで検索をしてもなにも表示されなくなってしまいます。  
（親が検索にひっかからないと子は表示されないため）  
  
ので、より細かく検索条件を分岐させる必要があります。  
  
その分岐をするのが、 QSortFilterProxyModelのVirtual関数、「filterAcceptRow」 です。    

  
```python
class TestProxyFilter(QtCore.QSortFilterProxyModel):
 
    def __init__(self, parent=None):
        super(TestProxyFilter, self).__init__(parent)
 
    def filterAcceptsRow(self, row, parent):
        item = parent.internalPointer()
        # 親ItemがGroupItemは、ProxyModelの検索対象にする
        if isinstance(item, GroupItem):
            return super(TestProxyFilter, self).filterAcceptsRow(row, parent)
        # それ以外は検索で消えてほしくないのでTrueにする
        return True
```

filterAcceptsRow関数は、表示するかどうかを各Itemごとに判定して  
表示するかどうかを bool で返します。

![](https://gyazo.com/c25434f14ff0abdcb10efdc47ae39b17.png)

parentとrowを引数として受け取ります。  
これは、表示するかどうか判定したいItemからみた「親」アイテムと、その親から見た「何番目のItemか」  
という情報になります。  
  
このparentはModelIndexになるので internalPointer を使用して実体のItemを取得してしています。  
internalPointerについては以前の [QtCore.QAbstractItemModelを使用したカスタムモデルの作成](custom_model.md)を  
参考にしてください。  
  
で。  
今回の場合は、「親がGroupItem」オブジェクトだった場合は検索対象のItem（TreeItem）なので  
正規表現によるチェックをするために、オーバーライドする前の filterAcceptsRow を実行するようにします。  
それ以外の場合、この場合でいうと GroupItemの場合は  
かならず表示するようにしたいので True を返すようにします。  
  
このようにすると、 GroupItemの場合は  
ProxyModelでどのような条件がきたとしても「絶対表示する」ようになるので  
今回のTreeViewのように特定のItemは判定外にする...といった事が可能になります。  
  
余談ですが、filterAcceptsRow意外にもfilterAcceptsColumn関数もあるので  
条件をRowではなくColumn単位で指定したい場合は  
同じような形でfilterAcceptsColumnで実装すればOKです。
  
### 検索文字列を指定のものにしたい場合

今回のサンプルの場合は列が1つなので問題ないのですが  
例えば列が複数あって、すべてを検索対象にしたい...というケースも発生します。  
  
その場合は、ProxyModelの self.proxymodel.setFilterRole(PROXY_FILTER_ROLE) を使用することで  
検索対象にする文字列を Model側で指定することが出来ます。  

まずは、Proxy側で setFilterRole に対してRoleを指定します。  
Roleは、 UserRole を使用しても良いし、すでに使っている場合は↓のように + 1 したものを  
別途定義するとかでもOKです。  

```python
# Proxyで使用するRoleを定義しておく。
PROXY_FILTER_ROLE = QtCore.Qt.UserRole + 1
# どのRoleをProxyの対象にするのかをセットしておく
self.proxymodel.setFilterRole(PROXY_FILTER_ROLE)
```
  
```python
    def data(self, index, role=QtCore.Qt.DisplayRole):
 
        if not index.isValid():
            return None
 
        item = index.internalPointer()
 
        if role == QtCore.Qt.DisplayRole:
            return item.data(index.column())
        # ProxyModelを使用した検索時の検索対象文字列を返す
        if role == PROXY_FILTER_ROLE:
            # とりあえず同じものを返す
            return item.data(index.column())
        return None
```

そして、Modelの data で、PROXY_FILTER_ROLEだった場合は、検索対象にしたい  
文字列を返すようにしておくと、ProxyModelでの絞り込み対象の文字列を  
カスタマイズすることができます。  
