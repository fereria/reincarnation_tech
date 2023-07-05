---
title: C++でUSDのViewportを作ろう(1) カメラを作る
tags:
    - USD
    - AdventCalendar2022
description: C++とimguiでビューポートを作る_カメラ実装
slug: /usd/cpp/viewport_01
sidebar_position: 4
---

[USD AdventCalendar2022](https://qiita.com/advent-calendar/2022/usd) 10 日目は C++と imgui で USD のビューポートを作ろう です。

![](https://gyazo.com/c8a3e25d0fb8c6df9558cd966603891a.gif)

今回は、こんな感じで OpenGL で USD を表示して、マウスでぐりぐり回せるようにしてみます。
そして GUI には imgui を使用して、必要な情報を表示したり編集できるようにしてみます。

なお、あらかじめ予防線を張っておくと私自身 C++はほぼ初心者です。
のでもっといいやり方あるよとか、いやそうじゃない、みたいなことも大いにあると思いますがお許しください。
もっといいやり方あるよという方は、公開リポジトリに PR なりコメントなり入れてくれると
大変喜びます。

という前置きはここまでにして、やっていきましょう。

## 準備

まず環境づくり。
最初に USD を事前にビルドしておきます。
ビルド方法は [USD を使ってみる](/usd/install_usd)にまとめてありますのでそちらを産所うをば。
次に、imgui を用意します。
今回は勉強を兼ねて vcpkg 経由でライブラリを取得して、CMake を使用してビルドします。
この辺りはものすごく苦戦して検証の大半はここに時間を取られました。
[VSCode で C++の環境を作るメモ](/pg/vscode/vscode_cpp) 詳細はこちらにまとめてあります。
この記事に書かれている通りに VSCode を設定し、 vcpkg で取得までした状態からスタートです。

## しくみ

OpenGL でビューポートを 0 から作ろうとすると、そこそこ大変です。
実際、私自身も 1 から作れと言われるととてもじゃないですが実装はできません。

ですが、USD と Hydra を活用することで簡単にモデルを描画させたり
カメラ操作を実装したりできます。

![](https://gyazo.com/5d5e0de67e9db35bc369e7e334819e3f.png)

USD のシーングラフは [UsdImagingGLEngine](https://graphics.pixar.com/usd/dev/api/class_usd_imaging_g_l_engine.html#details) と呼ばれる、USD のシーンをレンダリングするためのエントリーポイントを経由して Hydra に渡されます。
そしてレンダラにデータを渡しますが、
それ以外にも、データを OpenGL のビューポートに対して描画するという機能が用意されています。

これを活用することで、複雑な処理は USD の機能にお任せして、お手軽にビューポート実装が作れます。

## 参考にするもの

さすがにノーヒントで作るのは難しいので、USD リポジトリ以下にあるコードを参考にします。

https://github.com/PixarAnimationStudios/USD

USD リポジトリ以下の
pxr/usdImaging/usdviewq/stageView.py
に、usdview のビューポートを実装しているコードがあります。
これは Python で書かれていて、PySide2 の QGLWidget に対して、 UsdImagingGL.Engine を使用して実装されています。

ここのコードを読み取って、実装に必要な要素をリストしてみます。

-   OpenGL のビューポートを用意する＆初期化
-   Camera を用意する
-   Mouse の操作情報を取得してカメラを操作する
-   UsdImagingGL の設定
-   UsdStage 側の準備
-   描画

順番にやっていきます。

## OpenGL のビューポートを作る

https://gist.github.com/fereria/474ccd687e700bd729316ccbbae0216d

長いのでコードは ↑
Imgui の samples/example_glfw_opengl2/main.cpp をベースに、必要な部分だけをピックアップして
小さな Window が一つと、ビューポートを用意します。

![](https://gyazo.com/2d4c0c14d19ef1b4e45d66a286ffeede.png)

実行するとこのようになります。

Imgui は、メインループの都度舞フレーム実行することになります。
この場合 while の中がこれにあたり、このメインループの中でカメラの位置計算や実際の描画処理を
書いていく必要があります。

![](https://gyazo.com/8c0fcf8b1d366bf573090c89de96bf7c.png)

stageView.py の処理を参考にして全体の流れを書き出すと、こんな感じになります。
カメラの作成は、シーンに含まれるカメラというより
persp カメラのようなビューポートで自由に操作できるフリーカメラです。

pxr/usdImaging/usdviewq/freeCamera.py

usdview では、freeCamera.py で用意されていて
このフリーカメラでマトリクスの計算などもろもろやっています。

## Camera を作る

なので、まずはこの freeCamera.py を参考に C++でカメラを作ります。

<Gist id="a4d194bddf28c4b10447c227ef715b96" file="SimpleCamera.h"/>

まずはヘッダー。
基本操作の Track PanTilt Tumble をできるようにします（Walk は今回未実装）

UsdImagingGLEngine でのカメラは、 GfMatrix4d の viewMatrix と projectionMatrix で設定します。
このマトリクスは、GfCamera の GetFrustum() から [ViewFrustum](https://en.wikipedia.org/wiki/Viewing_frustum) を
管理する GfFrustum を取得することで、

```cpp
        renderer->SetCameraState(frustum.ComputeViewMatrix(),
                                 frustum.ComputeProjectionMatrix());
```

このようにそれぞれの値を取得できます。
ので、そのためにはまずカメラの定義である GfCamera を用意して
この GfCamera を Track PanTilt Tumble 関数を使用して処理していけば OK なわけです。

次に、各関数を実装します。

https://gist.github.com/fereria/10791528bebc1882258cf591af142827

全体はこちらですが、各要素を個別に解説していきます。

```cpp
SimpleCamera::SimpleCamera()
{
    this->YZUpMatrix = GfMatrix4d().SetRotate(GfRotation(GfVec3d::XAxis(), -90));
    this->YZUpInvMatrix = this->YZUpMatrix.GetInverse();
    this->cameraTransformDirty = false;
}
```

まずは、カメラの初期化でシーンが Zup なのか Yup なのかを指定します。
今回は Zup です。

freeCamera.py の内容を C++に移植しています

### Zoom

![](https://gyazo.com/0c672ca905f0178419fe4f6ed94b379d.png)

Zoom は、カメラとターゲットとなるポジションの値を変更することで実装します。

```cpp
        if (this->camMode == CameraMode::ZOOM)
            this->dist += -0.5 * (moveX + moveY);
```

次回まとめますが、メインループ時に指定のキーを押している場合
値を増減させます。

```cpp
void SimpleCamera::SetDist(double value)
{
    this->_dist = value;
    this->_pushFromCameraTransform();
    this->cameraTransformDirty = true;
}
```

![](https://gyazo.com/0442a5e952fad612c6fa83329ca91c02.gif)

結果こんな感じになります。

### Tumble

Tumble は、指定のターゲットポジションを中心にカメラを回転させます。

```cpp
void SimpleCamera::Tumble(float dTheta,float dPhi)
{
    //左ボタン
    this->_rotTheta += dTheta;
    this->_rotPhi += dPhi;
    this->cameraTransformDirty = true;
}
```

![](https://gyazo.com/a370dd358f818a7835d86fc36eb74356.png)

Tumble で値を足してるのは、カメラの移動の ↑ 部分の移動値を指定していて

![](https://gyazo.com/682e8b8faaccd1145724dd52f69658bd.gif)

### Track

Track は現在のカメラを縦横に移動します。

```cpp
void SimpleCamera::Track(float deltaRight, float deltaUp)
{
    // 中ボタン
    this->_pushFromCameraTransform();

    GfFrustum frustum = this->_cam.GetFrustum();
    GfVec3d cam_up = frustum.ComputeUpVector();
    GfVec3d cam_right = GfCross(frustum.ComputeViewDirection(),cam_up);
    this->_center += (deltaRight * cam_right + deltaUp * cam_up);
    this->cameraTransformDirty = true;
}
```

現在のカメラの視錐台おから UpVector とその UpVector から外積を使用して
RightVecotr を取得します。
そしてその 2 つのベクトルに対して、移動値(deltaRight DeltaUp)を追加して
カメラのセンターを移動します。

![](https://gyazo.com/03b12cb87f4f75bb8f83856d3a237aef.gif)

### PushCamera

ターゲットとの距離、ターゲットを中心に回転させ、カメラのセンター位置をずらした
カメラの ViewMatrix を作成します。

```cpp
void SimpleCamera::_pushFromCameraTransform()
{
    if(this->cameraTransformDirty == false) return;

    GfMatrix4d viewMatrix;
    viewMatrix.SetIdentity();

    viewMatrix *= GfMatrix4d().SetTranslate(GfVec3d::ZAxis() * this->_dist);
    viewMatrix *= this->RotMatrix(GfVec3d::ZAxis(), _rotPsi);
    viewMatrix *= this->RotMatrix(GfVec3d::XAxis(), _rotPhi);
    viewMatrix *= this->RotMatrix(GfVec3d::YAxis(), _rotTheta);
    viewMatrix *= this->YZUpInvMatrix;
    viewMatrix *= GfMatrix4d().SetTranslate(this->_center);

    this->_cam.SetTransform(viewMatrix);
    this->_cam.SetFocusDistance(this->_dist);

    this->cameraTransformDirty = false;
}

```

### Pan Tilt

Pan と Tilt は、カメラ位置を固定して左右あるいは上下に回転させる処理です。

```cpp
void SimpleCamera::PanTilt(double dPan, double dTilt)
{
    this->_cam.SetTransform(
        RotMatrix(GfVec3d::XAxis(), dTilt) *
        RotMatrix(GfVec3d::YAxis(), dPan) *
        this->_cam.GetTransform());
    this->_pullFromCameraTransform();

    this->_rotPsi = 0.0;
}
```

なので、カメラの SetTransform で X 軸（上下）に回転と Y 軸（左右）を計算します。
PushCamera で作成したカメラ位置から X 軸と Y 軸で回転し、

```cpp
void SimpleCamera::_pullFromCameraTransform()
{
    GfMatrix4d cam_transform = this->_cam.GetTransform();
    float dist = this->_cam.GetFocusDistance();
    GfFrustum frustum = this->_cam.GetFrustum();
    GfVec3d cam_pos = frustum.GetPosition();
    GfVec3d cam_axis = frustum.ComputeViewDirection();

    GfMatrix4d transform = cam_transform * this->YZUpMatrix;
    transform.Orthonormalize();
    GfRotation rotation = transform.ExtractRotation();
    GfVec3d result = -rotation.Decompose(GfVec3d::YAxis(),
                                         GfVec3d::XAxis(),
                                         GfVec3d::ZAxis());

    this->_dist = dist;
    this->_center = cam_pos + dist * cam_axis;

    this->cameraTransformDirty = true;
}
```

その結果計算した視錐台から、位置と View 方向とカメラのセンター位置を取得します。
この結果の dist と center は次の移動計算に使用しています。

これで、GfCamera を使用したカメラの計算ができました。

かなり計算が苦手なので、やっていることを理解しきれているか怪しいですが
カメラの実装も USD の各種クラスを活用すれば
何とかなりました。

次は、imgui の GUI とメインループを書いていきます。
