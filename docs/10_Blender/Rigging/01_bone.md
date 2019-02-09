# Bone の調整・設定

<!-- SUMMARY:Boneの調整・設定 -->

Armature で作成した Bone の調整をする。

## Bone の構成

Blender の Bone は、Maya とは違い、Bone と Head とう構造になっている。

![](https://gyazo.com/4bf14bf80f6d6eb2f096b8c81923e518.png)

Bone の丸い部分が Head で、その間の四角錐的なオブジェクトが Tail。  
開始位置の Head が Root、終わり部分が Tip と言う名前。
Pose モード時に Bone を選択した場合は、Tail 部分と Tip の Head が選択される。  
Head が選択・追加できるのは Edit モード時である。

## Layers を変更する

Blender には、Bone 専用の Layers が存在する。

![](https://gyazo.com/39a78aa86520fe016da4e5e5b9c300bb.png)

Armature の設定内の Layers が、その表示を切り替えるためのボタンになっている。  
デフォルトは、左上の Box に Bone が入っている。

![](https://gyazo.com/80393fc74633b78c81fd3aab4d88edaf.png)

Layer を変更したい Bone を選択し、 m を押すと、Change Bone Layer 画面が表示される。  
変更したい Layer のボタンをクリックすると

![](https://gyazo.com/187259556a6fbaba5e61d0e89551f8f5.png)

レイヤーから Joint がなくなり

![](https://gyazo.com/0ec72cce84efac466f4111217c1488aa.png)

移動先の Layer に Bone が追加される。

# BoneGroup を作成する

Armature の設定内の BoneGroups で  
Bone をグルーピングすることができる。  
これは「Pose モード」時のみ使用することができる。(Pose モード以外ではボタンが押せない)

![](https://gyazo.com/9d3f9cedc59567c12d40c8a93a5bcdf4.png)

まず、画面右上にある「＋」ボタンを押してグループを追加する。  
そのグループに追加したい Bone を選択し、「Assign」を押す。  
Color で好きな色を選択することで

![](https://gyazo.com/fc1ab8626ae3367c64015875d220dd9e.png)

グループごとに、Bone の色を変更することができる。

![](https://gyazo.com/5e958044248c501b80bce4b6900cd994.png)

BoneGroup は、Outliner 上でも切り替えすることができる。

# Pose Library

その名の通り、現在のポーズを保存することができる。

![](https://gyazo.com/d0c95e427669cf28f2481bb06c56dc17.png)

Armature 内の PoseLibrary で「ライブラリ」を追加する。  
ライブラリが、ポーズデータをまとめるグループの役割をしている。

![](https://gyazo.com/da96b1b6d5a4dea256b85f2a557525fb.png)

増やすにはここの用紙のようなアイコン（左から２つめ）をクリックする。  
名前は自由に変更する。

次に、ポーズを作成する。
作成したら　 Shift+L を押して Pose の追加メニューを出す。

![](https://gyazo.com/8c6b98126371d09e628f3aaca2ec3d0c.png)

新しく Pose を追加するのなら「Add New」を押す。
既存のものと置き換えたい場合は「Replace Exist」を選択する。

![](https://gyazo.com/7820505cec0dd22d67e818293249b942.png)

登録したポーズを使用したい場合は、ポーズを選択して虫眼鏡のようなアイコンを押すと  
選択したポーズに切り替えることが出来る。
ただし、ポーズが適応されるのは「選択されているボーンのみ」（えぇ...

![](https://gyazo.com/2032299044cfed9ac2e576b3303e6ec2.gif)
