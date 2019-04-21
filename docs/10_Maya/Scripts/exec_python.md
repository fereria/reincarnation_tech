# Python ファイル(.py)を実行する

<!-- SUMMARY:Python ファイル(.py)を実行する -->

## とりあえず、さくっと実行

Python で、.py ファイルを import ではなくそのまま実行したい場合は

```python
execfile("<python_path>")
```

このようにします。

```python
# -*- coding: utf-8 -*-
print u"はろーわーるど"
```

このファイルを

```python
execfile("S:/test_file.py")
```

このように実行すれば、

![](https://gyazo.com/8c8687e6f3c19ac8eac089fd325fbdff.png)

中のコードが実行されます。

この execfile は、import で実行するときと基本的なルールは同じで  
1 行目の

```
# -_- coding: utf-8 -_-
```

がない場合は、

![](https://gyazo.com/9a3a1b226a469c7acee83acefc4c7017.png)

エラーになります。

## 文字コードの問題

Python ファイルを実行する場合に注意しなければいけないのが文字コード問題。  
文字コードは、各エディタごとに設定ができるようになっています。

![](https://gyazo.com/389a04f77ab54d7500945dc30bf07ea1.png)

私が使っている VSCode の場合、右下のところに文字コードの設定が表示されています。

![](https://gyazo.com/f7bba044771ecb7fa1858ecd453052e8.png)

Python ファイルの 1 行目の coding:### 部分は、  
このエンコード設定と同じになってる必要があります。  
↑ のように、ファイル自体は「Shift JIS」になっているのに、  
ファイルそのものが utf-8 になっている場合は、

```python
# Error: (unicode error) 'utf8' codec can't decode byte 0x82 in position 0: invalid start byte
# Traceback (most recent call last):
#   File "<maya console>", line 1, in <module>
#   File "S:/test_file.py", line 2
#     print u"はろーわーるど"
# SyntaxError: (unicode error) 'utf8' codec can't decode byte 0x82 in position 0: invalid start byte #
```

このようにエラーになってしまいます。

```
# -*- coding: shift-jis -*-
```

エラーにならないようにするには、文字コードと 1 行目の設定を同じにすれば

![](https://gyazo.com/41f26ec0f16f49e9d8b60a1608da2fbb.png)

エラーは発生しません。

## 文字コードエラーを発生させずに無理矢理 Python ファイルを実行する

execfile を使用せずに、1 行目の #encoding 設定を書かずに実行したい場合は、  
Mel ファイルから実行するという手もあります。

```mel
global proc exec_python_file(string $py_path){
    string $cmd[];

    $fileId=fopen($py_path,"r");
    string $nextLine = `fgetline $fileId`;
    while ( size( $nextLine ) > 0 ) {
	    appendStringArray $cmd {$nextLine} 1;
	    $nextLine = `fgetline $fileId`;
    }

    string $exec_cmd = stringArrayToString($cmd,"\n");
    python $exec_cmd;
}
```

例がこちら。  
mel のコマンドで python を実行したい場合は、python("cmd");コマンドを使用します。  
コレを利用して、  
fopen で python ファイルをテキストとして読み込み、文字を改行コードで結合し  
その結合した結果を python コマンドで実行します。  
この場合、1 行目の encoding 設定がない場合でも、エラーは発生しません。

ただし、この場合はファイル自体が Shift-Jis である必要があり  
文字コードが UTF-8 などで作成されている物を Mel から実行しようとすると  
文字化けしてしまい正しく実行されません。

Maya のデフォルトエンコードについては ↓  
http://help.autodesk.com/view/MAYAUL/2016/JPN/?guid=GUID-88109151-076A-4AB1-836A-85370B32A256

## execfile のおまけ

```python
# -*- coding: utf-8 -*-
def test_hello():
    print u"はろーわーるど"
```

execfile で Python ファイルを実行したときは、グローバルに書かれた内容が実行されるだけで  
書かれている関数は実行されない。  
↑ のように書かれた関数を execfile で実行してから使用したい場合は

```python
G={}
L={}
execfile("S:/test_file.py",G,L)
L['test_hello']()
```

このようにする。  
execfile の 2、3 つめの引数に、空の Dict を入れると  
その中に execfile 内の関数・変数が代入されます。  
中で定義されている関数は Local 関数扱いなので 3 つめの引数「L」に入ります。

```python
{'test_hello': <function test_hello at 0x0000015C7B715F98>}
```

Dict 型はこのようになっていて、関数名の Key に中に Function が入ってます。

```python
HOGEHOGE = "fugafuga"
```

関数以外に、変数を定義してから使いたい場合も同様で

```python
{'HOGEHOGE': 'fugafuga', 'test_hello': <function test_hello at 0x0000015C7B715F98>}
```

Key が変数名、その中身に代入された中身が入っています。

これを利用して動的に python ファイルをロードする事も出来ますが、  
動的ロードをしたい場合は execfile を使用するよりも  
importlib を使う方が良いです。

importlib については ↓  
https://qiita.com/progrommer/items/abd2276f314792c359da
