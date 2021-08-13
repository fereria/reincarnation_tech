# Blender のマテリアルノードを作成する（2）

<!-- SUMMARY:Blender のマテリアルノードを作成する（2） -->

前回で基本的な構造ができたので、  
次にその中を拡張して、ノードの中にパラメーターを追加したりしてみます。  
  
## NoteNodeを作る

今回はプラグなどを作らないでもOKなのと  
比較的作りやすそうだったので、メモを書けるノードを作って見ることにします。  
  
コードは、  
https://github.com/ly29/GenericNote  
このaddonを使用しました。  
このプラグインが2.78までなので2.8だと使用出来ないので  
コードをマネしつつBlenderでのプラグインの作り方を  
理解していきます。  
  
## ノードクラスを拡張する

まずは、ノードクラスを拡張します。  
注意しないと行けないのは「RNA」プロパティと呼ばれる構造と  
UIにウィジェットというかパーツを追加する方法の2つです。  
  
まずコード。

```python
TW         = textwrap.TextWrapper()
TEXT_WIDTH = 3

class MyCustomNode(Node):

    bl_idname = 'SimpleCustomNode'
    bl_label  = "Simple Custom Node"
    bl_icon   = 'SOUND'

    text = StringProperty(name='text',
                          default='',
                          description="Text to show, if set will overide file")

    def init(self, context):

        self.width = 400
        self.use_custom_color = True

    def format_text(self):

        global TW

        out = []

        lines = self.text.splitlines()
        width = self.width
        TW.width = int(width) // TEXT_WIDTH
        for t in lines:
            out.extend(TW.wrap(t))
            out.append("")
        return out

    def draw_buttons(self, context, layout):
        # ノード内の設定項目を追加する
        # layout.label(text=self.text)
        col = layout.column(align=True)

        text_lines = self.format_text()
        for l in text_lines:
            if l:
                col.label(text=l)

    def draw_buttons_ext(self, context, layout):

        layout.prop(self, "text", text="Text", icon="GRIP")
        # 別に作った機能を呼び出す
        layout.operator("node.generic_note_from_clipboard", text="From clipboard")
```

## RNAプロパティについて

Blenderの各種プロパティを実装するときに使用するのが「RNAプロパティ」と呼ばれる物。  
これは、Blenderのデータ構造を拡張するための構造体で、DTO(Data Transfer Object)とのこと。  
と言う説明だけみても？？？ですが、  
とりあえず、各オブジェクトに追加のプロパティを追加することができる機能という認識でよさそうです。  [参考](https://dskjal.com/blender/rna-vs-id-property.html)
MayaのAddAttrとは違って、同種のノードタイプに一律でプロパティを拡張することができます。  
  
既存のオブジェクトに対して設定するように、自分で作成したカスタムノードに対してプロパティを  
作りたい場合は、このRNAプロパティの追加をします。  
  
```python
    text = StringProperty(name='text',
                          default='',
                          description="Text to show, if set will overide file")
```
プロパティはクラスの変数として指定してあげます。  
[プロパティ関係はこのHelp参照](https://docs.blender.org/api/blender2.8/bpy.types.Property.html#bpy.types.Property)

## 関数をオーバーライドする

プラグインを作る場合は、
[Nodeクラスのヘルプ](https://docs.blender.org/api/blender2.8/bpy.types.Node.html)を参考にして、自分が実装したい関数を  
オーバーライドして、自分のやりたい処理を作っていきます。  
  
今回のサンプルの場合は

* init
* draw_buttons
* draw_buttons_ext

この3つを使用しています。  

まず init。  
これはその名の通り、ノードが作成されたタイミングで実行され、  
いろいろな初期化の処理を作る事ができます。  
今回は、デフォルトのノードの横サイズをセットしています。  
  
Blenderのクラスは、「draw_XXXX」になっているものがUIへの描画になっている模様。  

### draw_buttons

まず、draw_buttonsがノード自体に各種ウィジェットを実装するための関数です。  

```python
    def draw_buttons(self, context, layout):
        # ノード内の設定項目を追加する
        # layout.label(text=self.text)
        col = layout.column(align=True)

        text_lines = self.format_text()
        for l in text_lines:
            if l:
                col.label(text=l)
```

BlenderでUIにオブジェクトを追加したい場合は  
**追加したいレイアウト.追加するオブジェクト（option）**
このように指定します。  
今回は、単純に文字を表示したいだけだったので、labelオブジェクトを追加しています。  
forで複数のラベルを追加しているのは  
テキストを複数行表示するためです。  
label自体は、改行コードが使えないため  
ウイジェットに複数のラベルを追加していきつつ、複数行表示ができるようにしているようです。  
  
### draw_buttons_ext

![](https://gyazo.com/2aada53efeab9471bbf15f2fc7753a96.png)

draw_buttons_extは、「N」を押したときにウィンドウの右側に表示されるトグルスライドバーの  
なかのUIパーツを追加するための関数です。

```python
    def draw_buttons_ext(self, context, layout):

        layout.prop(self, "text", text="Text", icon="GRIP")
        # 別に作った機能を呼び出す
        layout.operator("node.generic_note_from_clipboard", text="From clipboard")
```

この「prop」と「operator」は特殊で、  
propはRNAプロパティにつなげたUIを表示するときに使用します。  
今回の場合、テキストを保存するためのプロパティ「text」を変更できるようにしたいので  
propの第二引数でtextを指定しています。  
  
もう1つのoperatorは、ボタンを追加するコマンドで、  
実行するコマンドは、

```python
class pasteNoteFromClipboard(bpy.types.Operator):
    """
    Update note text from clipboard
    """
    bl_idname = "node.generic_note_from_clipboard"
    bl_label = ""
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        text = bpy.context.window_manager.clipboard
        if not text:
            self.report({"INFO"}, "No text selected")
            return {'CANCELLED'}
        node = context.node
        node.text = text
        return {'FINISHED'}
```

このようなOperatorクラスを継承したクラスを作成し、その中のexecutre内に  
ボタンを押したときの動作を実装します。  
  
この関数と紐付けをするのが ==bl_idname== で、 **node.generic_note_from_clipboard**  
この設定が、ボタンと実際の処理とをつなげる役割を持っています。  
  
今回のようなボタン以外も、メニューになにか機能を追加したいときなども  
Operatorで実装し、bl_idnameでメニューなどと紐付けをします。  
  
## 非日本語化Blenderでの注意点  
  
私は英語版のBlenderで作業をしていますが、  
その場合BlenderのUIに使用しているデフォルトフォントは英語のみのもののため  
今回作成したNoteで日本語を入れようとすると文字化けして表示されなくなります。  
  
この辺の環境はBlenderの環境依存っぽいので  
注意が必要です。  
  
なので、

![](https://gyazo.com/ba42c215bd27ae7ea4f84c62acbaeda8.png)

英語版のまま内部的に日本語文字列を使う場合は  
InterfaceのTextRenderingの「InterfaceFont」を  
日本語対応のフォントに切り替えておきます。  
  
## 結果  
  
![](https://gyazo.com/d4bee7a7f393a48373b718bb2a38ac1f.png)

こんな感じで、Node内のTextを変更すると  
ノードの中に文字が表示されるカスタムノードができあがりました。  
  
今回は中の処理をしないノードでしたが、  
プロパティの扱い方やUIへの追加、基本構造はほぼ同じなので  
必要に応じてノードの拡張は色々できそうです。  
  
夢が広がる