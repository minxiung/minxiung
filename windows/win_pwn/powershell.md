# 查詢自己的PS版本
指令:

`$PSVersionTable.PSVersion`

```PS
Major  Minor  Build  Revision
-----  -----  -----  --------
5      1      19041  1320
```

# 顯示相關 PowerShell 版本資訊的雜湊表：
`$PSVersionTable`
```
Name                           Value
----                           -----
PSVersion                      5.1.19041.1320
PSEdition                      Desktop
PSCompatibleVersions           {1.0, 2.0, 3.0, 4.0...}
BuildVersion                   10.0.19041.1320
CLRVersion                     4.0.30319.42000
WSManStackVersion              3.0
PSRemotingProtocolVersion      2.3
SerializationVersion           1.1.0.1
```

# PowerShell 命令 (Cmdlet)
PowerShell 的命令稱為 Cmdlet，Cmdlet 是原生的 PowerShell 命令，而不是獨立的可執行檔。 Cmdlet 會收集到可依需求載入的 PowerShell 模組。 您可以用任何編譯的 .NET 語言或 PowerShell 指令碼語言本身來撰寫 Cmdlet。

## Cmdlet 名稱
PowerShell 會使用 動詞-名詞 名稱組來命名 Cmdlet。例如，`Get-Command` 是用來取得命令 shell 中註冊的所有 Cmdlet。 
指令動詞會識別 Cmdlet 執行的動作，而名詞會識別 Cmdlet 執行其動作的資源。


# 執行原則
相對於普遍的看法，PowerShell 中的執行原則並非安全性界限。 其設計目的是要防止使用者在不知情的情況之下執行指令碼。 已確定的使用者可以輕鬆略過 PowerShell 中的執行原則。 表 1-2 顯示目前 Windows 作業系統的預設執行原則。

|||
|:-:|:-:|
Windows作業系統版本   |      預設執行原則  
Server 2019	         |        遠端簽署  
Server 2016	         |        遠端簽署  
Windows 10	         |       Restricted    
  
檢查目前的執行原則：
`$PSVersionTable`

```
Unrestricted
```

當執行原則設定為 Restricted 時，就無法執行 PowerShell 指令碼。 這是所有 Windows 用戶端作業系統上的預設設定。 若要示範此問題，請將下列程式碼儲存為名為 Stop-TimeService.ps1的 .ps1 檔案。