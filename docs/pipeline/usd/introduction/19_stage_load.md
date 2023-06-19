---
slug: /usd/load_rule
title: UsdStageLoadRulesの使い方
description: UsdStageLoadRulesを使ったペイロードの ロード・アンロードの方法
tags:
    - USD
    - Python
    - Payloads
sidebar_position: 20
---

USD のコンポジションの１つに「 [ペイロード](/usd/reference) 」があります。
この、現状のステージのうち、どの SdfPath の Prim がロードされているのか？
今回は、このペイロードのロード状況の取得方法についてまとめていきます。

## UsdStageLoadRules

このロード状況を取得するには、 UsdStageLoadRules クラスを使用します。
このクラスは、 **UsdStage に対してペイロードを組み込む先のルール** を表します。

まずは、通常の場合。

```bat
usdview D:\usd\Kitchen_set\Kitchen_set.usd
```

このように usdview でキッチンセットをロードします。
この場合は、ペイロードはロードされた状態になっています。

![](https://gyazo.com/d9c83e62890a6aa9a961b86582071981.png)

この場合は、ルールは特に指定されていません。

```bat
usdview D:\usd\Kitchen_set\Kitchen_set.usd --unloaded
```

次に、 --unloaded を追加して、シーン内のペイロードをアンロード状態でステージを開きます。

![](https://gyazo.com/b317b4d2f2b1976ff367b7b261d1f9db.png)

結果。
LoadRules を見ると NoneRule になっているのがわかります。
NoneRule とは、指定された Prim（この場合 / なのでルート）以下にある
すべての子孫にあるペイロードを除外します。
つまりは、すべてのペイロードがすべてアンロードされている状態です。

最後に、すべてアンロードされた状態から、
ある特定の Prim のみロードしてみます。

```python
prim = stage.GetPrimAtPath('/Kitchen_set/Props_grp/North_grp/NorthWall_grp/MeasuringSpoon_1')
prim.Load()

rules = stage.GetLoadRules()
print(rules)
```

UsdStageLoadRules([ (/, NoneRule) (</Kitchen_set/Props_grp/North_grp/NorthWall_grp/MeasuringSpoon_1>, AllRule) ])

実行すると、Load した Prim の SdfPath が UsdStageLoadRules に追加されているのがわかります。
ロード状態のものは「 AllRule」となっています。
これは、指定された Prim 以下にあるペイロード
（この場合は Prim の親子関係ではなく、ある Prim のコンポジションを指す）
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

たとえば、現在ロードされている Prim をすべて取得したい場合は
UsdStageLoadRules の GetRules を使用して、
SdfPath とルールを取得すれば、ロード済のもののみ取得できます。

あるいは、

```python
# effective rule AllRule/OnlyRule/NoneRule を取得する
print(rules.GetEffectiveRuleForPath(loadPath))
# ロードされているか
print(rules.IsLoaded(loadPath))
```

GetEffectiveRuleForPath で、SdfPath を指定すると、
指定の SdfPath の Prim のルールを直接取得することができます。

## ロードする

UsdStageLoadRules で現状の取得状況を取得できましたが、
取得だけではなくペイロードのロードも、UsdStageLoadRules を使用することで
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

追加する場合は、ステージの現在の UsdStageLoadRules を取得して、
そのルールに対して、AddRule で追加するか
SetRules で、複数ルールを同時に追加してから、
編集後の UsdStageLoadRules を、 SetLoadRules でセットします。

## 全ロード・アンロード

すべてをロード・アンロードするのも、基本は同じです。

```python
# 全アンロードする
stage.SetLoadRules(Usd.StageLoadRules.LoadNone())
# 全ロードする
stage.SetLoadRules(Usd.StageLoadRules.LoadAll())
```

すべてをロード・アンロードするルールは、 StageLoadRules.LoadNone() あるいは LoadAll() でルールを作成できます。
ので、そのルールを SetLaodRules で設定すれば変更することができます。

## まとめ

Stage や Prim のオブジェクトから Load / Unload できていたペイロードでしたが
UsdStageLoadRules を使用すれば、まとめてコントロールできる事がわかりました。

巨大なシーンをロードする場合は、多数のペイロードを制御することもあると思うので
その場合は、この UsdStageLoadRules を使用するとわかりやすそうです。
