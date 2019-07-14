# VSCodeでリモートデバッグ環境を作る

<!-- SUMMARY:VSCodeでリモートデバッグ環境を作る -->

Mayaのエディット環境再構築の一環で、VSCodeのリモートデバッグを出来るようにしました。  
  
手順については、概ね  
  
https://qiita.com/takumi_akashiro/items/5e18dd96b7af942cefbc  
  
こちらのサイト様を参考にしました。  

## ptvsdモジュールのインストール

まず、Maya側にVSCodeのリモートデバッグを実行するためのモジュールを追加します。  
  
https://pypi.org/project/ptvsd/#files

このサイトのptvsd-4.2.10.zipをダウンロードしてインストールを行います。  
Python2系のサポート終了が近い影響なのか、各所で公開されているwhlなどからWindowsが消えていて  
若干インストールに戸惑うところがあります。  
はやくMaya様も3系にならないかなとおもうんですが、それによるスタジオの悲鳴を考えると......  
  
インストール方法はそのままコピペでもOKですが、  
私はダウンロードしたptvsd-4.2.10.zipを解凍してできたフォルダに  
管理者モードのコマンドプロンプトで入り、  

```
"C:\Program Files\Autodesk\Maya2018\bin\mayapy.exe" setup.py install
```

setup.pyを利用してインストールしました。  
  
## デバッグモードを設定する  
  
![](https://gyazo.com/db1dc29358c0bd83655b0a4f53156975.png)

VSCodeのDebug画面に移動して、「構成の追加...」をクリックします。  

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Maya: Attach",
            "type": "python",
            "request": "attach",
            "pathMappings":[{
                "localRoot": "${workspaceFolder}",
                "remoteRoot": "${workspaceFolder}",
            }],
            "port": 3000,
            "host": "127.0.0.1"
        }
    ]
}
```

launch.jsonを上のように書き換えます。  
  
```python
import ptvsd;ptvsd.enable_attach(address=('127.0.0.1', 3000), redirect_output=True)
```
最後に、userSetup.py内にリモートデバッグを有効にするためのコマンドを記入して準備は終了。  
  
## 使用する


準備ができたら、

![](https://gyazo.com/4be95dfcdf0e17f8535011b8559dc76e.png)

デバッグを「Maya:Attach」に変更して、「F5」を押します。

![](https://gyazo.com/f92904583a016f9487672ad10a2be48b.png)

これで待機状態になります。  
  
あとは、Maya側で

![](https://gyazo.com/3fb0a1efb5fdc869e778346a5a298f68.png)

コマンドを実行すれば  
  
![](https://gyazo.com/c9d9a4a5cf879a5a24b28d704c4f8dca.png)

ブレークポイントのところでVSCode側でデバッグをすることができます。

## 使用感

使用感ですが、以前使っていたPyCharmのリモートデバッグよりシンプルで  
使いやすいきがします。  
PyCharmだと、一度接続して切ったらいろいろゴニョゴニョしないと次の実行が  
できなかったのですが  
VSCodeは使用時は特に何事もなく、終了したあとに再度実行すれば  
同じようにリモートデバッグが実行できました。  
  
