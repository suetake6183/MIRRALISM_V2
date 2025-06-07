#!/usr/bin/env swift
/*
ClaudeCode 自動承認アプリ (Swift版)
================================

目的: ネイティブmacOSアプリとしてClaudeCode確認ダイアログを自動化
方針: Accessibility API + 高度なパターン認識
作成日: 2025年6月6日

コンパイル方法:
swiftc -o claude_auto_clicker_app claude_auto_clicker_app.swift
*/

import Foundation
import AppKit
import ApplicationServices

class ClaudeAutoClickerApp {
    private var isRunning = false
    private var clickCount = 0
    private let scanInterval: TimeInterval = 0.5
    private var timer: Timer?
    
    // 監視対象のボタンテキスト
    private let targetButtons = [
        "Yes", "OK", "Allow", "Continue", "Proceed", "Confirm",
        "はい", "OK", "許可", "続行", "確認"
    ]
    
    // Claude関連キーワード
    private let claudeKeywords = [
        "claude", "Claude", "CLAUDE", "Terminal", "Code", "VS Code"
    ]
    
    init() {
        print("🤖 ClaudeCode自動承認アプリ (Swift版) 初期化")
        requestAccessibilityPermissions()
    }
    
    private func requestAccessibilityPermissions() {
        let options = [kAXTrustedCheckOptionPrompt.takeUnretainedValue(): true]
        let trusted = AXIsProcessTrustedWithOptions(options as CFDictionary)
        
        if !trusted {
            print("⚠️  アクセシビリティ権限が必要です")
            print("   システム環境設定 > セキュリティとプライバシー > プライバシー > アクセシビリティ")
            print("   でこのアプリケーションを許可してください")
        } else {
            print("✅ アクセシビリティ権限確認済み")
        }
    }
    
    func start() {
        guard !isRunning else {
            print("既に実行中です")
            return
        }
        
        isRunning = true
        print("🚀 自動承認監視開始")
        print("   停止: Ctrl+C")
        
        timer = Timer.scheduledTimer(withTimeInterval: scanInterval, repeats: true) { _ in
            self.scanAndClick()
        }
        
        RunLoop.current.run()
    }
    
    func stop() {
        isRunning = false
        timer?.invalidate()
        timer = nil
        print("🛑 自動承認監視停止 (総クリック数: \(clickCount))")
    }
    
    private func scanAndClick() {
        guard isRunning else { return }
        
        // フロントアプリケーション取得
        guard let frontApp = NSWorkspace.shared.frontmostApplication else { return }
        
        // 除外アプリチェック
        let excludedApps = ["System Preferences", "Finder"]
        if excludedApps.contains(frontApp.localizedName ?? "") {
            return
        }
        
        // Claude関連アプリかチェック
        let appName = frontApp.localizedName ?? ""
        let isClaude = claudeKeywords.contains { keyword in
            appName.lowercased().contains(keyword.lowercased())
        }
        
        if !isClaude {
            return
        }
        
        // アクセシビリティAPIでボタン検索
        if let appElement = AXUIElementCreateApplication(frontApp.processIdentifier) {
            findAndClickButtons(in: appElement)
        }
    }
    
    private func findAndClickButtons(in element: AXUIElement) {
        var children: CFArray?
        let result = AXUIElementCopyChildren(element, &children)
        
        guard result == .success, let childrenArray = children else { return }
        
        let count = CFArrayGetCount(childrenArray)
        
        for i in 0..<count {
            let child = CFArrayGetValueAtIndex(childrenArray, i)
            let childElement = Unmanaged<AXUIElement>.fromOpaque(child!).takeUnretainedValue()
            
            // ボタンかチェック
            if isButton(childElement) {
                if let title = getElementTitle(childElement) {
                    if targetButtons.contains(title) {
                        // ボタンクリック
                        clickButton(childElement, title: title)
                        return
                    }
                }
            }
            
            // 再帰的に子要素を検索
            findAndClickButtons(in: childElement)
        }
    }
    
    private func isButton(_ element: AXUIElement) -> Bool {
        var role: CFTypeRef?
        let result = AXUIElementCopyAttributeValue(element, kAXRoleAttribute, &role)
        
        guard result == .success,
              let roleString = role as? String else { return false }
        
        return roleString == kAXButtonRole
    }
    
    private func getElementTitle(_ element: AXUIElement) -> String? {
        var title: CFTypeRef?
        let result = AXUIElementCopyAttributeValue(element, kAXTitleAttribute, &title)
        
        guard result == .success else { return nil }
        return title as? String
    }
    
    private func clickButton(_ element: AXUIElement, title: String) {
        let result = AXUIElementPerformAction(element, kAXPressAction)
        
        if result == .success {
            clickCount += 1
            print("✅ 自動クリック実行: \(title) (\(clickCount)回目)")
        } else {
            print("❌ クリック失敗: \(title)")
        }
    }
}

// メイン実行部分
func main() {
    let app = ClaudeAutoClickerApp()
    
    // シグナルハンドラー設定
    signal(SIGINT) { _ in
        print("\n🛑 終了シグナル受信")
        exit(0)
    }
    
    signal(SIGTERM) { _ in
        print("\n🛑 終了シグナル受信")
        exit(0)
    }
    
    // 引数処理
    let arguments = CommandLine.arguments
    
    if arguments.contains("--help") || arguments.contains("-h") {
        print("""
        ClaudeCode自動承認アプリ (Swift版)
        
        使用方法:
          swift claude_auto_clicker_app.swift       # 開始
          swift claude_auto_clicker_app.swift --help # ヘルプ表示
        
        機能:
          - ClaudeCode関連ダイアログの自動Yes/OK/Allow
          - ネイティブmacOS Accessibility API使用
          - リアルタイム監視・自動クリック
        
        停止: Ctrl+C
        """)
        return
    }
    
    // アプリ開始
    app.start()
}

// 実行
main()