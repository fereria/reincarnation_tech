# MayaPySideで重複Windowを出さない方法（改

<!-- SUMMARY:MayaPySideで重複Windowを出さない方法（改 -->

http://flame-blaze.net/archives/4703  
  
以前自分のBlogで、MayaのWindowを重複させない方法というのを書いたのですが  
これだと一部問題があるので、問題ないように修正してみました。  
  
## 以前の方法

```python
class testUI(QtGui.QDialog):
 
    def __init__(self):
            
        QtGui.QDialog.__init__(self,getMayaWindow())
        #すでにUIが出来てる場合は削除する
        [x.close() for x in self.parent().findChildren(self.__class__)]
 
        btn    = QtGui.QPushButton("Hello World")
        layout = QtGui.QVBoxLayout()
        
        layout.addWidget(btn)
        self.setLayout(layout)
```
以前の方法はこんな感じ。  
なにをしているかというと、  
  
1. 自分自身の親（MayaのMainWindow）を取得して
2. そのMainWindowの子Windowを取得して
3. そのうち、自分のクラスオブジェクトと同じオブジェクト（別に開いてるWindow）を取得して
4. Closeする

ということをしています。  
  
このparent()関数は、Dialogの__init__の第一引数でしている親Windowを取得  
してくれる関数で、↑のサンプルでいうところの  
  
```python
def getMayaWindow():
    """
    Get the main Maya window as a QtGui.QMainWindow instance
    @return: QtGui.QMainWindow instance of the top level Maya windows
    """
    ptr = omUI.MQtUtil.mainWindow()
    if ptr is not None:
        return shiboken2.wrapInstance(long(ptr), QtWidgets.QMainWindow)
```
shiboken2を使ってMayaの本体のQMainWindowで取得している  
Windowを、parent()で再度取得している形になります。  
  
一応これでも閉じるのですが、  
MayaのScriptEditor上で実行した場合や  
.pyでImportしている場合でreloadをした場合  
クラスのIDが変わってしまうらしく、同じクラス名でも別クラス扱いになってしまい  
findChildren関数が動かないという問題がありました。  
(低音さん(@rateionn) が原因を見つけてくれました、感謝)  
  
## 改善版

というわけで改善版

```python
class testUI(QtWidgets.QDialog):
 
    def __init__(self):
        super(testUI,self).__init__(getMayaWindow())
        # すでにUIが出来てる場合は削除する #
        # ＭａｙａのＭａｉｎＷｉｎｄｏｗの子Ｗｉｎｄｏｗを取得
        child_list =  self.parent().children()
        for c in child_list:
            # 自分と同じ名前のUIのクラスオブジェクトが存在してたらＣｌｏｓｅする
            if self.__class__.__name__ == c.__class__.__name__:
                c.close()
        # ------------------------ #
        btn = QtWidgets.QPushButton("Hello World")
        layout = QtWidgets.QVBoxLayout()
 
        layout.addWidget(btn)
        self.setLayout(layout)
```
findChildrenで、指定クラスの子を探すのではなく  
全ての子オブジェクトのクラス名で判定して、同じなら閉じるようにすれば  
reloadしようがScriptEditorで実行しようが問題ありません。  
