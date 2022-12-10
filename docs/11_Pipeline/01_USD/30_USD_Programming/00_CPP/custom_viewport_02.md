---
title: C++でUSDのViewportを作ろう(2) メイン部分を作る
tags:
    - USD
    - AdventCalendar2022
description:
---

{{markdown_link('custom_viewport_01')}} では、UsdImagingGLEngine を使用した
カスタムビューポートのうち、GfCamera を使用したカメラの実装をしました。

ので、今度はメイン部分を実装します。

## ヘッダーを定義する

まずはヘッダーを定義します。

{{'2a98417e35ad275315da3e94904af749'|gist}}

作成しておいた SimpleCamera や、今回のメインとなる UsdImagingGLEngine
あとはレンダーパラメーターを定義する UsdImagingGLRenderParams 等を用意します。

## 本体

https://gist.github.com/fereria/f6802da7f418cc418ddd39dd1cab376e

本体は長いので全コードはこちらから。
いくつか重要ポイントをまとめていきます。

## コンストラクタ

```cpp
MainWindow::MainWindow()
{
    // 初期値の設定
    this->dist = 1000;
    this->pan = 0;
    this->tilt = 0;

    this->cameraActive = false;
    this->camMode = CameraMode::OFF;

    this->initGL();

    this->renderer = new UsdImagingGLEngine();

    this->renderParams.drawMode = UsdImagingGLDrawMode::DRAW_WIREFRAME_ON_SURFACE;
    this->renderParams.enableLighting = true;
    this->renderParams.enableIdRender = false;
    this->renderParams.frame = 0;
    this->renderParams.complexity = 1;
    this->renderParams.cullStyle = UsdImagingGLCullStyle::CULL_STYLE_BACK_UNLESS_DOUBLE_SIDED;
    this->renderParams.enableSceneMaterials = false;
    this->renderParams.highlight = true;

    this->stage = UsdStage::Open("D:/Kitchen_set/Kitchen_set.usd");
}
```

まずはコンストラクター。
カメラの初期値の指定や、カメラモード、もろもろ初期化
UsdImagingGLEngine を用意したり、renderParams も指定します。

そして、Viewport に表示したい USD ファイルのステージを開きます。
今回は引数とかで指定することもなく決め打ちです。

## マウスやキーボードの Callback

当初は、コールバックはクラス関数として定義して呼び出せばいいのか？
と思っていたのですが、GLFW が C 言語でできている？とかでうまくいかずかなり苦戦しました。

```cpp
void mouseCallback(GLFWwindow *window, double xpos, double ypos)
{
    MainWindow *_this = static_cast<MainWindow *>(glfwGetWindowUserPointer(window));

    _this->mouse_pos_X = xpos;
    _this->mouse_pos_Y = ypos;
}
```

対処法は、

```cpp
glfwSetCursorPosCallback(window, mouseCallback);
```

glfwSetCursorPosCallback でコールバックを登録し、
コールバック内で、 glfwGetWindowUserPointer でウィンドウのポインタを取得
そしてそれを MainWindow にキャストすることで、
MainWindow のマウスポジションに現在のポジションをセットできるというのに至りました。
難しすぎる。

```cpp
void mouseClickCallback(GLFWwindow *window, int button, int action, int mods)
{
    MainWindow *_this = static_cast<MainWindow *>(glfwGetWindowUserPointer(window));
    _this->camMode = CameraMode::OFF;
    if (_this->cameraActive)
    {
        if (button == GLFW_MOUSE_BUTTON_LEFT && action == GLFW_PRESS)
            _this->camMode = CameraMode::TUMBLE;
        if (button == GLFW_MOUSE_BUTTON_MIDDLE && action == GLFW_PRESS)
            _this->camMode = CameraMode::TRUCK;
        if (button == GLFW_MOUSE_BUTTON_RIGHT && action == GLFW_PRESS)
            _this->camMode = CameraMode::ZOOM;
    }
}
```

同様にキー入力もコールバックを指定し、現在押下中のキー情報を Enum で指定します。
今回の例だと、Maya の操作方法と同じになるように指定しています。

これで、キー入力でカメラを回したりする準備ができました。

## initGL

glfw や Window の初期化は、imgui のサンプルを参考にして書きました。

```cpp
void MainWindow::initGL()
{

    glfwInit();
    this->window = glfwCreateWindow(1280, 720, "Hydra Sample", NULL, NULL);
    glfwSetWindowUserPointer(window, this);
    glfwMakeContextCurrent(this->window);
    glfwSwapInterval(1); // Enable vsync

    glfwSetWindowUserPointer(window, this);
    // Key/Mouse入力取得
    glfwSetKeyCallback(window, keyCallback);
    glfwSetMouseButtonCallback(window, mouseClickCallback);
    glfwSetCursorPosCallback(window, mouseCallback);

    // Setup Dear ImGui context
    IMGUI_CHECKVERSION();
    ImGui::CreateContext();
    ImGuiIO &io = ImGui::GetIO();
    (void)io;
    // Setup Dear ImGui style
    ImGui::StyleColorsDark();
    // Setup Platform/Renderer backends
    ImGui_ImplGlfw_InitForOpenGL(window, true);
    ImGui_ImplOpenGL2_Init();
}
```

ここで、コールバックの指定なども行っています。

## メイン処理

show()を実行すると、imgui のメインループを実行するようにします。

