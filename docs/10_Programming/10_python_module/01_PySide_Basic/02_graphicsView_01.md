# GraphicsViewの基本(Sceneをスケールする)

<!-- SUMMARY:GraphicsViewの基本(Sceneをスケールする)-->

GraphicsViewを使用して、色々オブジェクトを配置したり移動したりする方法を  
わりとちゃんと調べることにしました。  
特にMatrix周りとか、View、Scene、Item周りは今まであやふやに使ってたので  
その当たり特に重点的にやっていきたいと思います。

## 基本的な構成

![](https://gyazo.com/6d6bee54ab9c8d0fa4243438b5fb4352.png)

まず、GraphicsViewを使用するときは  
大きく分けて「View」「Scene」「Item」の3つの構造になります。  
PhotoShopに例えると、Viewは新規　とかで作成できるウィンドウ。  
Sceneはレイヤー、 Itemはシェイプで、基本的にはSceneに対してItemを配置し  
それをViewに表示する...という形になります。  
とりあえず、その3つ＋Dialogクラスを作成したサンプルを元にざっくりまとめ。

```python
# -*- coding: utf-8 -*-

import sys
import os
import os.path

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtUiTools import QUiLoader

ZOOM_MIN = -0.5
ZOOM_MAX = 2


class UISample(QtWidgets.QDialog):

    def __init__(self, parent=None):

        super(UISample, self).__init__((parent))

        self.view = NodeView()
        layout  = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.view)

        self.scene = NodeScene()
        self.view.setScene(self.scene)

        item = self.scene.addEllipse(150, 150, 200, 100)
        item.setBrush(QtGui.QBrush(QtGui.QColor('pink')))


class NodeView(QtWidgets.QGraphicsView):

    def __init__(self, parent=None):
        super(NodeView, self).__init__(parent)

    def wheelEvent(self, e):
        delta = e.delta()
        adjust = (delta / 120) * 0.1
        self.set_zoom(adjust)

    def set_zoom(self, value):

        scale = 0.0
        # 今のズーム率 指定外にはならないようにする
        zoom = self.get_zoom()
        if ZOOM_MIN >= zoom:
            if value < 0.0:
                return
        if ZOOM_MAX <= zoom:
            if value > 0.0:
                return
        scale = 0.9 if value < 0.0 else 1.1
        self.scale(scale, scale)

    def get_zoom(self):
        transform = self.transform()
        cur_scale = (transform.m11(), transform.m22())
        return float('{:0.2f}'.format(cur_scale[0] - 1.0))


class NodeScene(QtWidgets.QGraphicsScene):

    sel_item = None

    def __init__(self, parent=None):
        super(NodeScene, self).__init__(parent)

    def mousePressEvent(self, e):
        if e.button() == QtCore.Qt.LeftButton:
            self.sel_item = self.itemAt(e.scenePos(), QtGui.QTransform())
            self.mouse_pos = e.scenePos()

    def mouseMoveEvent(self, e):
        if self.sel_item is not None:
            cur = e.scenePos()
            val = cur - self.mouse_pos
            self.sel_item.moveBy(val.x(),val.y())
            self.mouse_pos = cur

    def viewer(self):
        return self.views()[0] if self.views() else None

    def mouseReleaseEvent(self, e):
        self.mouse_pos = None
        self.sel_item = None


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    a = UISample()
    a.show()
    sys.exit(app.exec_())

```
実行すると、

![](https://gyazo.com/467b0327752953f929ebc3e0ebfd707d.gif)

ホイールで拡大・縮小、○をドラッグすることで動かせます。

## QTransformを使用して拡大縮小

今回のポイントは、「QTransform」を使用して変換を行うところ。  
今まではなんとなく移動したりするのにTransformを使う、、、程度の認識だったのですが  
ViewとSceneの役割考えて使わないと意図しないことになるな...という感じで調べ直しました。  
  
まず、今回の場合はマウスホイールでSceneに置いてあるオブジェクト全部をスケールしたいです。  
そのような処理をしたい場合は、個別のItemをそれぞれポジション弄って大きさ変えて...とか面倒くさいです。  
ので、transformのscaleに数値を入れることで変換を行います。  
  
ItemのPosition　→　TransformのMatrixで変換　→　表示  
  
こんな感じで、PySideのGraphicsItemやView、Sceneには transformを取得・設定できるようになっていて  
その中には「今描画する時の変換用Matrix」が保存されています。  
  
今回の「拡大・縮小」をしたい場合の行列は

![](https://gyazo.com/e6815d68f718d155c3b864041baa7205.png)

この行列で求められます。  
Sx、Syというのが、ベクトル（X,Y,1)を拡大縮小するためのスケール値。  
元のベクトル（X,Y,1）に対して行列をかけ算することで、スケールした結果を取得できます。  
  
現在のスケールを取得している  
```python
cur_scale = (transform.m11(), transform.m22())
```
というのは、

![](https://gyazo.com/0af788717484171b095485438ca2c5e0.png)

PySideのMatrixの各要素を取得する場合、  
ScaleのSxとSyの数値に対応する m11(scaleX) と m22(scaleY) を  
取得すれば良いからです。  
  
この行列はてっきり単位行列かとおもってたのですが、デフォルトはぜんぶ0で  
拡大してれば＋の数値、縮小していればーの数値が入っているようでした。  
なので、0.5なら1.5倍、1.0なら2倍というように、＋1をした数値をかけたその結果の数値で  
拡大・縮小をしているようでした。（不思議）  
  
全体の拡大縮小はサンプルの通りtransformを使用した変換を使用していますが  
ItemをDragしたときに移動するほうは  
あえてTransformではなくItemのポジションを変更するやり方で作成しています。  
  
moveBy(x,y)は、現在位置からの移動量でItemのポジションを動かしているので  
前回のマウスポジションと現在のマウスポジションの差分を  
このmoveByにセットしています。  
  
同じ理屈で、マウスのドラッグでScene全体をスクロールしたいとかも作れそうです。  
  
次は、各座標系ごとのポジション取得とかを調べます。