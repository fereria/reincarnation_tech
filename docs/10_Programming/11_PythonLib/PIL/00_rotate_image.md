---
title: PIL_EXIFの回転情報に合わせて画像を回転する
---

写真の縦・横のように、画像の Exif の Orientation 情報によって
画像の縦・横が設定されている場合、ツールによっては正しく扱えなかったりするので
無理矢理 Exif 無しでも正しくなるように画像を回転して保存するやり方を調べてみました。

この Exif での表示。
たとえば PhotoShop や IfanVIew では正しく見えるのに、Windows デフォルトのビューだと
縦横がおかしく表示されてしまうパターンがあります。

ツールなんかで調べた中だと、ffmpeg で画像をムービー化したいばあい等も
Exif で回転が入っている場合、おかしな感じでムービー化されてしまうようでした。

ということで、この Exif を取っ払って、PIL を使用して回転をします。

まずは、Exif 情報の取得。

https://www.lifewithpython.com/2014/12/python-extract-exif-data-like-data-from-images.html

やり方は、こちらのサイトのコードを使用しました。

画像の向きの Orientation は、整数の 1 ～ 8 で指定することが出来ます。
それだけだと、扱いにくいので、どのぐらい回転するか + ミラー反転するかどうか
に置き換えるような関数を作ります。

```python
def get_exif_rotation(orientation_num):
    """
    ExifのRotationの数値から、回転する数値と、ミラー反転するかどうかを取得する
    return 回転度数,反転するか(0 1)
    # 参考: https://qiita.com/minodisk/items/b7bab1b3f351f72d534b
    """
    if orientation_num == 1:
        return 0, 0
    if orientation_num == 2:
        return 0, 1
    if orientation_num == 3:
        return 180, 0
    if orientation_num == 4:
        return 180, 1
    if orientation_num == 5:
        return 270, 1
    if orientation_num == 6:
        return 270, 0
    if orientation_num == 7:
        return 90, 1
    if orientation_num == 8:
        return 90, 0
```

一応全パターン作りましたが、Exif の設定でミラーリングとか
絶対使わない気がします。

最後に、Exif 情報を取得して画像を回転をして保存します。

```python
def rotation_exif_info(path, to_path):
    """
    画像のexif情報を使用して、画像を回転する
    """

    to_save_path = to_path + "/" + os.path.basename(path)
    if os.path.exists(to_path)  is False:
        os.makedirs(to_path)

    exif    = get_exif_of_image(path)
    rotate  = 0
    reverse = 0
    if 'Orientation' in exif:
        rotate, reverse = get_exif_rotation(exif['Orientation'])

    img = Image.open(path)

    data = img.getdata()
    mode = img.mode
    size = img.size

    with Image.new(mode, size) as dst:
        dst.putdata(data)
        if reverse == 1:
            dst = ImageOps.mirror(dst)
        if rotate != 0:
            dst = dst.rotate(rotate, expand=True)
        dst.save(to_save_path)
```
コードはこんな感じ。

画像のミラー反転は、 PILのImageOps.mirror(obj)
回転は、imgObj.rotate(回転,expand=True)とします。
expand=Trueにすると、元の全画像を見える状態で回転をしてくれるようになります。
Falseの場合、画像サイズは同じになるので、90度回転とかすると、上下が切れて、左右が空いてしまうことになります。

最後に、そのままだと、Exif情報が残ってしまうので、Exif情報を削除するために
新しくPILのImageを作成して、回転した結果をその新しいキャンバスに貼り付けて保存しています。

今回は、Exif入りの画像を扱うときにとおかしくなる問題がでたので
やり方をしらべてみたのですが、
コレをつかうと、
撮影した写真をBlogに載せるときに回転情報がおかしくなってるものなんかを直すのにも使えそうです。

PILとかOpenCVまわりはまだまだ出来ることが多そうなので
色々試してみたいです。