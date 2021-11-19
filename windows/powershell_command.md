# 檔案與資料夾操作教學：建立、複製、搬移、刪除
# 檢查檔案或目錄是否存在:
```PS
# 檢查檔案是否存在
Test-Path -Path C:\OfficeGuide\MyFile.txt
```

若指定的檔案或目錄存在，則 Test-Path 會傳回 True，若不存在的話，則會傳回 False，所以通常我們會搭配 if 判斷式一起使用：
```PS
# 使用 if 判斷式
if (Test-Path -Path C:\OfficeGuide\MyFile.txt) {
  "檔案存在。"
} else {
  "檔案不存在。"
}
```

```PS
# 檢查目錄是否存在
if (Test-Path -Path C:\OfficeGuide) {
  "目錄存在。"
} else {
  "目錄不存在。"
}
```

# 檢查路徑是檔案還是目錄
Test-Path 可以判斷檔案或目錄是否存在，如果要分別一個路徑是檔案還是目錄，可以使用 Get-Item 取得該路徑的資訊，然後依據該資訊檢查是否為目錄：
```PS
# 判斷路徑是否是目錄
if ((Get-Item C:\OfficeGuide) -is [System.IO.DirectoryInfo]) {
  "此路徑是目錄。"
} else {
  "此路徑不是目錄。"
}
```

# 建立檔案或目錄
```PS
# 建立新目錄
New-Item C:\MyFolder -ItemType "directory"
```

```PS
# 建立新檔案
New-Item C:\MyFolder\MyFile.txt -ItemType "file"
```

# 複製檔案或目錄
若要複製檔案，可以使用 Copy-Item 指令：
```PS
# 複製檔案
Copy-Item C:\MyFile.txt -Destination C:\MyFile2.txt
```
若要將檔案複製到指定的目錄下（檔案名稱維持不變），則 -Destination 就指定為目的目錄的路徑即可：
```PS
# 複製檔案至指定目錄
Copy-Item C:\MyFile.txt -Destination D:\MyFolder
```
如果要複製整個目錄（連同裡面的所有檔案），則要加上 -Recurse 參數：
```PS
# 複製目錄
Copy-Item C:\OfficeGuide -Destination C:\OfficeGuide2 -Recurse
```
若要複製的目的檔案已經存在，而且是一個唯讀檔案的話，在複製檔案時就會失敗，若要強制複製檔案，可以加上 -Force 參數：
```PS
# 強制複製檔案
Copy-Item C:\MyFile.txt -Destination C:\MyFile2.txt -Force
```

# 搬移檔案或目錄
若要搬移檔案，可以使用 Move-Item 指令：
```PS
# 搬移檔案
Move-Item C:\MyFile.txt -Destination D:\MyFile2.txt
```

若要搬移檔案至指定目錄（檔案名稱維持不變），則 -Destination 就指定為目的目錄的路徑即可：
```PS
# 搬移檔案至指定目錄
Move-Item C:\MyFile.txt -Destination D:\MyFolder
```

搬移目錄的作法也相同：
```PS
# 搬移目錄
Move-Item C:\MyFolder -Destination D:\
```

# 刪除檔案或目錄
若要移除檔案，則可使用 Remove-Item 指令：
```PS
# 移除檔案
Remove-Item C:\MyFolder\MyFile.txt
```

移除目錄的作法也相同：
```PS
# 移除目錄
Remove-Item C:\MyFolder
```

若要移除的目錄中還有其他的檔案，則在移除的時候 PowerShell 會詢問使用者是否要全部移除，如果不想讓它詢問，可以加上 -Recurse 參數，這樣它就會自動把所有裡面的資料一次刪除：
```PS
# 移除目錄（不詢問、直接移除）
Remove-Item C:\MyFolder -Recurse
```