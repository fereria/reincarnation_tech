# Data-Block の User,Link,Proxy

<!-- SUMMARY:Data-Block の User,Link,Proxy -->

Data-Block とは、Blender の基本となるデータ単位で、  
**mesh,object,material,texture,node-tree,scenes,text,brush,evenscreen**  
が Data-Block の扱いになる。  
Bone や Vertex は Data-Block ではなく、Scene や Mesh に内包される扱いになっている。  
Blender は、この Data-Block を 1 つの blend シーン内で Link  
あるいは他の blend シーンから Link する形で構成されている。

> Maya 的に言うノードがこの Data-Block？

## User について

![](https://gyazo.com/03241d2d576056a3064a74eef957ec0c.png)

Blender における「ユーザー」とは、Blender をさわっている作業者のことではなく、  
**Data-Block を使用している Data-Block のこと** を指している。  
上のスクショの例だと、Material の User は Cube(Mesh)だし、  
Cube(Mesh)の User は Cube(Object)になる。

User のないデータブロックは、  
いわゆる「未使用ノード」扱いになるため保存されなかったり、  
あやまって削除されてしまうことになる。
ので、間違って削除されないように  
 **「使用してないけど消されない」ようにするため「FakeUser」** を指定する。

## Link

Data-Block は、他の blend ファイルからも Link を作る事が出来る。  
この Link というのが、Maya でいうところのリファレンスに近い機能。

![](https://gyazo.com/81b50b5e608f319f0ea96b3994249601.png)

リファレンスとは違い、シーンをリファレンスするわけではなく、blend 内に含まれる  
Data-Block をそのまま Link することができる。

![](https://gyazo.com/c8c8af5878ccb5679725c31e0d3b6c96.png)

オブジェクト単位、マテリアル単位でも Link を作成できるが  
個別に Link を作るのが面倒な場合は、Collection を作成してから  
その Collection を Link してあげれば、複数のオブジェクトをまとめて Link することができる。

Link で読み込んだデータは、鎖のようなマークが付く。

![](https://gyazo.com/6e43ec327032c4d11f04e52d9e6cb087.png)

この状態だと、シーン内では一切編集することが出来ない（移動なども）  
背景などのようなデータを読み込む場合は問題ないが、  
モデルデータを Link して共有したい場合はこのままだと NG なので「プロクシ」を作成する。

![](https://gyazo.com/e964afed551483ae871cfe36acb8655a.png)

編集したいオブジェクトを選択して、Object>Relations ＞ Make Proxy... をクリック。

![](https://gyazo.com/f9325efd760df47d1c4302f4747b938a.png)

クリックすると、↑ のようにプロクシを作成する前のオブジェクトは残したまま  
\_proxy と言う名前のオブジェクトが追加される。

![](https://gyazo.com/9b88c293b900f43bf20dad7a30191404.png)

Link しただけの場合は、
移動やスケールなどの変更、モディファイアの使用もできないが  
プロクシを作成した後ならば移動もできるし、  
モディファイアも使用できる。

![](https://gyazo.com/5680bf692511567067cbb2bdf1e95e53.png)

試しに Link 元を編集してから、再度シーンを開き直すと

![](https://gyazo.com/aab4a9b0f7db06fe89a5ebdedacbc19a.png)

Link 元の編集を適応した状態で、プロクシで変更した情報が適応される。

> このプロクシは、オブジェクト単位で作成する必要がある。
> 1 つのモデルが複数のオブジェクトで作成されている場合は
> 編集したい数分プロクシを作成する必要がある？
> （Collection を選んで Proxy を作成した場合、
> 押したあとに Collection 内のオブジェクトを選択するウィンドウが表示される)

## 一部リンクを残し Append

Proxy 作成以外で Link したオブジェクトを編集したい場合は、「MakeLocal」をする。

![](https://gyazo.com/8623cdf89e7d408931b569f31a20a205.png)

この MakeLocal を押すと、選択したオブジェクトのみ読み込むことが出来る。  
例えば Object を選択し MakeLocal すると、Object は Link からはずれるが  
Material や Mesh の Link は残ったままになる。

> 共通モデルを使用してアニメーション、モデルはあとで差し替え...のようなフローを作りたい場合は、
> プロクシ使って編集するようなフローが一般的なのか...？
