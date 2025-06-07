(*
ClaudeCode 自動承認スクリプト (AppleScript版)
==========================================

目的: AppleScriptによるシンプルな自動Yes/OKクリック
方針: 軽量・高速・即座実行可能
作成日: 2025年6月6日

実行方法:
osascript claude_auto_clicker.applescript

または

AppleScript Editor で開いて実行
*)

-- 設定
property scanInterval : 0.5 -- スキャン間隔（秒）
property targetButtons : {"Yes", "OK", "Allow", "Continue", "Proceed", "Confirm", "はい", "許可", "続行", "確認"}
property claudeApps : {"Terminal", "Code", "Claude", "iTerm2", "iTerm"}
property excludedApps : {"System Preferences", "Finder", "System Settings"}

-- グローバル変数
global isRunning
global clickCount
global logMessages

set isRunning to true
set clickCount to 0
set logMessages to {}

-- ログ関数
on addLog(message)
    set currentTime to (current date) as string
    set logEntry to "[" & currentTime & "] " & message
    set end of logMessages to logEntry
    log logEntry
end addLog

-- アクティブアプリケーション取得
on getActiveApp()
    try
        tell application "System Events"
            return name of first application process whose frontmost is true
        end tell
    on error
        return ""
    end try
end getActiveApp

-- Claude関連アプリかチェック
on isClaudeApp(appName)
    repeat with claudeApp in claudeApps
        if appName contains claudeApp then return true
    end repeat
    return false
end isClaudeApp

-- 除外アプリかチェック
on isExcludedApp(appName)
    repeat with excludedApp in excludedApps
        if appName is excludedApp then return true
    end repeat
    return false
end isExcludedApp

-- ボタン検索・クリック
on findAndClickButton()
    try
        set activeApp to getActiveApp()
        
        -- 除外アプリチェック
        if isExcludedApp(activeApp) then return false
        
        -- Claude関連アプリのみ対象（オプション）
        -- if not isClaudeApp(activeApp) then return false
        
        tell application "System Events"
            tell process activeApp
                -- フロントウィンドウの存在チェック
                if not (exists front window) then return false
                
                -- ボタン検索・クリック
                repeat with buttonText in targetButtons
                    try
                        if exists button buttonText of front window then
                            click button buttonText of front window
                            set clickCount to clickCount + 1
                            addLog("自動クリック実行: " & buttonText & " in " & activeApp & " (" & clickCount & "回目)")
                            return true
                        end if
                    on error
                        -- ボタンが見つからない場合は次へ
                    end try
                end repeat
                
                -- ダイアログ内のボタンも検索
                repeat with buttonText in targetButtons
                    try
                        if exists button buttonText of sheet 1 of front window then
                            click button buttonText of sheet 1 of front window
                            set clickCount to clickCount + 1
                            addLog("自動クリック実行(シート): " & buttonText & " in " & activeApp & " (" & clickCount & "回目)")
                            return true
                        end if
                    on error
                        -- シートが存在しない場合は次へ
                    end try
                end repeat
                
            end tell
        end tell
        
        return false
        
    on error errorMsg
        addLog("エラー: " & errorMsg)
        return false
    end try
end findAndClickButton

-- メイン監視ループ
on startMonitoring()
    addLog("🤖 ClaudeCode自動承認監視開始 (AppleScript版)")
    addLog("停止: AppleScript Editor の停止ボタン、またはForce Quit")
    
    repeat while isRunning
        try
            findAndClickButton()
            delay scanInterval
        on error errorMsg
            addLog("監視ループエラー: " & errorMsg)
            delay 1
        end try
    end repeat
    
    addLog("🛑 ClaudeCode自動承認監視終了")
    addLog("総クリック数: " & clickCount)
end startMonitoring

-- 状態表示
on showStatus()
    set statusReport to "📊 ClaudeCode自動承認状態 (AppleScript版)" & return & return
    set statusReport to statusReport & "状態: " & (if isRunning then "✅ 実行中" else "⏹️ 停止中") & return
    set statusReport to statusReport & "総クリック数: " & clickCount & return
    set statusReport to statusReport & "スキャン間隔: " & scanInterval & "秒" & return
    set statusReport to statusReport & "対象ボタン: " & (targetButtons as string) & return
    set statusReport to statusReport & "Claude関連アプリ: " & (claudeApps as string) & return
    set statusReport to statusReport & "除外アプリ: " & (excludedApps as string)
    
    display dialog statusReport buttons {"OK"} default button "OK" with title "ClaudeCode自動承認"
end showStatus

-- メニュー表示・操作選択
on showMenu()
    set menuChoice to display dialog "ClaudeCode自動承認ツール (AppleScript版)" & return & return & "操作を選択してください:" buttons {"監視開始", "状態確認", "終了"} default button "監視開始" with title "ClaudeCode自動承認"
    
    set buttonPressed to button returned of menuChoice
    
    if buttonPressed is "監視開始" then
        startMonitoring()
    else if buttonPressed is "状態確認" then
        showStatus()
    else if buttonPressed is "終了" then
        set isRunning to false
        addLog("ユーザーによる終了")
    end if
end showMenu

-- スタンドアロン実行用
on run
    try
        showMenu()
    on error errorMsg
        addLog("実行エラー: " & errorMsg)
        display dialog "エラーが発生しました: " & errorMsg buttons {"OK"} default button "OK" with icon stop
    end try
end run

-- 外部呼び出し用関数
on startAutoClicker()
    set isRunning to true
    startMonitoring()
end startAutoClicker

on stopAutoClicker()
    set isRunning to false
    addLog("外部からの停止要求")
end stopAutoClicker

on getClickCount()
    return clickCount
end getClickCount

on getStatus()
    return {isRunning:isRunning, clickCount:clickCount, logMessages:logMessages}
end getStatus