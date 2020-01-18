---
title: functoolsの使い方
---
**ipynbFile** [functoolTest__functoolsの使い方.ipynb](https://github.com/fereria/reincarnation_tech/blob/master/notebooks/pythonBasic/functoolTest__functoolsの使い方.ipynb)
#### [30]:


```python
# partiald
# 引数を与えた状態の関数を生成する


def hogehoge(*val):
    print(val)


a = functools.partial(hogehoge, 'aaa')

for i in range(10):
    a = functools.partial(a, i)
    a()

```

!!! success
    ```

    ('aaa', 0)
    ('aaa', 0, 1)
    ('aaa', 0, 1, 2)
    ('aaa', 0, 1, 2, 3)
    ('aaa', 0, 1, 2, 3, 4)
    ('aaa', 0, 1, 2, 3, 4, 5)
    ('aaa', 0, 1, 2, 3, 4, 5, 6)
    ('aaa', 0, 1, 2, 3, 4, 5, 6, 7)
    ('aaa', 0, 1, 2, 3, 4, 5, 6, 7, 8)
    ('aaa', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    

    ```


#### [31]:


```python
# デコレータ


def decoTest(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        print("Calling decorated function")
        print(args)
        print(kwargs)
        print("ST")
        ret = f(*args, **kwargs)
        print("END")
        return ret
    return wrapper


@decoTest
def aaa(a, b, c, d=10):
    print("aaa")


aaa(10, 20, 30, d=20)


```

!!! success
    ```

    Calling decorated function
    (10, 20, 30)
    {'d': 20}
    ST
    aaa
    END
    

    ```