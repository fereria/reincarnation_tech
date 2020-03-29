---
title: グラデーションピッカーを作る
---

## 動機

<blockquote class="twitter-tweet"><p lang="ja" dir="ltr">あと前に見て、やってみたいなと思ったのが、SDのグラデーションスポイトの実装なんですが、これってPySideで出来ますかね？<a href="https://t.co/daZeJ5huCC">https://t.co/daZeJ5huCC</a></p>&mdash; 大翔士 (@d658t) <a href="https://twitter.com/d658t/status/1240625451636101120?ref_src=twsrc%5Etfw">March 19, 2020</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

大翔士さん主催の PySide 勉強会があったので、
その発表ネタに SD にあるというグラデーションピッカーがほしいという話があったので
PySide で作ってみました。

## 挙動

まずは SD を起動してどういう結果がほしいのかを確認してみます。

![](https://i.gyazo.com/17466eae3e54e262c52f21d56b619878.gif)

まず、グラデーションを選択する　を実行するとピックモードになり
ドラッグ中の色を取得して、移動距離に応じて Color が 0-1 位置に配置されるようになります。

どの程度のしきい値でコントロールポイントを配置するかがグラデーションスポイトの制度という形で
設定できるようになっています。

ということで、今回のスクリプトも

1. マウスのドラッグ中の色を
2. しきい値に応じて、マウスの移動距離に応じて配置して
3. 0-1 の位置と　色の配列を返す

ようにします。

## コード

全コードはそこそこ長いので以下参照。
https://snippets.cacher.io/snippet/89349b71822dedc44c70 Python3 系
https://snippets.cacher.io/snippet/c326b9e4b9a245578a47 DCC ツール用に Pick 部分を 2 系で書き直したもの
https://snippets.cacher.io/snippet/2c7496d1dbbdc093033c 大翔士さんによる修正版

## 説明

というわけで中でやっていることの説明をば。

解説部分は Python2 系にて書いておきます（※3/29 修正）

まず、今回のような画面に対して何かを書いたりするような処理を作りたい場合
PySide の「mouseMoveEvent」を使用してイベントをしゅとくすれば良さそうですが
PySide のイベントは Window 外だと Event を拾ってくれません。
（画面外でもイベントを拾う方法は調べてもわからず...）

というわけでこれをどうやって処理したらよいかというと、

[PySide で範囲スクリーンショットを作る](04_screen_shot.md) でやったのと同じ処理で作ることができます。

```python
class ColorPick(QMainWindow):

    getGradation = Signal(list)

    def __init__(self, parent=None):
        super(ColorPick,self).__init__(parent)

        self.setMouseTracking(True)

        self.screen = QApplication.primaryScreen()
        self.originalPixmap = self.screen.grabWindow(QApplication.desktop().winId())
```

それが、Picker ツール部分で
スクリーンを取得し、現在の ScreenShot を撮影する処理をしています。

あと、今回はマウスの動きをトラッキングしたいので setMouseTracking(True) をいれておきます。

```python
    def paintEvent(self, event):

        painter = QPainter()
        painter.begin(self)
        rectSize = QApplication.desktop().screenGeometry()
        painter.drawPixmap(rectSize, self.originalPixmap)
```

そのスクリーンショットを、paintEvent 内で Window 内に描画して

```python
    def showPick(self):
        # ボタンを押すと、ピッカーGUIが全画面に表示される
        a = ColorPick(self)
        a.showFullScreen()
        a.getGradation.connect(self.setGradationColor)
```

そのスクリーンショットを描画した Window を全画面表示します。

こうすることで、マウスのイベントを取得しつつ画面に対してなにかするということが
可能になります。

注意点としては、スクリーンキャプチャは更新していないので、ColorPick を全画面表示した段階で
ウィンドウの表示は更新されない（静止画扱い）になります。
このあたりは書き方次第で回避策はあるかもしれません。

これで、画面のドラッグをする部分の下準備ができました。

### マウス位置の色を取得する

```python
    def getCurrentColor(self, pos):
        x = pos.x()
        y = pos.y()
        return self.originalPixmap.toImage().pixelColor(x, y)
```

準備ができたので、実際に色の取得をしていきます。
色を取得するには、上の画像描画用に取得した ScreenShot のイメージを使用します。
Pixmap のままだとピクセルカラーは取得できないので
toImage で QImage にしてから現在のピクセルカラーを取得します。

### マウスの移動中の色を取得する

色の取得ができるようになったので、マウスの挙動を取得してきます。
取得するには
mousePressEvent mouseMoveEvent mouseReleaseEvent
この３つでそれぞれの処理を作ります。

#### mousePressEvent

まずはここから。Press すると、色の取得を開始したいので
処理を開始できるようにフラグをたてて開始位置の色を取得します。

```python
    def mousePressEvent(self, event):
        self.isDrag = True
        self.currentPos = QCursor().pos()
        # クリックしたタイミングを0としてグラデーションをピックする
        color = self.getCurrentColor(self.currentPos)
        self.startColor = (color.red(), color.green(), color.blue())
```

グラデーションの位置を決めるのにはマウスの移動量の取得が必要なので
その計算用に今のマウスポジションを取得しておきます。

#### mouseMoveEvent

```python
    def mouseMoveEvent(self, event):
        # GradColorを処理する
        if self.isDrag:
            pos = QCursor().pos()
            line = QLineF(QPointF(pos), QPointF(self.currentPos))
            # マウスの移動距離を保存（あとで正規化）
            self.totalLength += line.length()
            color = self.getCurrentColor(pos)
            currentColor = (color.red(), color.green(), color.blue())

            self.gradation.append([self.totalLength, currentColor])

            self.currentPos = pos
            self.repaint()
```

MoveEvent が今回のメイン処理です。
まず、ドラッグ中のみの実行なので isDrag = True のときのみ処理をさせます。
そして、前のマウスポジションと今のマウスポジションの移動量を計算しておきます。

ここではとりあえず全部の値を入れておき、あとで同じ色だった場合は外す処理を行います。


```python
def colorDifference(src, dst):
    # 超シンプルな色差を求める関数
    rd = (src[0] / 255.0) - (dst[0] / 255.0)
    gd = (src[1] / 255.0) - (dst[1] / 255.0)
    bd = (src[2] / 255.0) - (dst[2] / 255.0)
    return math.sqrt(rd * rd + gd * gd + bd * bd) / math.sqrt(3)
```

色の差の取得は、今回はシンプルに距離に応じて 0-1 を返すようにしました。

#### mouseReleaseEvent

最後にマウスをはなしたときに今まで記録した内容をシグナルで返す処理を追加します。

```python
    def mouseReleaseEvent(self, event):

        self.isDrag = False
        # 1つ目は0なので、そのまま取り出す
        retVal = [[0, self.startColor]]

        # 正規化
        for i, item in enumerate(self.gradation):
            if i != 0 and i != len(self.gradation) - 1:
                prevDiff = colorDifference(item[1], self.gradation[i - 1][1])
                nextDiff = colorDifference(item[1], self.gradation[i + 1][1])
                if prevDiff > self.threshold or nextDiff > self.threshold:
                    retVal.append([item[0] / self.totalLength, item[1]])
            else:
                retVal.append([item[0] / self.totalLength, item[1]])
        # マウスを話したらSignalで結果を返す
        self.getGradation.emit(retVal)

        self.close()
```

今回はグラーデーション位置は 0-1 で取得したいので、マウスの総移動量で各
ポイントの移動量を割って 0-1 に値が収まるようにします。

更に、グラデーションカラーの調整で前後の色を見て、色の差が大きい場合のみreturnを返すようにすることで
SD のグラデーション的な挙動をつくることができるようです。（大翔士さんの修正版に変更、ありがとうございます！）

最後に、その結果を Signal で送信して、Window を閉じて終了です。

これで、

```
[[0,(0,0,0)],[0.5,(1,1,1)]]
```

こんな感じの配列を、Signal で取得できるようになりました。

### 現在のピクセル色をマウス位置に表示する

![](https://gyazo.com/8dc4ccdef266e61a3c0640d05d07a158.png)

メインの処理はできましたが、ピック中の色がわかるように
マウス位置に色を表示できるようにします。

```python
    def paintEvent(self, event):

        painter = QPainter()
        painter.begin(self)
        rectSize = QApplication.desktop().screenGeometry()
        painter.drawPixmap(rectSize, self.originalPixmap)

        x = QCursor().pos().x()
        y = QCursor().pos().y()
        offset = 30

        if self.isDrag:
            pen = QPen(Qt.red, 7)
            painter.setPen(pen)
            painter.drawPoint(x, y)

            color = self.getCurrentColor(QCursor().pos())
            painter.setBrush(color)
            pen = QPen(Qt.black, 1)
            painter.setPen(pen)
            rect = QRect(x + offset, y + offset, 20, 20)
            painter.drawRect(rect)

            painter.setFont(QFont(u'メイリオ', 8, QFont.Bold, False))
            pen = QPen(Qt.white, 1)
            painter.setPen(pen)
            painter.drawText(x + offset + 30, y + offset + 17,
                             "RGB({},{},{})".format(color.red(), color.green(), color.blue()))

        painter.end()
```

描画部分は、まずスクリーンショットを全画面に表示させて
現在のマウス位置基準で右下あたりに文字と色の矩形を表示させるようにしました。

とりあえずこれで必要な配列はできたので、Houdini でツールをつくるなりすれば OK ですが
それだとわかりにくかったのでグラデーションの GUI をつくってみました。

```python
class Gradation(QGraphicsScene):

    def __init__(self, parent=None):
        super(Gradation,self).__init__(parent)

        self.colorList = []

    @property
    def width(self):
        return self.sceneRect().width()

    @property
    def height(self):
        return self.sceneRect().height()

    def drawBackground(self, painter, rect):

        grad1 = QLinearGradient(0.0, 0.0, self.width, 0.0)
        for ratio, color in self.colorList:
            grad1.setColorAt(ratio, QColor(*color))
        painter.setBrush(QBrush(grad1))
        painter.drawRect(0, 0, self.width, self.height)

    def setColor(self, colorList):

        self.colorList = colorList


# グラーデーション確認用GUIを作る
class UISample(QDialog):

    def __init__(self, parent=None):
        super(UISample,self).__init__(parent)

        self.resize(350, 100)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.scene = Gradation()
        self.scene.setSceneRect(0, 0, 300, 50)

        self.view  = QGraphicsView(self.scene, self)
        layout.addWidget(self.view)

        btn = QPushButton("Pickする")
        layout.addWidget(btn)

        btn.clicked.connect(self.showPick)

    def showPick(self):
        # ボタンを押すと、ピッカーGUIが全画面に表示される
        a = ColorPick(self)
        a.showFullScreen()
        a.getGradation.connect(self.setGradationColor)

    def setGradationColor(self, colorList):

        self.scene.setColor(colorList)
        self.view.repaint()
```

こちらのコードは、もちおさんが速攻作ってくれた https://github.com/mochio326/GradationWidget  
こちらを参考に、グラデーション表示部分だけ作ってみました。

<blockquote class="twitter-tweet"><p lang="ja" dir="ltr">若干挙動が怪しい気もするけど、明日のはここまで... <a href="https://t.co/qCSZ8dzrvb">pic.twitter.com/qCSZ8dzrvb</a></p>&mdash; あんどうめぐみ@れみりあ (@fereria) <a href="https://twitter.com/fereria/status/1243533080154918914?ref_src=twsrc%5Etfw">March 27, 2020</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

できあがった結果がこちら。

## はまったところ

今回の実装ではいくつかのはマリポイントがありました。

### ColorPickWindow の継承元をなににするか

PySide の GUI を作る場合は QMainWindow QDialog QWidget のいずれかを継承して
GUI を作るかと思います。

が、今回の ColorPick で全画面化したい場合は QMainWindow である必要がありました。

QDialog の場合は、全画面化したとしてもタスクバーは消えてくれないため
正しい挙動にならず、
QWidget は一応全画面化できるものの、parent で親 Widget をしてしまうと
全画面化したいのに、親の Window 内以上にできず
うまく起動できませんでした。

## まとめ

というわけで、こんなかんじでピックツールができました。
個人的なポイントはスクリーンショットを全画面に表示するところで
ここがつかめていれば、あとは画面の QPixmap を取得して処理をすれば OK なので
実装方法はわかりやすいのかなと思います。

<blockquote class="twitter-tweet"><p lang="ja" dir="ltr">PySide勉強会のあんどうさん(<a href="https://twitter.com/fereria?ref_src=twsrc%5Etfw">@fereria</a>)の発表のおかげで、HoudiniにSubstance Designerのグラデーションスポイトを実装出来たよー！<br>詳しい実装方法についてはあんどうさんが記事にしてくれるそうです。<a href="https://twitter.com/hashtag/Houdini?src=hash&amp;ref_src=twsrc%5Etfw">#Houdini</a> <a href="https://twitter.com/hashtag/PySide?src=hash&amp;ref_src=twsrc%5Etfw">#PySide</a> <a href="https://t.co/KqPeaNfxDd">pic.twitter.com/KqPeaNfxDd</a></p>&mdash; 大翔士 (@d658t) <a href="https://twitter.com/d658t/status/1243855355030974465?ref_src=twsrc%5Etfw">March 28, 2020</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

そして終わってすぐ早速 Houdini に入れてくれました。
個人的にはこの Houdini への追加方法が知りたいです。

## 追記

Python3 で書いてましたがそれだと DCC ツール的には混乱をうむので、記事は 2 系にしておきました。

変更点は

- super().**init**(parent) のように書いてたところを Python2 系に戻す
- f"{val},{val2}" のようにフォーマットを書いてたのを "".format(val,val2) にした
- アノテーション書いてたところを消した func(val:Type) -> func(val)
  です。

あとは、ピックする部分はもうちょい調整が必要なので、引き続き検証かなー

## 追記２ 03/29 19:30

大翔士さんがさらに手を入れてより SD に近いピッカーに進化しました。
素晴らしい！！

https://snippets.cacher.io/snippet/2c7496d1dbbdc093033c
