---
title: mermaidで作図をする
---

## 基本

```mermaid
graph LR
    A --> B
```

graph 以下にインデントで実際のグラフを表記する。
LR というのは 横方向のノードになり、

```mermaid
graph TB
    A --> B
```

TB(Top to Bottom)とすると、縦方向のグラフになる。

## ノード形状

```mermaid
graph LR
    id1(This is the text in the box)
    id2[This is the text in the box]
    id3[[This is the text in the box]]
    id4[(Database)]
    id5((Circle))
    id6>This is the text in the box]
    id7{This is the text in the box}
    id8{{This is the text in the box}}
    id9[/This is the text in the box/]
    id10[\This is the text in the box\]
    id11[/Christmas\]
    id12[\Go shopping/]
```

```
graph LR
    id1(This is the text in the box)
    id2[This is the text in the box]
    id3[[This is the text in the box]]
    id4[(Database)]
    id5((Circle))
    id6>This is the text in the box]
    id7{This is the text in the box}
    id8{{This is the text in the box}}
    id9[/This is the text in the box/]
    id10[\This is the text in the box\]
    id11[/Christmas\]
    id12[\Go shopping/]
```

ノード形状を指定したい場合は、ID[Text] や ID((Text)) のような
カギカッコの組み合わせによって指定できる。

## →の接続


```mermaid
graph LR
    
    A[hello]
    B[world]
    C[hoge]
    D[fuga]
    
    A --> B
    B --- C
    C ---|Text| D
    D -- Text --- A
```

```
graph LR
    
    A[hello]
    B[world]
    C[hoge]
    D[fuga]
    
    A --> B
    B --- C
    C ---|Text| D
    D -- Text --- A
```

ノードの定義と→野定義は別に書くことができる。
→の間に文字を挟むには **NodeA ---|文字|NodeB** あるいは **NodeA -- Text --- NodeB** のようにする。

```mermaid
graph LR
    
    A[hello]
    B[world]
    C[hoge]
    D[fuga]
    
    A -.-> B
    B ==> C
    C -. text .-  D
    D -- Text --- A
```

```
graph LR
    
    A[hello]
    B[world]
    C[hoge]
    D[fuga]
    
    A -.-> B
    B ==> C
    C -. text .-  D
    D -- Text --- A
```
矢印のスタイルは色々変えられる。

## Subgraph

```mermaid
graph TB
    A[hello]
    B[world]
    C[hoge]
    D[fuga]
    OUT[out]
    
    OUT --> A
    subgraph sampleA
    A --> B
    end
    subgraph sampleB
    C --> D
    end
```

```
graph TB
    A[hello]
    B[world]
    C[hoge]
    D[fuga]
    OUT[out]
    
    OUT --> A
    subgraph sampleA
    A --> B
    end
    subgraph sampleB
    C --> D
    end
    
```

```mermaid
graph LR
    subgraph s1
        A --> B
    end
    subgraph s2
        C --> D
    end
    D --> A
```

## 見た目の調整

```mermaid
graph LR
    A:::someclass --> B
    classDef someclass fill:#f96;
```

classDef name style で、見た目のスタイル定義ができる。

## 色々実験

```mermaid
graph TB
    Start
    A{A}
    Yes
    No
    End
    LoopStart[/Start\]
    HogeHoge
    LoopEnd[\End/]
    
    Start --> A
    A --Yes--> Yes
    A --No--> No
    No --> Start
    Yes --> LoopStart
    subgraph loop
    LoopStart --> HogeHoge
    HogeHoge --> LoopEnd
    end
    LoopEnd --> End

```

```mermaid
stateDiagram
    [*] --> Still
    Still --> [*]

    Still --> Moving
    Moving --> Still
    Moving --> Crash
    Crash --> [*]
```

```mermaid
    stateDiagram-v2

        State1: Sample
        note right of State1
        Hoge Hoge
        end note
        State2: Sample2
        note left of State2
        Fugafuga
        end note
        State3: Sample3
        state One{
            State1 --> State2
            State2 --> State3
            State3 --> [*]
        }
```
