---
title: npm の基本
---
# npm の基本

## 基本設定

npm のプロジェクトフォルダにて、

```
npm init
```

このコマンドを実行することで、**この下は npm の管理下におく！！** ということを宣言する。

## パッケージのインストール

このフォルダ内にて、パッケージを使用したい場合は、

```
npm install <package_name>
```

で、インストールすることが出来る。

```
npm install <package_name> --save
```

このようにセーブオプションを追加した状態でコマンドを実行すると、  
同フォルダにある package.json に、パッケージ情報が保存され

```
npm install
```

このように、パッケージ名を入れない場合自動的にインストールできるようになる。

## 参考

- https://qiita.com/hashrock/items/15f4a4961183cfbb2658
