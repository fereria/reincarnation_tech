# Blender から Maya にデータを移植する

<!-- SUMMARY:BlenderからMayaにデータを移植する -->

## FBX でシーンを持ち込み

### Material まわり

![](https://gyazo.com/3345ddbc33f0dccb41fc47e1c4cd0373.png)

Maya にデータを持ち込みしたい場合は  
FBX を使用するのが良い。

File→Export→FBX 　を選択すると  
現在のシーンを FBX で出力することができる。  
出力する場合、Light や Camera もほぼそのまま持って行くことが出来る。

Mesh データはほぼほぼ行くようだが、問題が発生するのは Material まわり。  
Blender で基本となる Principled BSDF がアサインされている場合だと  
Maya 的には Phong に置き換わる。

Color などの情報は行くようだが  
ただし細かい値は持って行くことは出来ない。  
ノードエディタでのコネクションは、Image 等が接続されている場合は  
Maya 側でも File ノードが生成されるものの  
RGB や Noise のようなノードは持ち込むことはできない。

![](https://gyazo.com/fae1b2592f1615203c71737770ea9e9a.png)

このように Face 単位でマテリアルをアサインしている場合は

![](https://gyazo.com/60023c2c3b16466de46becbeb399f60e.png)

アサイン情報は持ち込むことが出来る。

### Joint まわり

![](https://gyazo.com/afb2ef477e6f73d3e785cbddeaa48e83.png)

シンプルな Armature と Bone を作成し、Export する。

![](https://gyazo.com/b2c9448a1d48649a53d2ba35914f5d45.png)

Maya 側で開くと、なぜか末端 Joint の Radius が吹っ飛ぶが

![](https://gyazo.com/c6dd3bb749bc7b0f12c2c6e42afaf2e1.png)

Radius を正しくすると、問題なくもっていけてるのがわかる。

![](https://gyazo.com/742a9f65f65904d90f99c9d3abafd9f1.png)

Armature がロケーターに置き換わった状態で、親子階層はそのままになる。  
名前は Bone の名前＋ FBX にしたときに付いてくる文字列。

![](https://gyazo.com/5966286bdc0ffa6f02457cab98691f2d.png)

注意点は、Blender は、Zup 　 Maya は Yup という違いがある。  
そのため、Blender 上は「Zup」で作っている場合でも

![](https://gyazo.com/89d86432065b76c905d8e6c65da895a3.png)

Maya に持ち込むと、Yup に置き換わる。

### Maya にはないオブジェクト

LightProbe や Lattice のような、Blender 特有のオブジェクトがあった場合  
Null などができるわけでもなくそもそも **「なにも持ち込まれない」**  
Empty オブジェクトのうち、Locator 形状以外の場合は  
位置は保持したまま、形状はデフォルトの Locator の形状に置き換わる。

## 構造に関わるもの

### モディファイア・コンストレインなど

IK や Constraint のようなものも、基本持ち込むことは出来ない。

## 親子化

Blender の

![](https://gyazo.com/ca3bb9becd9ca464e733739b5747304e.png)

リレーションに指定がある場合

![](https://gyazo.com/f3baf547aa73b7db1473fbe29aad2e70.png)

Maya 上では親子化が再現される。
