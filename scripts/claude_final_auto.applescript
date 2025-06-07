-- ClaudeCode最終自動化スクリプト
-- 確実にYESボタンを自動クリック

on run
    set logFile to (path to home folder as string) & ".mirralism:claude_final_auto.log"
    
    -- 開始ログ
    my writeToLog("🤖 ClaudeCode最終自動化開始", logFile)
    
    repeat
        try
            tell application "System Events"
                -- すべてのプロセスをチェック
                set allProcesses to every process
                
                repeat with currentProcess in allProcesses
                    try
                        set processName to name of currentProcess
                        
                        -- ClaudeCode関連プロセスをチェック
                        if processName contains "claude" or processName contains "Claude" or processName contains "Terminal" then
                            tell currentProcess
                                set allWindows to every window
                                
                                repeat with currentWindow in allWindows
                                    try
                                        tell currentWindow
                                            -- YESボタンを探す（複数パターン）
                                            set yesButtons to {}
                                            
                                            try
                                                set yesButtons to yesButtons & (every button whose name is "Yes")
                                            end try
                                            
                                            try
                                                set yesButtons to yesButtons & (every button whose name is "はい")
                                            end try
                                            
                                            try
                                                set yesButtons to yesButtons & (every button whose name is "OK")
                                            end try
                                            
                                            try
                                                set yesButtons to yesButtons & (every button whose name is "確認")
                                            end try
                                            
                                            try
                                                set yesButtons to yesButtons & (every button whose name is "実行")
                                            end try
                                            
                                            try
                                                set yesButtons to yesButtons & (every button whose name is "Continue")
                                            end try
                                            
                                            try
                                                set yesButtons to yesButtons & (every button whose name is "Proceed")
                                            end try
                                            
                                            -- ボタンが見つかったらクリック
                                            if (count of yesButtons) > 0 then
                                                repeat with yesButton in yesButtons
                                                    try
                                                        click yesButton
                                                        my writeToLog("✅ 自動クリック成功: " & (name of yesButton) & " in " & processName, logFile)
                                                        delay 0.1
                                                    on error
                                                        -- クリック失敗は無視
                                                    end try
                                                end repeat
                                            end if
                                            
                                            -- Dialogボックスもチェック
                                            try
                                                set dialogs to every sheet
                                                repeat with currentDialog in dialogs
                                                    tell currentDialog
                                                        set dialogButtons to every button whose name is in {"Yes", "はい", "OK", "確認", "実行", "Continue", "Proceed"}
                                                        repeat with dialogButton in dialogButtons
                                                            try
                                                                click dialogButton
                                                                my writeToLog("✅ ダイアログクリック成功: " & (name of dialogButton), logFile)
                                                            on error
                                                                -- エラーは無視
                                                            end try
                                                        end repeat
                                                    end tell
                                                end repeat
                                            end try
                                            
                                        end tell
                                    on error
                                        -- ウィンドウエラーは無視
                                    end try
                                end repeat
                            end tell
                        end if
                    on error
                        -- プロセスエラーは無視
                    end try
                end repeat
            end tell
            
        on error errorMessage
            my writeToLog("⚠️ システムエラー: " & errorMessage, logFile)
        end try
        
        -- 0.5秒待機（高速応答）
        delay 0.5
    end repeat
end run

-- ログ書き込み関数
on writeToLog(message, logFilePath)
    try
        set currentTime to (current date) as string
        set logEntry to "[" & currentTime & "] " & message & return
        
        set fileHandle to open for access file logFilePath with write permission
        write logEntry to fileHandle starting at eof
        close access fileHandle
    on error
        try
            close access file logFilePath
        end try
    end try
end writeToLog