# Python のクラスで多重継承した場合の**init**順序

<!-- SUMMARY:Pythonのクラスで多重継承した場合の__init__順序 -->

## 多重継承した場合

```python
# -*- coding: utf-8 -*-

class BASE(object):
    def __init__(self):
        print "BASE"
class A(BASE):
    def __init__(self):
        print "A-mae"
        super(A, self).__init__()
        print "A"
class B(BASE):
    def __init__(self):
        print "B-mae"
        super(B, self).__init__()
        print "B"
class MAIN(B, A):

    def __init__(self):
        super(MAIN, self).__init__()
        print "MAIN"

a = MAIN()

```

このような多重継承のクラスを作成した場合。  
プリントの結果は

B-mae  
A-mae  
BASE  
A  
B  
MAIN

このような順序になる。  
A と B は、同じ BASE クラスを継承しているが  
BASE が呼ばれるのは 1 度のみ。  
親クラスの初期化順序は、 MAIN( ) この() の右側が先となる。  
この場合、 (A,B) ならば、初期化で呼ばれる順序は B->A となる。

> Super を使用した場合は、多重継承していた場合でも関係する親クラスの**init**を
> 重複しているクラスがあったとしても 1 回ずつ実行するようになる。

## 初期化方法の注意点

```python
class MAIN(B, A):

    def __init__(self):
        # super(MAIN, self).__init__()
        A.__init__(self)
        B.__init__(self)
        print "MAIN"
```

親クラス名.**init**(self) このような書き方もできるが、  
この場合は init の順序が違い

A-mae  
BASE  
A  
B-mae  
A-mae  
BASE  
A  
B  
MAIN

このようになる。  
なぜか、この書き方の場合 init が 2 回入ることになる。

![](https://gyazo.com/8354e62976d48597191c2ce820bea456.gif)

チェックをしてみると、B.**init**() のところで、A の初期化にもいくようになっている。  
super の場合、親クラス(多階層になっていても）1 ずつ初期化するので  
特に理由がない場合は super を使用して初期化する方が安全な模様。

> 上の例の場合は、 BASE2 回 A 2 回 B 1 回の初期化でしたが、これを継承元を 3 つにすると
> Base3 A3 B2 C1 のように、継承先が増えるほど初期化の数が増えいく。
