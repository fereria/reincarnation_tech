# [pymel] DrivenKey を取得する

<!-- SUMMARY:DrivenKey を取得する -->

```python
import pymel.core as pm

#DrivenKeyを取得する
#DrivenKeyは animCurveU* というノード
dKey = node.listConnections(type=("animCurveUL",
                                  "animCurveUA",
                                  "animCurveUT",
                                  "animCurveUU"))

#animCurveからDriver・Drivenを取得する｀
#driver
key.input.connections()[0]
#driven
key.output.connections()[0]
#DrivenKeyのKeyの数を取得(indexを取得)
num = key.numKeys()
#Driverの値を取得
driverVal = key.getUnitlessInput(index)
#Drivenの値を取得
drivenVal = key.getValue(index)

#すべてのKeyに対して処理をしたい場合は、numKeysで取得したindex数で
#ループを回してやれば良い。
for i in range(0,num):
    print key.getUnitlessInput(i)
    print key.getValue(i)
```

DrivenKey のノードは animCurveU\* とついている４つのノード。  
アクセス方法は、基本通常の Key と変わらない。  
ただし、入力側が Time ではなく Value のため　 getTime(index) ではなく getUnitlessIntpu(indes)になる。  
index は 0 スタート。

![](https://gyazo.com/6e1608ee3216af0b1c6d361cad0f4a66.png)

animCurve の Attribute に表示されている Keys。  
左側の数字が getValue や getTime や getUnitlessInput するときの引数になる index  
取得するコマンドは画像の通り。
