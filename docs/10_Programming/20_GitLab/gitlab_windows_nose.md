# GitLab CI で nosetests

<!-- SUMMARY: GitLabCIでnosetests-->

まず、 .gitlab-ci.yml を作成する。

```yml
stages:
  - nose_tests

before_script:
  - pip install pipenv
  - pipenv --python 2.7
  - pipenv install nose
  - pipenv shell

nose_tests:
  stage: nose_tests
  script:
    - nosetests
```

環境はクリーンにした状態にしたいので、pipenv で環境を作成する。  
before_script 内で pipenv の基本環境のセッティングを行い、仮想環境を shell でスタートする。

![](https://gyazo.com/d0d2124a1c84c7bb72d6a72fa24dedac.png)

テストするスクリプトは

```py
# -*- coding: utf-8 -*-

def add(num1, num2):
    if (num1 is None):
        raise RuntimeError('num1 is None')
    return num1 + num2
```

簡単なコード。

tests フォルダを作成し、その中に nose を使用したテストコードを作成する。

```py
# -*- coding: utf-8 -*-

from nose.tools import with_setup
from test_repos.add import add

# -----------------------------------------------------#
# テストケース実行前に実行する関数
# -----------------------------------------------------#

def setup_func():
    # 好きなことをする
    print "setup!!"

# -----------------------------------------------------#
# テストケース実行後に実行する関数
# -----------------------------------------------------#

def teardown_func():
    # 好きなことをする
    print "finish!!"

# -----------------------------------------------------#
# 以下テスト関数
# -----------------------------------------------------#

# @with_setupはテストケース前・後に実行する関数を指定 with_setup(前,後)
@with_setup(setup_func, teardown_func)
def test_addNumbers():
    actual = add(-1, 2)
    assert actual == 0
```

準備ができたら、GitLab に Push をする。  
実行すると、Runner の PC でクローンが作成され、その下に pipenv の環境を作成し  
環境ができあがった後に nose のテストが実行される。

![](https://gyazo.com/be78660438cc4e310a8aea552559d33c.png)

実行結果。  
テストがエラーの場合は、

![](https://gyazo.com/6cba4ead31ecf620715762191bc4a70e.png)

CI の結果もエラーとして表示される。

## 注意点

環境にもよるかもしれないが、Runner を実行している PC の Python に  
sitecustomize.py を使用して文字コードを UTF-8 に変更している場合  
unicodeError が表示されてしまい、pipenv install nose を実行したタイミングで  
処理が止まってしまった。

ので、現状は sitecustomize.py は使用せずに実行をしている。
