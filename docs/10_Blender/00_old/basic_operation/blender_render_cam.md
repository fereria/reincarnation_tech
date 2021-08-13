# レンダリングカメラを操作する

<!-- SUMMARY:レンダリングカメラを操作する-->

Blender で ViewCamera（RenderCamera）を Area 表示した状態で  
直接カメラを操作したい場合。

> デフォルトだと、ViewCamera 表示にしたときにカメラを動かすと  
> Persp ビューに切り替わってしまう

1. Ctrl + ALt + 0 を押して、現在の Persp ビューに RenderCamera をフィットさせる

2. SideBar の Camera Lock の Lock Camera to View のチェックを ON にする

![](https://gyazo.com/e5f285cf73252d5a1ce08cb04ac4d413.png)

チェックを ON にすると

![](https://gyazo.com/335458a3091bf0d63e3482468cd0a520.png)

ビューポートに赤の点線が表示される。  
この状態になると、カメラを動かせば ViewCamera を直接動かせるようになる。

![](https://gyazo.com/ad9a560c4376886c40a1717e3ed46c39.png)

この View カメラは、Scenes 設定の「Camera」で指定しているカメラ。
