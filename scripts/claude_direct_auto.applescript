-- ClaudeCode直接自動化スクリプト
-- 確認ダイアログを自動でYESに応答

on run
    -- ログファイル設定
    set logFile to (path to home folder as string) & ".mirralism:claude_direct_auto.log"
    
    -- 自動化開始ログ
    writeLog("🤖 ClaudeCode直接自動化開始", logFile)
    
    repeat
        try
            -- ClaudeCodeのウィンドウを確認
            tell application "System Events"
                set claudeProcesses to every process whose name contains "claude"
                
                repeat with claudeProcess in claudeProcesses
                    try
                        tell claudeProcess
                            set claudeWindows to every window
                            
                            repeat with claudeWindow in claudeWindows
                                try
                                    -- 確認ダイアログを検索
                                    tell claudeWindow
                                        set dialogButtons to every button whose name is in {"Yes", "はい", "OK", "確認", "実行"}
                                        
                                        if (count of dialogButtons) > 0 then
                                            -- Yesボタンをクリック
                                            repeat with dialogButton in dialogButtons
                                                click dialogButton
                                                writeLog("✅ 自動クリック実行: " & (name of dialogButton), logFile)
                                            end repeat
                                        end if
                                    end tell
                                end try
                            end repeat
                        end tell
                    end try
                end repeat
            end tell
            
        on error errorMessage
            writeLog("⚠️ エラー: " & errorMessage, logFile)
        end try
        
        -- 0.3秒待機
        delay 0.3
    end repeat
end run

-- ログ書き込み関数
on writeLog(message, logFilePath)
    try
        set currentTime to (current date) as string
        set logEntry to "[" & currentTime & "] " & message & return
        
        set logFileRef to open for access file logFilePath with write permission
        write logEntry to logFileRef starting at eof
        close access logFileRef
    on error
        try
            close access file logFilePath
        end try
    end try
end writeLog