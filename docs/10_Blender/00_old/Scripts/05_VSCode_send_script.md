# Blender のスクリプトを VSCode から実行

<!-- SUMMARY:BlenderのスクリプトをVSCodeから実行 -->

まず、VSCode 側からスクリプトの実行をできるように準備する。  
事前のじゅびは「VSCode での Addon 開発」を、参照。

![](https://gyazo.com/77380111c1d104969bd2d125807cfae2.png)

まず、コマンドパレットで「Blender:Start」でコマンドを実行する。
そして、実行する blender.exe を選択して、Blender が起動するのを待つ。

![](https://gyazo.com/e6ee99578cdeb75528f0599d9d4d61b9.png)

起動が完了すると、Blender と VSCode が接続される。

```python
# -*- coding: utf-8 -*-

import bpy
from mathutils import *
D = bpy.data
C = bpy.context

print(D)
```

VSCode で Python をファイルを作成して、このようなテストコードを作成する。

![](https://gyazo.com/13541b49918da5519d1e635fb5e20e30.png)

そのあと、Run Script を実行する。

![](https://gyazo.com/d4e95a5b20a793f483de229f01586311.png)

実行すると、デバッグコンソールに Blender での実行結果が  
表示され、Blender でコマンドが実行される。

![](https://gyazo.com/3c86c7ce1581ac93801de17c30762bec.png)

ブレークポイントを置いてから Run Script を実行すると、ブレークポイントで  
停止して、関数の中身の確認なども見ることができる。

![](https://gyazo.com/8f661f3ea517d6011fcea04f574b7053.png)

ブレークポイントを作成して実行すると、  
読み込み専用のバッファが作成され、そちらでデバッグを実行できる。  
実行が終了したら、タブを閉じる。
