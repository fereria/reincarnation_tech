# Build 結果をダウンロードする

<!-- SUMMARY:Build 結果をダウンロードする -->

GitLab-CI のビルド結果をダウンロードしたい場合は、
artifacts キーを使用する。

```yml
stages:
  - test_paths

test_paths:
  stage: test_paths
  script:
    - copy nul download_test.txt
  artifacts:
    paths:
      - download_test.txt
```

シンプルな構造はこんな感じ。
artifacts で指定したパス（Git のルート以下のみ指定可）にあるファイルを

![](https://gyazo.com/20b577c43516838842c37dd3176c729f.png)

JOB の実行画面右側の Download 表示をクリックすると

![](https://gyazo.com/8878a97f8159232c822147f01aa87f2d.png)

paths で指定したファイルをダウンロードできるようになる。

## 参考

- https://kore1server.com/351/GitLab+CI%E3%81%AE%E5%9F%BA%E6%9C%AC%E3%83%81%E3%83%A5%E3%83%BC%E3%83%88%E3%83%AA%E3%82%A2%E3%83%AB%EF%BC%88%E7%BF%BB%E8%A8%B3%EF%BC%89
- https://qiita.com/ynott/items/1ff698868ef85e50f5a1
