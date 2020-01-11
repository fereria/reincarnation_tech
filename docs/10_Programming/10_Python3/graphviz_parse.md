---
title: Graphvizのノードの配置情報をパースする
---
# Graphvizのノードの配置情報をパースする

PySideのNodeEditorのレイアウト部分にGraphvizを使っているケースが多かったので、  
実行結果をパースしてNodeとして取得するる方法をテストしてみました。  
  
```python
import tempfile
import os.path
import subprocess

DOT_FILE = """
strict graph {
  a -- b
  b -- a
  a -- c
}
"""

tmp = tempfile.TemporaryDirectory()

dot_file = os.path.join(tmp.name, 'dot_file.dot')
xdot_txt = os.path.join(tmp.name, 'xdot.txt')

with open(dot_file, 'w') as f:
    f.write(DOT_FILE)

subprocess.call(f"dot -T plain-ext -o {xdot_txt} {dot_file}")

class Node(object):

    def __init__(self):

        self.name = ""
        self.pos_X = 0
        self.pos_Y = 0
        self.size_X = 0
        self.size_Y = 0
        self._inputs = []
        self._outputs = []

    def addInputs(self, n):
        if n not in self._inputs:
            self._inputs.append(n)

    def addOutputs(self, n):
        if n not in self._outputs:
            self._outputs.append(n)


nodes = {}

with open(xdot_txt, 'r') as f:
    for i in f.readlines():
        print(i)
        buff = i.split(" ")
        if buff[0] == "node":
            node = Node()
            node.name = buff[1]
            node.pos_X = float(buff[2])
            node.pos_Y = float(buff[3])
            node.size_X = float(buff[4])
            node.size_Y = float(buff[5])
            nodes[buff[1]] = node
        elif buff[0] == "edge":
            nodes[buff[1]].addOutputs(nodes[buff[2]])
            nodes[buff[2]].addInputs(nodes[buff[1]])

print(nodes)
tmp.cleanup()
```

![](https://gyazo.com/bef448ee03989e8fc97123b1fdd53d30.png)

実行すると、こんな感じでNodeオブジェクトを取得できます。  
  
![](https://gyazo.com/57f8b184b30c2fa939672e1ce79f79f5.png)

Nodeオブジェクトの中身。  
  
まず、出力したいdotファイルをPythonのtempfileモジュールで作ったフォルダ下に  
一端出力します。  
出力したら、その結果をtxtで出力します。  
  
dot.exeはpngのような画像でも出力できるのですが、  

![](https://gyazo.com/c91263e6f6714221e02937c04f1a9056.png)

こんな感じのテキストでも出力できるので  
パースのしやすさから -T plain-ext 形式でレイアウトした状態の結果を取得します。  
  
https://www.graphviz.org/doc/info/output.html#d:plain-ext

フォーマットのルールはDocs参照。  
Docsにはjsonもあるっぽいことが書かれているのですが、Versionのせいなのかなんなのかは  
わかりませんがErrorになってしまい使えませんでした。  
何故。  
  
NodeEditor回りのもろもろはもちおさんのGitHubにアップされている
mochinode(https://github.com/mochio326/mochinode)    
を参考にさせてもらいました。  
いつもありがとうございます。
