# PythonでHoudiniのパラメーターを取得・セットする

<!-- SUMMARY:PythonでHoudiniのパラメーターを取得・セットする -->

![](https://gyazo.com/a8376db18ae84ff7b973731277d30dbb.png)

Houdiniのパラメーターは、Objectなどと同じくPath形式で取得することができる。  
PathはパラメーターがあるNode/パラメーター名。  
アクセス用の名前が知りたい場合は、  
取得したいパラメーター名をクリックし、PythonShellにDrag&Dropすればフルパスが表示される。

## Nodeのアトリビュートを取得する
  

```python
node = hou.node('/obj/geo1/testgeometry_pighead1')
node.parm('difficulty')
```

指定のオブジェクトのパラメーターを取得したい場合は、 parm('parm_name')でOK。  

## プルダウンの中身を取得したい


![](https://gyazo.com/b1e756b57d76af9a3f63952561baf791.png)

こんな感じのListの中の要素を取得したい場合。  
  
```python
param = node.parm('difficulty')
p_temp = param.parmTemplate()
p_temp.menuItems() # Tupleで取得
```
MenuParmTemplate形式で取得できる。  

!!! note
    パラメーターの中の要素を弄ったりするのもこのparmTemplateっぽい
    

## 値をセットする

指定のパラメーターに値をセットする場合は、 set を使用する。

```python
param.set(0)
```
このようにすると、Listの0番目が選択される。