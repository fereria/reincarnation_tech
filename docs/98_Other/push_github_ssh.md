---
title: VSCode から SSH 経由で Push
---
# VSCode から SSH 経由で Push

表題のことをやろうとしたらものすごくハマったのでメモ。

https で PUSH する場合なら問題なくできるのだが、  
その場合、毎度パスワードを聞かれてしまって非常にめんどくさいので  
SSH 化してみた。  
が、

![](https://gyazo.com/327888c5a66c9cdf29d875b371999765.png)

これがでてしまって接続できない。  
うーん。

## SSH の認証用の鍵ファイルを作る

まずは、認証用の鍵を作成する。

コマンドプロンプトで、

```
C:\Users\<user_name>\.ssh
```

に移動して

```
ssh-keygen -t rsa -C "メールアドレス"
```

同フォルダに鍵を作成。  
.ssh フォルダ下に id_rsa.pub ファイルが作成されているので、中に書かれているテキストを  
GitHub に登録する。

![](https://gyazo.com/3707c47a264fdd849b627be403a40843.png)

Settings の SSH and GPG keys をクリックして、

![](https://gyazo.com/d610917d2c3a01fac42e790af97b97a7.png)

New SSH key をクリック。  
Title には　 MyPC 　のようなにのキーなのかを入力し、  
Key に、id_rsa.pub の中身をコピペして、Add SSH Key を追加する。

## config 作成

Git で、ssh を使用して接続するときのオプションを config ファイルに記入する。

```
C:\Users\<user_name>\.ssh
```

下に、config ファイル（拡張子なしのテキスト）を作成。
その中に

```
Host github.com
  User git
  Hostname github.com
  IdentityFile "c:/Users/<user_name>/.ssh/id_rsa"
```

このように書く。  
こうしておくと、github.com で SSH 接続する場合、  
この設定に書かれている id_rsa などの設定で接続できるようになる。
続いて、この config が Git で使われるようにシンボリックリンクを作成する。

```
mklink "C:\Program Files\Git\etc\ssh\ssh_config" "C:\Users\<user_name>\.ssh\config"
```

ssh_config がすでにある場合は、削除する。  
リンクが張られていない場合は、 .ssh 下に config を作成していても  
そもそも使われていなかった。（ハマりポイント１）

## ssh-agent を起動し忘れていた

鍵を作成して config を指定したのに、これでもうまくいかなかった。  
うーむ、なんだろうと調べていったら  
そもそも ssh-add でキーを登録していないと NG だった。  
が、

```
Error connecting to agent: No such file or directory
```

になってしまって、キーを追加することすらできなかった。（ハマりポイント２）  
このエラーが出るときは、Windows のサービスでエージェントが起動していないのが原因だった。

![](https://gyazo.com/d2bfa27ea8e6c065adbc2df15f74e820.png)

Windows のサービスから OpenSSH Authentication Agent のプロパティを開いて  
開始＋スタートアップからも起動できるようにしておく。

ここまでやってから、接続できるかテストしてみる。

```
ssh -T git@github.com
```

こんな感じで実行して、うまくいっていれば

```
Hi fereria! You've successfully authenticated, but GitHub does not provide shell access.
```

GitHub のアカウント名（fereria）とう表示がされる。  
ログイン時の名前は、fereria@github.com のようにしたくなるが、  
この部分のアカウント名は git@で固定なので注意が必要。

接続はできたので、SSH 鍵の登録はおそらく問題はなさそう。  
うまくいかない場合は

```
ssh -vT git@github.com
```

を実行すると、接続のテストを実行することができる。

![](https://gyazo.com/904444b478e9960f94afecc151f1cbb2.png)

public key の読み先が正しいかなども、確認することができる。

## Git の使用する ssh-agent を登録する

コマンドプロンプトのテストなどでも正しく動いているし、Clone も正しく動いているが  
それでも Permission Denied で VSCode で PUSH することができなかった。（ハマりポイント３）

どうやら、Git で上で指定した Windows の OpenSSH ではないものが使用されている場合  
そもそも設定した SSH 設定が使われていないので接続できないようだった。  
ので、Git の設定を変更して、Windows の OpenSSH を使用するようにする。

```
git config --global core.sshCommand "C:/Windows/System32/OpenSSH/ssh.exe"
```

この設定をしたら、無事接続できた。

## 参考

ssh 接続でエラーがでてつながらない -> サービスが起動してない場合、フォルダがない扱いになる

- https://qiita.com/yuta0801/items/d65f1fc3115773861283

config の設定

- https://qiita.com/pakiln/items/bd89ef5cc148a5349964

OpenSSH を使用する設定

- https://qiita.com/hikarin522/items/ae9043412c997597e889
