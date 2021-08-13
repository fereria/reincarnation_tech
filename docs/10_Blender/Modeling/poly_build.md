# PolyBuild の使い方

<!-- SUMMARY:PolyBuild の使い方 -->

![](https://gyazo.com/44c670cff895c3994e50e2cecea0363b.png)

PolyBuild は、Mesh を Edit モードで選択したときに Menu に表示される。  
この PolyBuild は、リトポをするときなどに便利な Mesh 追加ツール。

## Mesh を追加する

![](https://gyazo.com/b7c6a82cf6fd51f7780bcf45397c4305.gif)

まず、PolyBuild ツールを起動する。  
Mesh を追加したいときは、Edge にマウスをオーバーさせて Edge をピンク表示にし  
その後、左でドラッグする。  
そうすると、上のように、三角ポリゴンを作成できる。

![](https://gyazo.com/9e2fa464b1a983b4e9dbfcc7a26c908e.gif)

そこから □ ポリゴンを作りたいときは、追加した Edge を「CTRL を押しながら左クリック → 移動」する。  
CTRL を押さないでクリックした場合は、三角ポリゴンが作成される。

![](https://gyazo.com/a117f5482da484b26a2652079d337fb8.gif)

↑ のように Edge と Edge をつなぐようにしたい場合は、Edge をドラッグするのではなく  
つなぎたい Edge の交点にあたる Vertex をドラッグする。  
そうすると、四角 Mesh が作成される。

## 頂点を配置してから Mesh を貼る

まずは、Plane を作成する。

![](https://gyazo.com/56338886651807effd0aaf7fef1f12a9.gif)

次に、Edit モードで頂点表示にし、頂点をすべて選んだあと Vertex を削除する。  
こうすると、Vertex もなにもない空の Mesh データができあがる。

![](https://gyazo.com/6048c012f329ade5b20ea52b7cde6359.gif)

その後、PolyBuild をクリックし  
作成する Mesh の頂点を置くところをクリックする。  
すると、Mesh の貼られていない Vertex のみが作成される。

![](https://gyazo.com/4b1ea9047be53956179b42f2fecd2ee7.gif)

最後に、作成した頂点を選択して F キーを押す。  
すると、選択した Vertex に Face が貼られる。

![](https://gyazo.com/31822f5295807e1cfc337f19961d0c87.png)

頂点が 4 つ以上の場合は、選択した Vertex の多角形が作成できる。

> このツールは、「Shrinkwrap モディファイア」と併用して
> Mesh のリトポをするときに使用すると効果を発揮する。

## 参考

- https://www.youtube.com/watch?v=RFJ2XqnL8I4