```cpp
    while (!glfwWindowShouldClose(window))
    {
    // メインループ
    }
```

この中に imgui の Widget の定義などを書いていきます。

```cpp
        {
            ImGui::SetNextWindowSize(ImVec2(520, 600), ImGuiCond_FirstUseEver);
            ImGui::Begin("Debug");

            ImGui::InputDouble("Distance", &this->dist);
            ImGui::InputDouble("Tilt", &this->tilt);
            ImGui::InputDouble("Pan", &this->pan);

            if (this->camMode == CameraMode::OFF)
                ImGui::Text("CamMode::OFF");
            if (this->camMode == CameraMode::TUMBLE)
                ImGui::Text("CamMode::TUMBLE");
            if (this->camMode == CameraMode::TRUCK)
                ImGui::Text("CamMode::TRUCK");
            if (this->camMode == CameraMode::ZOOM)
                ImGui::Text("CamMode::ZOOM");

            ImGui::InputDouble("MousePosX", &this->mouse_pos_X);
            ImGui::InputDouble("MousePosY", &this->mouse_pos_Y);

            ImGui::End();
        }
```

![](https://gyazo.com/5fbdb084fff8b97aacfc4eba7bf9bdea.gif)

実験用に Widget を作り、そこに現在のマウス位置を表示したり、Zoom/Pan/Tilt の
値をいじれるようにしてみました。
Imgui は、メインループ内で都度評価がされるので、PySide とかに比べても
コード量が圧倒的に少ないのが良いです。

```cpp
        ImGui::Render();

        ImVec4 clear_color = ImVec4(0.45f, 0.55f, 0.60f, 1.00f);

        int display_w, display_h;
        glfwGetFramebufferSize(window, &display_w, &display_h);
        glViewport(0, 0, display_w, display_h);

        glEnable(GL_DEPTH_TEST);
        glDepthFunc(GL_LESS);
        glClearColor(clear_color.x, clear_color.y, clear_color.z, clear_color.w);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        glEnable(GL_DEPTH_TEST);

```

そして、次に glViewport の各種設定をして

```cpp
        double moveX = this->_lastX - this->mouse_pos_X;
        double moveY = this->_lastY - this->mouse_pos_Y;

        // カメラの移動
        if (this->camMode == CameraMode::TUMBLE)
            this->_cam.Tumble(moveX * 0.25, moveY * 0.25);

        if (this->camMode == CameraMode::TRUCK)
            this->_cam.Track(moveX * 0.25, moveY * -0.25);

        if (this->camMode == CameraMode::ZOOM)
            this->dist += -0.5 * (moveX + moveY);

        // 前のカメラの数値を保存
        this->_lastX = this->mouse_pos_X;
        this->_lastY = this->mouse_pos_Y;

        this->_cam.SetDist(this->dist);
        this->_cam.PanTilt(this->pan - currentPan, this->tilt - currentTilt);

        currentPan = this->pan;
        currentTilt = this->tilt;

        GfFrustum frustum = this->_cam.GetFrustum();
        GfVec3d cam_pos = frustum.GetPosition();
```

Callback で取得したキー入力やマウス情報を使用して
各種カメラの移動を実行します。
\_cam が、前回の記事で作成した SimpleCamera で
現在のキー入力状態をもとに、 Tumble Truck Zoom の処理を行い
前回のフレームからの移動値をセットします。

そして、最後に viewMatrix と projectionMatrix を取得するために
Camera から、GefFrustum で視錐台を取得します。

```cpp
        GlfSimpleLightVector lights;
        GlfSimpleMaterial material;
        GfVec4f ambient(GfVec4f(.1f, .1f, .1f, 1.f));
        GlfSimpleLight l;
        l.SetAmbient(GfVec4f(0, 0, 0, 0));
        l.SetPosition(GfVec4f(cam_pos[0], cam_pos[1], cam_pos[2], 1.f));
        lights.push_back(l);

        material.SetAmbient(GfVec4f(.1f, .1f, .1f, 1.f));
        material.SetSpecular(GfVec4f(.6f, .6f, .6f, .6f));
        material.SetShininess(16.0);

```

そして、ビューポート用の仮のライトと material を作成し、
カメラポジションにライトを配置します。

```cpp
        renderer->SetRenderViewport(GfVec4d(0, 0, display_w, display_h));
        renderer->SetCameraState(frustum.ComputeViewMatrix(),
                                 frustum.ComputeProjectionMatrix());
        renderer->SetLightingState(lights, material, ambient);

        UsdPrim root = stage->GetPseudoRoot();
        renderer->Render(root, renderParams);
```

最後に、ビューポートの矩形を指定し、
カメラを指定し、
ライトを指定し、
レンダリング対象の Stage のルートプリムと renderParams を指定して終了です。

![](https://gyazo.com/f8d1d25a2d4eb8ec940ec8206a7081e8.png)

あとはビルドして exe を作り、実行すると
このようなツールが完成しました。

## まとめ

C++のビルド、実装方法など、ほぼ 0 状態からやったためかなり時間がかかりましたが
とりあえず動くものが無事出来上がりました。

まだまだ改善したり、勉強したりすることはありますが
まずはスタート地点にはこれたので今回はここまでにしておきます。
引き続き C++の学習は続けていきたいなぁと思います。

https://github.com/fereria/usdViewportSample

サンプルコードは Github にアップしました。
