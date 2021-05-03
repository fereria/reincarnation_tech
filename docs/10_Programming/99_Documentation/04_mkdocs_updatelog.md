---
title: mkdocsの更新履歴を表示する
tags:
    - mkdocs
---

mkdocsの弱点として、いつどこを更新したかを時系列で追うことができない..というのがあります。
（一応Git側を見れば解決するけれどもめんどくさい）

ので、前回作ってみたマクロプラグインを利用して、Gitのコミットログを

![](https://gyazo.com/703daeed5b4232207d4fbecaaaa66d1b.png)

こんな感じで表示するページを作ってみます。

## macroを作る

まずやりたいことは

1. 更新日時順（新しい更新が上）で表示
2. 時間を表示
3. コメントを表示
4. 更新したページへのリンク作成

です。
これを実現するために、必要な処理をマクロに記述します。

今回はGitへのアクセスにGitPythonを使っているので、
```
pipenv install GitPython
```
mkdocsのPython環境にGitPythonをインストールします。
これはGithubActionで自動ビルドするときにインストールする必要があるのでpipenvを使います。
マクロ本体は以下の通り。

```python
import os
import os.path
import re
import codecs
from datetime import datetime
from git import Repo

def define_env(env):
    def getTitle(md):
        if os.path.exists(md):
            with codecs.open(md, 'r', 'utf8') as f:
                for i in f.readlines():
                    if re.search("^title:", i):
                        return i.strip().split(":")[1]
        return None

    @env.macro
    def update_info(num, header="##"):

        repo = Repo(os.getcwd())
        msg = []
        for commit in repo.iter_commits('master', max_count=num):
            dt = datetime.fromtimestamp((commit.committed_date))
            buff = commit.message.split("\n")
            msg.append(f"{header} {dt.strftime('%Y-%m-%d %H:%M:%S')} {buff[0]}")
            msg.append("")
            if len(buff) > 2:
                # 更新コメントがちゃんと書いてあったら詳細を書く
                msg += buff[2:]
            # 更新ページ
            files = commit.stats.files.keys()
            for f in files:
                ext = os.path.splitext(f)[1]
                if ext == ".md":
                    link = re.sub("^docs/", "", f.replace("\\", "/"))
                    title = getTitle(os.getcwd() + "/" + f)
                    if not title:
                        title = link
                    msg.append(f"* [{title}]({link})")
        return "\n".join(msg)
```
Gitのコミットのうち、指定数のコミットを取得して、
日時やコメント、ファイルを取得してmarkdownのテキストを生成し、
その生成した結果を返すようにします。

マクロの準備ができたら、
更新履歴を表示したいところに
```
{{"update_info(5,'###')"|macroprint}}
```
このマクロを書いておきます。
引数で、表示したい履歴数と、目次をつけるときのHeaderの段数を入れておきます。

https://github.com/fereria/reincarnation_tech/blob/master/docs/update_docs.md

今回はトップページと履歴表示専用ページ両方にいれられるようにしたかったので
履歴専用ページは md ファイルを作り、そこにマクロをだけを記述しておきました。

以前はビルド前にmdをスクリプトで無理やり生成して履歴を表示する....
みたいなことをしていましたが、マクロを使うとPython内にシンプルにかけるのでとても便利です。

コミットメッセージがページに表示されるので、
以降はメッセージはちゃんと書いていこうと思います。。。。

## 参考

* https://qiita.com/radiocat/items/31a0f956be522ad8b8e4