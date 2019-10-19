# Markdownの書き方サンプル

1. aaa
2. bbb

----

```python
print "hello World"
```

```
pip install mkdocs
```

!!! Warning
    わーにん！わーにん！
    
!!! Note
    これはノートです。    


++ctrl+alt+delete++

:fa-external-link: [MkDocs](http://www.mkdocs.org/)

:smile:  
:fa-coffee:

==MARK TEST== hogehoge  

![](https://gyazo.com/42ff00b4fe5ad7bc8e1742cdad3aaafc.png)

## 参考
  
  * https://qiita.com/mebiusbox2/items/a61d42878266af969e3c


```plantuml format="png" classes="uml myDiagram" alt="My super diagram placeholder" title="My super diagram" width="300px" height="300px"

@startuml

up -up-> right
-right-> down
-down-> left
-left-> up

@enduml  
```

```plantuml
@startuml

:hello world;
:hoge hoge;

if (condition A) then (yes)
  :text ;
else (no)
  :textB ;
endif
:hoge ;

repeat
  :hoge ;
  :hoge2 ;
repeat while (condition)

floating note left : this is a note

while (hogehoge)

  :hogeB;
  :hogeC;

end while

:end hoge;

note right
  note
end note

#hotpink: hogehoge;

:hoge>
-[#blue]->
:hoge<
-[#blue,dotted]->
:hoge|
-[#red,bold]->
:hoge/

fork
 :hoge;
 :hoge2;
fork again
 :hogeB;
 :hogeC;
endfork

stop


@enduml
```



{{color(red)::some_text}}  
{{color(blue)::some_text}}

