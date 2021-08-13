# IK を作成する

<!-- SUMMARY:IKを作成する -->

![](https://gyazo.com/ff7bd2ca0ae1c343631a5e7c4ab8ab37.png)

まず、Armature を作成し  
IK を貼る Bone を作成する。

![](https://gyazo.com/43c0a5302a23038bac125866d3d8d21a.png)

IK を貼りたいときは、「Pose モード」に切り替えて  
IK の末端の Bone を選択する。

![](https://gyazo.com/194c54483af6822f0c36012e5ce0f997.png)

次に、プロパティパネルで BoneConstraint を開く。

![](https://gyazo.com/cdd364d0cb170238e75d46ca8343eb3f.png)

その中から「Inverse Kinematics」を選択する。

![](https://gyazo.com/594fb08aa2cb52789304ec0e79d9e9ed.PNG)

最後に、IK を動かすためのコントローラーとポールベクターのターゲットを作成する。

![](https://gyazo.com/abb12b350e1a89eb8ffdf2546d3ea5ec.png)

Target には IK を動かすためのロケーター、PoleTarget にはポールベクターのターゲットロケーターを指定する。

![](https://gyazo.com/1d0691f263349f24d3510bdc1c277332.gif)

!!! info 
    PoleTarget をいれただけだと角度がズレてしまうので、現状 90 度を入れている。  

