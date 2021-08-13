# オブジェクトの共有・構造・ユーザーについて

<!-- SUMMARY:オブジェクトの共有・構造・ユーザーについて -->

![](https://gyazo.com/5f6b635f9deee57bd91f9c72667c825b.png)

Blender のシーンないのオブジェクトは、Collection 等に入っていないものであっても  
Blend ファイルに存在する場合がある。

![](https://gyazo.com/e785cd2de8c4c8880abf25d5d4285639.gif)

ViewLayer 表示上では、オブジェクトを移動したとしても  
Maya のグループを移動するのと同じように、移動するだけだが

![](https://gyazo.com/b491120bea11c564adc837b227e283bd.gif)

アウトライナの BlenderFile 一覧から移動すると、同じオブジェクトを、Collection をまたいで  
共用することができる。

Blender は、「Data-Block」と呼ばれる個別のデータによって構成される。  
Data-Block は、BlenderFile に表示されている　 Cameras や Objects などの  
サブフォルダが種類にあたり、その中にあるのがデータになる。

BlenderData の Data-Block を Collection に移動した場合は  
同じ Data-Block を共有している状態なので、Maya でいうところの「インスタンス」のように  
片方を編集すると、もう片方にも変更が反映される。

## 表示状態の共有

![](https://gyazo.com/99255f4ef626dbcbb7ecd23ebb0809dd.gif)

LayerViewer のアイコンを使用すると、オブジェクトの表示状態を切り替えることができる。  
この表示状態は、Maya の親子化時に親オブジェクトを Hide すると子も Hide されるのと同様  
Collection を Hide すると Object も Hide される。

このとき、共有する Object がある状態で片方の Collection を Hide すると  
上の動画のように共有されてるオブジェクト側もいっしょに Hide される。

## シーンをまたいでの共有

![](https://gyazo.com/62a4d65e9371eeaf28e45a3001951bec.png)

Object は、Collection だけではなく Scene をまたいでも共有することができる。

![](https://gyazo.com/a4971cacda1f0bd7fb97e59fbdcfa919.gif)

シーンを切り替えても、オブジェクトは同じ位置にある。  
編集をした場合、もう片方のオブジェクトも更新される。

## 共有するオブジェクトを削除する(Delete と UnLink)

![](https://gyazo.com/acb546a6d2f2b0063a5febf91c6cf456.png)

読み込んだオブジェクトをシーンから削除したい場合は「UnLink」か「Delete」を使用する。  
Unlonk の場合は、あくまでも Blender の Data-Block と Collection の関係を削除するだけで  
Data-Block のデータ本体はそのまま残る。

![](https://gyazo.com/2cdca24adc96fbd03bd719ee66511fd1.gif)

対して、Delete でオブジェクトを削除した場合は  
選択したシーンのオブジェクトだけではなく、別のシーンで読み込んであるオブジェクトも削除される。

## 関係図

![](https://gyazo.com/0489848c4d604a2c3297af1e57072c72.png)

ざっくり整理すると、BlenderFile はこのようになっていて  
→ 部分は親子関係、参照　となっているところが親子化ではなくインスタンス扱いになっているイメージ。

## 孤立データとフェイクユーザー

オブジェクトを Delete せず、Unlink をしていくと
**「どこにも読み込まれていない Data-Block」** ができてしまう。
孤立したデータは、アウトライナの「orphan data」で確認することができる。

![](https://gyazo.com/122f7f4b410865e9c6ace19562b4b23f.png)

ここにある孤立データは、何かしらのタイミングで自動で削除されてしまう。

![](https://gyazo.com/e617d3a840a879e87ec1b124fc472ce8.png)

このようなデータを、意図的に削除させないようにするには「Fake User」を使用する。  
この「User」というのは、Blender を使用しているユーザーというわけではなく  
「オブジェクトの使用者」という意味での User。  
Mesh と Material だと、Mesh は Material の User だし  
オブジェクトがはいっている Collection は、オブジェクトの User になる。

![](https://gyazo.com/5f4020a2ada9e9336a1b70f6e956bc40.png)

フェイクユーザーは、別のオブジェクトで使用されているわけではないが  
データを削除されないようにすることができる。  
FakeUser になっている場合は、OrphanData 上のオブジェクト名の右側に「F」の文字が表示される。

Blender の Data-Block と User、Collection などの関係性は  
いまいちピンときていなかったけれども  
細かく挙動を確認していくと、なんとなく関係性が理解出来た気がする。

## 参考

- http://imoue.hatenablog.com/entry/2016/07/08/222400
