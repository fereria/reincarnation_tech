# VSCode のタスクを作成する

<!-- SUMMARY:VSCode のタスクを作成する -->

![](https://gyazo.com/c7ebaf071cf1ffe0c835d38d781bacac.png)

まず、VSCode のパレットから、タスクの構成を実行する。

![](https://gyazo.com/800a0590ab7215475dea29e6206c1bca.png)

実行すると、テンプレートからタスクを作成　というのがでるので、

![](https://gyazo.com/fe1fd7ba416b939555a4c4723e436d5f.png)

Others で任意の外部コマンドを実行出来るようにする。

![](https://gyazo.com/ccd4fa6d92357e6fc1b38c56fe5c179f.png)

実行すると、.vscode 下に task.json が作成される。

```json
{
  // See https://go.microsoft.com/fwlink/?LinkId=733558
  // for the documentation about the tasks.json format
  "version": "2.0.0",
  "tasks": [
    {
      "label": "echo",
      "type": "shell",
      "command": "echo Hello"
    }
  ]
}
```

実行すると、テンプレートが作成される。

![](https://gyazo.com/1737d881997af08ffa72765bf9d2da2c.png)

作成ができたら、**タスクの実行** を実行し、

![](https://gyazo.com/f2d8f253f630c4a6dbc8af5459a5063b.png)

作成したタスクを実行する。

![](https://gyazo.com/8a3e3f19ed14f6b964fd976bcf6c9872.png)

とりあえずタスクの出力をスキャンせずに続行を実行する。

![](https://gyazo.com/b5e250e59deaac20e445491c602c7992.png)

実行すると、コンソールに結果が表示される。  
ここで実行されるのは、task.json 内で指定した command がコンソール上で実行される。

## ためしにタスクを作って見る

Gitbook のサマリーを自動作成するタスクを作成。

```create_summary.bat
book sm -r docs
```

まずは普通にサマリーを作成する。  
ただし、このコマンドで作成すると、現在の ROOT を基準にして階層を作るため  
一端 docs 下にサマリーを作り、その後ルートに移動させたい。

```update_summary.bat
call create_summary.bat
move %~dp0\docs\SUMMARY.md %~dp0\SUMMARY.md
```

ただ、1 つのコマンドで実行すると book コマンドを実行したところで処理が止まってしまうので  
別の bat を作成して、call で呼び出し。  
その実行後、作成したサマリーをルートに移動する。

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "update_summary",
      "type": "shell",
      "command": "update_summary"
    }
  ]
}
```

最後に、tasks.json の中身を編集する。  
このコマンドの実行は、現在の VSCode のプロジェクトになっているので  
コマンド部分を batch ファイル名にすれば OK。

毎度設定するのはめんどくさいので、簡単に実行出来るように  
ビルドタスクに指定する。  
その場合は、tasks.json 内の task の{}内に

```json
      "group": {
        "kind": "build",
        "isDefault": true
      }
```

を追加する。

## 参考

- https://qiita.com/suzuki_sh/items/968ba9aeb312c8742f4e
