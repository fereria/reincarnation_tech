---
title: mkdocsにJupyterNotebookの結果(ipynb)を表示する
---

表題の通り。  
最近各種コマンドのテストをJupyterNotebook＋VSCodeでやることが多いのですが  
その結果となるipynbのイイカンジの共有方法が見つからないというか  
この結果をmkdocsのこのWebページにおいておきたかった。。。が、  
いいかんじに埋め込む方法がない。  
  
最初考えたのはHTML化して埋め込むとか、  
ipynbをCacherにUPしてそこでエンコードして表示するとか  
GitHubにUPするとか  
考えたのですが、ipynbそのままUPすると表示までえらくラグが発生してイライラ。。。  
  
そしたら、mkdocsにそのままコンバートしてUPできるプラグインがあったので  
ソレを参考に自分で作って見ることにしました。  
  
## nbconvertを使う  

まず、ipynbをmarkdownに変換します。  
これは公式で使えるコマンドライン  

```
jupyter nbconvert --to markdown --output <PATH> <ipynbファイルPATH>
```

これで変換できます。  
なので、とりあえずdocsと同じ階層に notebook フォルダを作り  
そのフォルダ階層を、docs下の notebookフォルダに対してmarkdown出力するようにして  
その後にmkdocsのビルドをするようにします。  
  
が、  
そのままだと見た目がよろしくないのと  
markdownのタイトルに日本語がつけられないので  
  
ipynbのファイル名は  
  
markdownName__日本語のタイトル名.ipynb  
  
にして、markdown出力後にtitleを仕込むようにしました。

## Jinjaテンプレート

出力されるmarkdown側は、--template 引数に対してjinjaテンプレートで作成した  
テンプレートを設定することで、自分で見た目をカスタマイズすることができます。  
  
ので、とりあえずmarkdownのテンプレートを作って見ました。

<script src="https://embed.cacher.io/d8516ed40d63f842aead47915f2b4ca02a09ae46.js?a=ae7cea5f84ed07f91d22771e2bd04f81"></script>

テンプレートの作り方は、  
まずは基本となるテンプレートをインポートし、上書きしたいブロックを追加していきます。  
  
https://nbconvert.readthedocs.io/en/4.2.0/customizing.html  
  
上書きするブロック名などはここを参考にしました。  
  
カスタマイズポイントは、JupyterのCellごとに番号を入れることと  
SuccessとError部分はわかりやすくブロック化すること。  
  
![](https://gyazo.com/1cd022f093b0406ca828c81190aab219.png)

完了はこうだし、  

![](https://gyazo.com/2372df7122bd85dc5b5f5fe518168e3d.png)

エラーの場合、こんな風に表示されます。  
  
```python
# -*- coding: utf-8 -*-
import nbconvert
import nbformat
import codecs
import subprocess

import os.path
import re
import glob
import shutil

BLOG_ROOT_DIR = "C:/reincarnation_tech"


def createNoteBookMD(ipynbFile, root, exportPath):

    ipynbFile = re.sub("\\\\", "/", ipynbFile)
    ipynbFile = ipynbFile.replace("//", "/")
    root = re.sub("\\\\", "/", root)
    root = root.replace("//", "/")

    bn = os.path.splitext(os.path.basename(ipynbFile))[0]
    # FileNameは En__Title にする。
    # __がなければファイル名とタイトルは同じ。
    buff = bn.split("__")

    if len(buff) > 1:
        fileName = buff[0] + ".md"
        title = buff[1]
    else:
        fileName = bn + ".md"
        title = bn

    md_path = re.sub(root, "", os.path.dirname(ipynbFile))
    md = os.path.join(exportPath, md_path, fileName)

    p = subprocess.Popen(['jupyter',
                          'nbconvert',
                          '--to', 'markdown',
                          '--output', md,
                          '--template', f'{BLOG_ROOT_DIR}/jupyter_template.tpl',
                          ipynbFile])

    p.wait()

    title = ['---', f'title: {title}', '---']

    with codecs.open(md, 'r', 'utf8') as f:
        lines = [x.replace("\n", "") for x in f.readlines()]

    lines = title + lines

    with codecs.open(md, 'w', 'utf8') as f:
        f.write("\n".join(lines))


if __name__ == "__main__":

    root = f"{BLOG_ROOT_DIR}/notebooks"
    md = f"{BLOG_ROOT_DIR}/docs/60_JupyterNotebook"

    if os.path.exists(md):
        shutil.rmtree(md, True)
    os.makedirs(md)

    ipynbFiles = glob.glob(root + "/*.ipynb")

    for ipynb in ipynbFiles:
        createNoteBookMD(ipynb, root, md)
```

後はこんな感じでPythonコードを書いて、Deployするコードと同じBatchに

```bat
py -3.6 create_jupyter_markdown.py
py -3.6 create_mkdocs_pages.py
mkdocs gh-deploy
```

こんな感じで書きます。  
create_mkdocs_pages.pyは、mkdocs.ymlに自動でnavカテゴリを追加してくれるコマンドです。  
なので、  
まずipynbからmarkdownを作り、そのmarkdownでNavメニューを作ってくれます。  
  
出来あがったテストページが  
https://fereria.github.io/reincarnation_tech/60_JupyterNotebook/NoteSample/
こちら。  
  
結構見やすいし、セルごとにクリップボードコピーもできるのがGood。  
これでテストしたりとか検証した物は投げ込んでおけばイイカンジのスクリプトメモになりそう。  
  
やはりmkdocsは便利。
