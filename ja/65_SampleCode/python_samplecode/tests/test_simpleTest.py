import pytest


# fixtureを定義すると、テストの引数に同じ関数名が指定されていれば
# fixtureのreturnをテストの引数に渡すことができる
@pytest.fixture
def sample():
    return 'a'


def test_Add():
    a = 1
    b = 2
    assert a + b == 3


def test_AddErr():
    a = 1
    b = 2
    assert a + b != 4


# fixtureで指定した値を引数で受け取る
def test_Fixture(sample):
    assert sample == 'a'
