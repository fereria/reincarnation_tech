# USDをPythonから色々操作するための環境を作る

<!-- SUMMARY: USDをPythonから色々操作するための環境を作る -->

USD周りの基本であったり、構造周りの説明を先にやろうと思いましたが  
なんとなく中途半端な理解で書くと~~~微妙に恥ずかしいことになりそうなきがするので~~~  
混乱をうみそうなので、そっちはもうちょっと自分の中で咀嚼しつつ.....  
  
前回usdviewでUSDを開くまではできたので、  
USDファイルをそのまま直書きするのではなく、Python側から操作して  
なにがどうなっているのか検証するための環境を作ってみようとおもいます。  
  
## じゅんび

まず、準備。  
モデルをチェックできるusdviewですが、これはあくまでもビューワーなので  
AttributeEditorで数値をいれてコントール...のようなことはできません。  

![](https://gyazo.com/c9db8ccab23266051d25085db95c77bd.png)

が、数値を弄りたければPythonInterpreterがついているので  
そちらからコントロールすることはできます。  
  
が...このインタープリタで頑張るのは無理があるので  
私はVSCodeとJupyterを使用して環境をつくってみることにしました。  
  
まず、使用するPythonは３系を使用します。  
しかしこちらにはusdviewは入っていないので  
別途Python2用のUSD（nvidiaビルド）をダウンロードしておき  
そちらからusdviewを開いておきます。  
  
```
cd /d I:\jupyter_notebook_root
jupyter notebook
```
とりあえず、こんな感じで固定の場所でJupyterを起動できるBatchを作り  
裏でnotebookを起動しておきます。  
しかし、このnotebookをブラウザから使用すると、

![](https://gyazo.com/b3a8bf3a0e527f61b217b5cab8d82e9d.png)

一応使えますが、この場合AutoCompleteがきかないのと  
ショートカットが使いにくいので、korewoVSCode側からたたくようにします。  
  
![](https://gyazo.com/de2de82522cab139a46da49981bae9cc.png)

Pythonの Jupyter Server URIの設定を開き、  
裏で起動しているNotebookのURLを入力します。  
  
が、Tokenを入れたりするのが面倒だったので

```
jupyter notebook --generate-config
```
まず、Configを作り、  
  
C:/Users/<ユーザー名>/.jupyter  
  
下にある、 jupyter_notebook_config.py の中の  
```python
c.NotebookApp.token = ''
```
Tokenを消しておいて、  

```python
c.NotebookApp.password = "sha1:～～～～"
```

パスワードをいれておきます。  
  
パスワードは

```
python -c "import IPython;print(IPython.lib.passwd())"
```

このコマンドで生成できます。  
  
で。  
  
ここまで準備ができたら、あとはVSCode側でいろいろ検証していきます。  
  
## VSCodeでいろいろやる  
  
![](https://gyazo.com/f0178ed34c457eb832a04ea1ead65f11.png)

まず、VSCodeでどうやってセルを指定するかというと、処理を分けたいところで  

```
# %% 
```

これを入れて上げればOKです。  
あとは、実行したいときに「Run Cell」を押せばOKです。  
  
![](https://gyazo.com/c6c65af50bd2333a0c711671b179002a.png)  
  
Run Cellを実行すると、Python Interactiveタブが表示され、  
そこに実行結果が表示されます。  
  
## USDの中身を確認する  

## プリントする
  
まず、usdviewで開く前に　USDファイルの中身をプリントで確認してみます。  
  
```python
print(stage.GetRootLayer().ExportToString())
```
たびたび確認をしたくなるので、ここだけをセルで分けておいて  
必要に応じてプリントしてみます。

![](https://gyazo.com/67708aa3b9cd65a747f03ca9084c6a11.png)

こんな感じで、現在のUSDファイル（正確にはレイヤー）を  
プリントすることができます。  
  
注意点として、プリントする場合は「 print(～～～)」のように  
ちゃんとプリントコマンドを使用する必要があること。  
なしでも表示はできますが、その場合改行ができません。  
  
### 保存する

保存するときは StageをExportします。  
ここも度々やるのでセルにしておくと便利です。  
  
```python
stage.GetRootLayer().Export(USD_PATH_ROOT + "/refTest.usda")
```

こんな感じで出力します。  
  
USDは、開くときにNewOpenしてSaveすることもできるのですが  
すでにファイルがある場合エラーになってしまったりと微妙に面倒だったので  
  
```python
# 一度メモリ上にファイルを作り
stage = Usd.Stage.CreateInMemory()
# Export
stage.GetRootLayer().Export("PATH")
```
こんな感じでメモリ上にシーンを作り、最後にExportする方が  
毎回新規シーンでテストできてお手軽かなと思います。（たぶん）  
  
### usdviewで開く  
  
Exportしたら、usdviewでファイルを開きます。  
  
```
usdview I:\usd_test\refTest.usda
```

Windowsでusdviewを使う場合のトラップなのか  
引数で渡すusdファイルはフルパスである必要がある上、引数にusdファイルを必ず渡す必要があります。
また、このツール起動が尋常じゃなく遅いので  
初回のみ適当なファイルで開いておいて  
ツール上のメニューからファイルをNewOpenしたりReloadしたりするのがオススメです。  
  
![](https://gyazo.com/052b4430de2622643f14ae59322af78d.png)

とりあえずファイルが開けました。  
  
ここまで準備ができたら、あとはVSCode側でコードを書きつつ  
保存したらusdviewでCtrl+RでシーンをリロードしてプロパティやらPrimやら見た目やらが  
望む形になっているのか確認します。  
  
https://snippets.cacher.io/snippet/e4a461c3093c7ce7929f

あとは、テストした結果はCacherにメモとしてUPするようにしています。  

## 小ネタ

![](https://gyazo.com/5878a971ba83dcf4312eb3e6d1afcaae.png)

VSCodeのPythonInteractive の実行結果表示ですが  
どんどんたまっていきます。  
が、Interactiveの右上にある×ボタンを押せばリセットできます。  
  
また、フロッピアイコンを押すことでJupyterの ipynb ファイルとしても出力できます。  
  
https://snippets.cacher.io/snippet/90166b7fd86eb73d7d0e

出力はできるけど、そこまで使わなそう。  
  
  
とりあえず、ここまでやったらPythonで色々弄りたおすのに  
ストレスがないぐらいまでの環境ができました。  
  
多分、Exporterとかでデータフォーマットとして使う分には  
ここまでやらなくても良いかと思うのですが  
やはりUSDの合成を扱うにはPythonやC++での操作は必須になりますし  
データ構造を理解する意味でもPython側から扱うのは重要なので  
  
テスト環境をストレスなくできるようにするのは大切かなーと思います。