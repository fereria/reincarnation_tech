---
title: LoadRulesを使用してPayloadsを操作する
tags:
    - USD
    - Python
    - Payloads
---

USDのコンポジションの１つに「 [ペイロード](09_comp_arc_reference.md)」があります。
この、現状のステージのうち、どのSdfPathのPrimがロードされているのか？
今回は、このペイロードのロード状況の取得方法についてまとめていきます。

## UsdStageLoadRules

このロード状況を取得するには、 UsdStageLoadRules クラスを使用します。
このクラスは、 **UsdStageに対してペイロードを組み込む先のルール** を表します。

まずは、通常の場合。

```bat
usdview D:\usd\Kitchen_set\Kitchen_set.usd
```

このようにusdviewでキッチンセットをロードします。
この場合は、ペイロードはロードされた状態になっています。

![](https://gyazo.com/d9c83e62890a6aa9a961b86582071981.png)

この場合は、ルールは特に指定されていません。

```bat
usdview D:\usd\Kitchen_set\Kitchen_set.usd --unloaded
```

次に、 --unloaded を追加して、シーン内のペイロードをアンロード状態でステージを開きます。

![](https://gyazo.com/b317b4d2f2b1976ff367b7b261d1f9db.png)

結果。
LoadRulesを見ると </> , NoneRule になっているのがわかります。
NoneRuleとは、指定されたPrim（この場合 / なのでルート）以下にある
すべての子孫にあるペイロードを除外します。
つまりは、すべてのペイロードがすべてアンロードされている状態です。

最後に、すべてアンロードされた状態から、
ある特定のPrimのみロードしてみます。

```python
prim = stage.GetPrimAtPath('/Kitchen_set/Props_grp/North_grp/NorthWall_grp/MeasuringSpoon_1')
prim.Load()

rules = stage.GetLoadRules()
print(rules)
```

> UsdStageLoadRules([ (</>, NoneRule) (</Kitchen_set/Props_grp/North_grp/NorthWall_grp/MeasuringSpoon_1>, AllRule) ])

実行すると、LoadしたPrimのSdfPathがUsdStageLoadRulesに追加されているのがわかります。
ロード状態のものは「 AllRule」となっています。
これは、指定されたPrim以下にあるペイロード
（この場合はPrimの親子関係ではなく、あるPrimのコンポジションを指す）
すべてをロードするようになります。
これ以外のルールに、OnlyRule がありますが、こちらの場合は
現在のペイロードのみロードするというオプションになります。

これを利用することで、ステージのペイロードの状況を取得できて、

```python
rules = stage.GetLoadRules()
for sdfPath,rule in rules.GetRules():
    if rule == Usd.StageLoadRules.AllRule:
        print("[loadPath]")
        print(sdfPath)
```

たとえば、現在ロードされているPrimをすべて取得したい場合は
UsdStageLoadRulesの GetRules を使用して、
SdfPathとルールを取得すれば、ロード済のもののみ取得できます。

あるいは、
```python
# effective rule AllRule/OnlyRule/NoneRule を取得する
print(rules.GetEffectiveRuleForPath(loadPath))
# ロードされているか
print(rules.IsLoaded(loadPath))
```
GetEffectiveRuleForPath で、SdfPathを指定すると、
指定のSdfPathのPrimのルールを直接取得することができます。

## ロードする

UsdStageLoadRulesで現状の取得状況を取得できましたが、
取得だけではなくペイロードのロードも、UsdStageLoadRulesを使用することで
実行できます。

```python
loadPath = '/Kitchen_set/Props_grp/Ceiling_grp/CeilingLight_1'

prim = stage.GetPrimAtPath(loadPath)
print(prim.IsLoaded())
# >> False
rules = stage.GetLoadRules()
rules.AddRule(loadPath,Usd.StageLoadRules.AllRule)
stage.SetLoadRules(rules)
print(prim.IsLoaded())
# >> True

# 複数の場合
rules = stage.GetLoadRules()
r  = [('/Kitchen_set/Props_grp/DiningTable_grp/ChairB_1',Usd.StageLoadRules.AllRule),
      ('/Kitchen_set/Props_grp/DiningTable_grp/ChairB_2',Usd.StageLoadRules.AllRule)]
rules.SetRules(r)
stage.SetLoadRules(rules)
```

追加する場合は、ステージの現在のUsdStageLoadRulesを取得して、
そのルールに対して、AddRuleで追加するか
SetRulesで、複数ルールを同時に追加してから、
編集後のUsdStageLoadRulesを、 SetLoadRules でセットします。

## 全ロード・アンロード

すべてをロード・アンロードするのも、基本は同じです。

```python
# 全アンロードする
stage.SetLoadRules(Usd.StageLoadRules.LoadNone())
# 全ロードする
stage.SetLoadRules(Usd.StageLoadRules.LoadAll())
```

すべてをロード・アンロードするルールは、 StageLoadRules.LoadNone() あるいは LoadAll() でルールを作成できます。
ので、そのルールをSetLaodRules で設定すれば変更することができます。

## まとめ

StageやPrimのオブジェクトからLoad / Unload できていたペイロードでしたが
UsdStageLoadRulesを使用すれば、まとめてコントロールできる事がわかりました。

巨大なシーンをロードする場合は、多数のペイロードを制御することもあると思うので
その場合は、この UsdStageLoadRulesを使用するとわかりやすそうです。