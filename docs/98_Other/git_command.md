# Gitよく使うコマンドやら操作メモ

<!-- SUMMARY:Gitよく使うコマンドやら操作メモ -->

今回はGitLabを使用して、Gitの基本的なフローについてメモしておきます。  
おおむね自分用のメモ。  
  
http://remi-saba.net:30000/testGroup/gitTest

テストに使うのはこのリポジトリ。  
GitLabは、自分で作ったリポジトリを自分でフォークすることは出来ないので  
まずはGroupを作成し、そのGroup下にフォーク元のリポジトリを作成します。  
  

## フォークする

![](https://gyazo.com/556611ea36841633526e777d7b1f0707.png)

まずはフォーク。  
フォーク元リポジトリのForkボタンをクリックして  

![](https://gyazo.com/95053ba22dda0934b6461b30938c6824.png)

自分のアカウントをクリック。  
そうすると、指定のリポジトリをフォークすることができます。  
  
以降は、まずフォークしたリポジトリに対してデータをアップしていきます。  
  
## 基本的な操作

### 現在のブランチを確認する

```
git branch
```

![](https://gyazo.com/1f6cb3de65eb4542ccf75a68280943c1.png)

### ブランチを作る

```
git checkout -b hogehoge
```

### ブランチを切り替える

```
git checkout hogehoge
```

checkout ##### で、指定した名前のブランチに切り替わる。  
切り替えるときに、現在のブランチに編集済のファイルが存在する場合は

![](https://gyazo.com/c77c3523202e7e7b9b484803ca04bd8a.png)

エラーになってしまうので、コミットするかStash（一時退避場所）に逃がしておく必要がある。

### Stash（一時退避場所）にアップする

![](https://gyazo.com/95baa15f5178b3907ab2d0d6abd08ee7.png)

```
git stash
```

一時的に逃がす場合はStashに入れる。  

### コミット～プッシュする

編集結果をGitのリモートリポジトリにアップする

```
git add hogehoge.txt
git commit -m "hogehoge"
git push -u origin hogehoge
```

アップするには、まず add を使用して「変更した」というフラグを立てる。  
そしてアップ対象をセットしたら、 commit で、ローカルリポジトリにコミットする。  
-m で、コメントを記入する。  
最後にリモートリポジトリにPushする。  
  
Pushするときのコマンドは git push -u ローカルリポジトリのBranch名 リモートリポジトリのBranch名  
のようにする。  
-u は、リモートリポジトリに街灯のブランチが存在しない場合は自動で作るというフラグ。  

![](https://gyazo.com/bbe73212bdf4c31e622b9bc63cd20130.png)

実行すると、無事リモートリポジトリに適応された。  
  
### プルリクを作る

フォークしたリポジトリの変更内容を、フォーク元に対してマージするために  
プルリクを作成します。  
  
![](https://gyazo.com/e746c3469607631513920e5bedd8fab8.png)

フォークしたページにある「Merge Requests」をクリックして  
  
![](https://gyazo.com/1c2b357d33900c3666ea0c3339188a5a.png)

New Merge Request を押します。  
  
![](https://gyazo.com/c12d442de7bd105c272bab8b70920c88.png)  
  
SourceBranchには、フォークしたリポジトリとブランチを指定し  
ターゲットブランチにはフォーク元のリポジトリとマージしたいブランチを指定します。  
  
あとはコメントを記入して Submit merge Request を押します。

### マージする

![](https://gyazo.com/f7e7b9bebfe370cff0bcefdbd874a554.png)

プルリクが作成されると、Group側にリクエストが追加されます。  
ここでコードレビューを行い、問題がなければマージを押します。  
  
### マージされたGroupのリポジトリをFork先にマージする

Groupに自分のプルリクがマージされたら、その結果を自分のForkしたリポジトリに適応します。  
  
```
git checkout master
```
まずはmasterブランチに切り替えて  

```
git remote add upstream <URL>
```

remoteに、Group側のURLを追加します。  
  
![](https://gyazo.com/d741139c9500af6a2c7f45612cdf20ca.png)

追加すると、Remoteに upstream が追加されます。  
  
```
git fetch upstream
```
追加したリモートをFetchして

```
git pull
git merge upstream/master
```
upstreamのmasterを自分のmasterにマージします。  
  
![](https://gyazo.com/5577f0c9aa30fb4c277f87d028838a6b.png)

変更内容が取り込まれました。  
めでたしめでたし。

  
## GUIを使用する

コミットやPushは、コマンドでやるとステージするのが面倒だったり  
コメントを日本語で入れるのが面倒だったりするので、  
GUIを使用します。

```
git gui
```
![](https://gyazo.com/1a9f38cca286d2d43ab0989e02760827.png)

addするのとかはコマンドでやるのは地味にめんどくさいけど、GUIならわりと楽。  
UnstagedChangesにファイルがある状態で「Stage Changed」するとコミットできる状態になるので  
コメントを記入してCommitする。  
  
![](https://gyazo.com/c4a46c2bba19ca29ebeef0e2f4871ffa.png)

あとはPushすればおしまい。  
  
### 編集履歴を確認する

![](https://gyazo.com/afdbc1ddbe70c5f7eeb982a5ec680a1d.png)

VisualizeAllBranchHistoryで、変更を確認できる。  
  
![](https://gyazo.com/9a7109ed85b938889e6ea94984c74abc.png)

## ローカルブランチをマージする

ローカルブランチで、別ブランチを切った状態で作業しているときに  
ほかのブランチをマージしたい場合は、とりこみ先でチェックアウトをして
```
git merge 取り込みたいリポジトリ名
```
これで、リポジトリを現在のブランチにマージすることができる。

## ローカルリポジトリとリモートリポジトリで衝突した場合

衝突してしまったら、まずローカル側を逃がしてからPullしてマージする。

```
git stash
git stash list
```

まず、現在の編集情報をStashに逃がす。

```
git pull
```

そしてリモートの状態をPullして最新の状態にする

```
git stash pop
```
Stashに入れてた内容を元に戻す。  
取り出したらコンフリクトが発生するので、必要に応じてマージしてからコミットする。  
マージ処理はわりと自動でやってくれる。  
してくれないばあいは自力で編集する。  
  
