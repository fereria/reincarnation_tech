# クラスのインスタンス変数とクラス変数

<!-- SUMMARY:クラスのインスタンス変数とクラス変数-->

PythonのクラスにListを使ったときに地味にはまったこと。

```python
class Test:
    value = []
    
a = Test()
b = Test()

a.value.append(10)


print(a.value)
print(b.value)
# 参照メモリがオブジェクトが違っても同じ
print(id(a.value))
print(id(b.value))
```
まず、こんな感じにPythonのクラスのメンバ変数に「List」を定義する。  
そうすると  
  
![](https://gyazo.com/771806fa0672becd645ed707a2f0ff49.png)

aのほうにしかappendしていないのに、bのほうのオブジェクトの変数にも  
数値が入ってしまっている。  
確認してみると、aオブジェクトもbオブジェクトも同じメモリを参照してる様子。  
  
```python
class TestB:
    def __init__(self):
        self.value = []
        
c = TestB()
d = TestB()

c.value.append(10)

print(c.value)
print(d.value)
print(id(c.value))
print(id(d.value))
```

このように、selfで初期化している場合は違うIDになりました。  
  
今までは、上の書き方も下の書き方も同じものだと思って考えてたのですが、  
この2つはクラスの変数という意味で似たものですが全然違うものなのを今日知りました。  
  
上のほうは **「クラス変数」** と呼ばれるもので、別インスタンスであっても共通の値で  
クラス内で使う場合は ClassName.value のようにして扱い、  
インスタンスをまたいでメモリを共有する変数になる。
対して、下のほうは **「インスタンス変数」** と呼ばれるもので、インスタンス固有の値を持つようになる。  
クラス内では、 self.value のように書くのは（当たり前だが） self = インスタンス  
という意味で、自信のインスタンスのvalueを参照...という意味になる。  
  
なので、

```python
class TestC:
    value = []
    def __init__(self):
        self.value = [1,2,3]
```
このような書き方をしていると、クラス変数をインスタンス変数で上書きしてしまうので  
あまり意味がなくなってしまう。  
ので、インスタンス変数として使いたいなら __init__ 内で初期化すべきだし  
違いは理解しておかないといろいろと問題になるので注意が必要。
  
今まで全く知らなかった...orz  


## 参考

* https://uxmilk.jp/41600