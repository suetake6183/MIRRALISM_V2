---
author: 末武修平
category: 知識ベース
created: '2025-05-25'
status: draft
tags:
- tech/ai
- tech/web
title: 'ATOK Pad 代替ツール調査 '
---

# **ATOK Padの代替ツール調査およびATOK Padの現在価値に関する分析レポート**

## **1\. はじめに**

本レポートは、かつて多くのユーザーに利用された日本語入力支援メモツール「ATOK Pad」の現状と、その代替となり得る現代的なツールについて多角的に調査・分析するものです。ATOK Padが提供していた利便性、特にATOK IMEとの連携や軽快な動作、ホットキーによる即時アクセスといった特徴を踏まえ、現在のソフトウェア市場における選択肢を評価します。また、ATOK Pad自体が今なお利用価値を持つのかについても検証します。

かつてATOK Padは、ATOKユーザーにとって、アイデアのメモや一時的なテキスト入力の場として重宝されました。しかし、ソフトウェアの進化は速く、OSのアップデートや新しいクラウドサービスの登場により、ATOK Padの立ち位置も変化しています。本レポートを通じて、ユーザーが自身のニーズに最適なメモ環境を再構築するための一助となることを目指します。

## **2\. ATOK Padの現状分析**

ATOK Padは、ジャストシステムが提供するATOK日本語入力システムと連携するメモツールとして開発されました。その主な特徴は、ホットキーによる迅速な呼び出しと、入力したメモのEvernoteなど外部サービスとの連携機能でした 1。しかし、現在の開発状況やサポート体制には注意が必要です。

### **2.1. 開発・サポート状況**

ATOK Padに関する公式情報は限定的であり、積極的な開発が継続されているとは言い難い状況です。

* **Windows版ATOK Pad:**  
  * ATOK 2017 for Windowsのヘルプ情報では、ATOK Padの利用にはATOK 2017、ATOK 2015、またはATOK 2011 for Windowsのいずれかが必要とされています 3。これは、ATOK Padが特定の古いATOKバージョンに依存していることを示唆しています。  
  * 2017年2月3日更新の情報では、ATOK Pad \[ベータ5\]以降の変更点として、Yahoo\!連携の変更、EvernoteおよびTwitterの認証方法変更、Evernoteとの自動同期機能などが記載されています 3。しかし、これ以降のメジャーな機能アップデートに関する情報は乏しいです。  
  * ATOK Padのバージョン情報を確認する方法はタスクトレイのアイコンからアクセスできるとされていますが 3、これはサポートが継続していることを保証するものではありません。  
  * ATOK 2013 for WindowsをアンインストールするとATOK Padが表示できなくなるという記述もあり 3、特定のATOK本体との強い依存関係が伺えます。  
* **Mac版ATOK Pad:**  
  * Mac App StoreにおけるATOK Padの最終アップデートは2014年6月26日のバージョン2.0.7で、Evernote認証時の強制終了問題が修正されたと記録されています 2。  
  * 開発元であるJUSTSYSTEMS CORPORATIONは、Appleに対してプライバシー慣行に関する詳細を長らく提供しておらず、次のアプリアップデート時に提供が求められる状態です 2。これは、2014年以降、実質的な開発が停滞している可能性が高いことを示しています。  
  * 互換性としてはmacOS 10.6.6以降が必要とされていますが 2、ユーザーレビューでは、OSのバージョンアップ（例：Yosemite）に伴いホットキーが機能しなくなる 2、フォント設定が保存されないといった不具合が2014年～2016年頃に報告されています 2。これらの情報から、最新のmacOSでの安定動作は期待薄と言えます。  
* **iOS版ATOK Pad:**  
  * 「ATOK Pad for iOS」という名称で存在し、Evernoteを介してWindows版やMac版のATOK Padとメモを同期できる機能がありました 2。  
  * サポートFAQには2017年時点の情報も含まれていますが 4、2017年にはiPhoneとiPadで使用できなくなったという情報も見られます 5。これは、iOSの進化に伴いアプリが対応できなくなった可能性を示唆しています。  
  * 現在、ATOK for iOS \[Professional\] は提供されていますが、これにATOK Padと同等のメモ機能が搭載されているという明確な情報はありません 6。ATOK for iOS \[Professional\] はあくまでIMEとしての機能が中心であり、クラウドサービス（ATOKクラウド辞典、ATOK Sync APによる単語共有など）は提供されていますが、独立したメモアプリ機能は確認できません 6。  
* **Android版ATOK Pad:**  
  * ATOK for Android \[Professional\] が提供されており、こちらは高精度な変換機能やクラウドサービス（ATOKクラウド辞典、ATOK Sync APなど）が特徴です 8。  
  * しかし、ATOK Padのような独立したメモ機能がこのProfessional版に搭載されているかは不明確です 7。Android版ATOKのFAQでは、メモ帳アプリなど一般的なアプリでの日本語入力方法の切り替えについて説明されており 10、ATOK Padに特化した記述は見当たりません。

ATOK Padは、かつてはWindows、Mac、iOSといった複数のプラットフォームで展開され、Evernote連携を軸としたメモ同期機能が特徴でした 1。しかし、各プラットフォームでの開発は2010年代半ばから後半にかけて停滞、あるいは終了していると推測されます。特にMac版とiOS版は、OSのアップデートへの追従が困難になった可能性が高いです。Windows版も、古いATOKバージョンへの依存が見られ、最新環境での利用は推奨されません。

### **2.2. 現在の利用価値**

ATOK Padの現在の利用価値は、極めて限定的と言わざるを得ません。

* **メリット:**  
  * もし古い互換性のあるOSとATOKバージョンを使い続けているユーザーがいれば、慣れた操作性で軽快なメモツールとして機能する可能性は残っています 11。  
  * ホットキー（Windows版ではCtrlキー2回、Mac版ではOptionキー2回が初期設定）による即時呼び出しは、依然として魅力的な機能です 2。  
* **デメリット・リスク:**  
  * **開発・サポートの終了:** 長期間アップデートされておらず、セキュリティリスクや最新OSとの互換性問題が深刻です 2。  
  * **機能の陳腐化:** Evernoteとの連携も、現在のEvernoteの仕様や認証方式に対応しているか不明確です（Windows版は\[ベータ5\]で認証方式変更に対応した記載があるものの 3、それ以降のEvernote側の変更への追従は期待できません）。Twitter連携は2021年2月時点で既に機能しないことが確認されています 13。  
  * **ATOK Passport非連携:** ATOK Padは、現在のATOKの主流であるサブスクリプションサービス「ATOK Passport」との直接的な連携機能は提供されていません。ATOK Passportは最新のATOKエンジンやクラウドサービスを利用できる点がメリットですが 14、ATOK Padはこの恩恵を受けられません。  
  * **動作環境の制約:** Windows版はATOK 2010～2017など特定の古いバージョンが必要であり 3、Mac版はmacOS 10.6.6以降とされていますが、近年のOSでは不具合報告があります 2。Android版ATOKも、古いバージョン（Android 7.1以下）へのアプリ提供は終了しています 18。

これらの点を総合的に勘案すると、ATOK Padを現在積極的に利用することは、セキュリティ、安定性、機能性のいずれの観点からも推奨できません。特に新規での導入や、最新環境での利用は避けるべきです。

ATOK Padは、その登場時にはユニークな価値を提供していましたが、開発の停滞と技術の進化により、その役割を終えたと考えるのが妥当です。ユーザーは、より現代的で、セキュリティが確保され、活発に開発・サポートされている代替ツールへ移行することが賢明です。

## **3\. ATOK Padの代替候補ツール**

ATOK Padの代替を探るにあたり、ATOK Padが持っていた「ATOKとの連携（快適な日本語入力）」「ホットキーによる素早い起動」「シンプルなメモ機能」「クラウド同期（主にEvernote）」といった要素を考慮し、いくつかのカテゴリーに分けて候補を検討します。

### **3.1. ジャストシステム製品内の代替候補**

ジャストシステムはATOK Pad以外にもメモ機能を持つ、あるいは連携する製品を提供しています。

#### **3.1.1. 一太郎Pad**

「一太郎Pad」は、スマートフォン・タブレット専用のメモアプリで、ワープロソフト「一太郎」との連携を主眼に置いた製品です 19。

* **主な機能:**  
  * **写真からの文字起こし (OCR):** スマートフォンのカメラで撮影した画像からテキストを抽出できます。紙資料のデジタル化に便利です 19。ただし、この機能は2025年5月末でサポート終了予定で、「一太郎2025」では新たな「画像から文字起こし」機能が提供されます 20。  
  * **省入力ツール:** 日時や定型的な記号（括弧、三点リーダーなど）を簡単に入力できるツールバーが備わっています 19。  
  * **一太郎とのWi-Fi連携:** 作成したメモを一太郎（一太郎2020以降）にWi-Fi経由で転送できます。書式情報（「\#」で見出し指定など）を伴う連携も可能です 19。  
  * **対応OS:** iOSおよびAndroidに対応しています 19。  
* ATOK Padとしての代替性評価:  
  一太郎Padは、ATOK Padが提供していたデスクトップでの素早いメモ環境とは特性が異なります。主にモバイル環境での利用を想定し、一太郎へのコンテンツ供給を目的としています 19。ホットキーで即座に呼び出せるデスクトップアプリケーションではありません。  
  ATOK IMEとの連携については、モバイルOS上で選択されたIME（ATOK for Android/iOSも選択可能）を使用する形となり、ATOK Padのような製品レベルでの密な連携というよりは、OS標準のIME利用の範疇です 21。省入力ツールは入力補助にはなりますが、ATOK IMEの高度な機能を直接呼び出すものではありません。  
  ATOK Passportとの関連では、「一太郎2025」のインストールにATOK Passportの設定が必要であり 23、「一太郎2023」以降ではATOK Passport搭載のATOKクラウド辞典が利用可能になるなど 24、デスクトップ版一太郎がATOK Passportを活用する形です。一太郎Pad自体がATOK Passportの機能をフルに活用するわけではありません。  
* **メリット・デメリット:**  
  * **メリット:** 高品質なOCR機能（ただしサポート終了予定あり）21、一太郎ユーザーにとってはモバイルからの入力手段として有用、無料であること 22。  
  * **デメリット:** ATOK Padのようなデスクトップでのクイックメモの代替にはならない、モバイル中心のアプリであること、OCR機能の提供形態が変更される点 20。

一太郎Padは、ATOK Padの直接的な後継や代替とは言えません。その設計思想は、あくまで一太郎ユーザーがモバイルデバイスでメモや資料のテキスト化を行い、それをPCの一太郎本体で活用するための支援ツールという位置づけです。手軽なメモ入力とOCR機能を求める一太郎ユーザーには価値がありますが、ATOK Padのようなホットキー起動のデスクトップメモを求めるユーザーのニーズは満たしません。

### **3.2. OS標準搭載のクイックメモ機能**

WindowsおよびmacOSには、OSレベルで簡易的なメモ機能が提供されており、これらがATOK Padの代替となり得るか検討します。

#### **3.2.1. Windows**

* **付箋 (Sticky Notes):**  
  * **機能:** デスクトップ上にデジタル付箋を表示し、簡単なメモを書き留めることができます。基本的な書式設定（太字、斜体、下線、取り消し線、箇条書き）もショートカットキーで可能です 25。Microsoftアカウントでデバイス間の同期も行われます。  
  * **ATOK IME連携:** 通常のWindowsアプリケーションと同様に、ATOK IMEを日本語入力に使用できます。多くのユーザーレビューで、ATOKはWindows上で快適な入力環境を提供すると評価されています 16。  
  * **ホットキーアクセス:** ATOK Padのように、グローバルホットキーで*新規の*付箋を即座に作成する機能は標準では備わっていません。既存の付箋はデスクトップに表示されています。アプリがアクティブな状態であれば、Ctrl+Nで新しい付箋を作成できます 26。Windows \+ Alt \+ NはOneNoteのクイックノートを起動するもので、付箋アプリを直接起動するものではありません 29。  
  * **カスタマイズ/常駐:** 付箋はデスクトップに常駐します。新規付箋作成のためのグローバルホットキーを設定するには、AutoHotkeyのようなサードパーティ製ツールが必要になる場合があります 30。  
  * **使用感:** 素早く視覚的なリマインダーとして便利です 32。  
* **メモ帳 (Notepad) \+ クイック起動:**  
  * **機能:** OS標準の基本的なテキストエディタです。高速な起動以外に、特筆すべき「クイックメモ」機能はありません。  
  * **ATOK IME連携:** ATOK IMEは標準的なWindowsアプリケーションとして動作します 33。  
  * **ホットキーアクセス:** タスクバーへのピン留めや、実行ファイルへのカスタムショートカットキー割り当てにより、比較的素早く起動できます。しかし、ATOK Padのようなグローバルホットキーによる表示/非表示の切り替えはできません。

#### **3.2.2. macOS**

* **クイックメモ (Quick Note \- macOS Monterey以降):**  
  * **機能:** ホットコーナーまたはFn+Qショートカットキーにより、システム全体で利用可能なメモ作成機能です 35。作成されたメモは標準の「メモ」アプリに保存され、他のアプリで表示中のコンテンツへのリンクも可能です。  
  * **ATOK IME連携:** システムで選択されているIME（ATOK for Macも含む）を使用します。macOSでのATOKの評価は概ね良好ですが、macOS標準IMEも高性能であるとの意見も見られます 38。  
  * **ホットキーアクセス:** デフォルトはFn+Qです 35。ホットコーナーも利用可能です。システム設定である程度のカスタマイズが可能で、BetterTouchToolのようなツールを使えば、より複雑なキーマッピングも実現できます 40。  
  * **使用感:** アプリケーションを切り替えることなく、思いついたことをすぐにメモできるため非常に便利です。  
* **メモアプリ (Notes App):**  
  * **機能:** フォルダ管理、書式設定、添付ファイル、iCloud同期など、より多機能なノートアプリです 42。クイックメモは、このメモアプリへの入力手段の一つと位置づけられます。  
  * **ATOK IME連携:** 上記クイックメモと同様、システムIMEを使用します。  
  * **ホットキーアクセス:** アプリ内でCommand+Nで新規メモを作成できます 35。グローバルなクイック作成はクイックメモ機能が担います。

OS標準のクイックメモ機能、特にmacOSの「クイックメモ」は、ATOK Padが提供していた即時アクセス性に近い体験を提供します。Windowsの「付箋」は、新規メモの即時作成という点では一手間必要です。これらのOS標準機能は、アクティブなIMEとしてATOKを利用できますが、ATOK Padがジャストシステム製品として持っていた可能性のある、ATOK IMEの特定機能とのより深い連携（例えば、専用パレットの呼び出しや特殊コマンドの実行など。ただし、提供資料からはATOKでの変換以外の具体的な連携内容は不明瞭 1）までは期待できません。OS標準ツールは利便性とシステム統合性を提供するものの、「ATOK連携」はIME選択のレベルに留まることが多いでしょう。

### **3.3. 汎用テキストエディタのメモ活用**

汎用テキストエディタは、その軽量性やカスタマイズ性を活かしてメモ用途に転用できます。

#### **3.3.1. Windows**

* **サクラエディタ (Sakura Editor):**  
  * **機能:** 無料で軽量な国産テキストエディタ。タブインターフェース、豊富なカスタマイズオプション、マクロ機能を備えています 44。  
  * **起動速度:** 一般的に高速かつ軽量であると評価されています 44。タスクトレイに常駐させることも可能です 46。  
  * **ATOK IME連携:** 標準的なWindowsアプリケーションとしてATOK IMEと連携します。ユーザーからはATOKとの組み合わせで良好な使用感が報告されています 52。  
  * **メモ管理:** 複数ファイルをタブで管理できます 45。ファイル名やフォルダ構造以外での高度なタグ付け機能は内蔵していません。  
  * **クラウド同期:** ネイティブなクラウド同期機能はありません。Dropboxなどのクラウド同期フォルダにファイルを保存することで、手動またはスクリプトやバッチファイルを用いて同期が可能です 53。  
  * **ホットキーアクセス:** ショートカットキーで起動可能です。常駐モードではタスクトレイから素早くアクセスできます 51。CLaunchやFenrirといったランチャーソフトと組み合わせることで、カスタムホットキーによる起動も実現できます。  
* **Notepad++:**  
  * **機能:** 無料で軽量なテキストエディタ。タブインターフェース、プラグインによる機能拡張、シンタックスハイライトなどが特徴です 58。  
  * **起動速度:** 高速な起動で知られています 58。  
  * **ATOK IME連携:** 標準的なWindowsアプリケーションとして動作し、ATOKの日本語入力における強みを活かせます 59。  
  * **メモ管理:** タブ機能、セッション管理（前回開いていたファイルを記憶）があります。  
  * **クラウド同期:** ネイティブな同期機能はなく、クラウド同期フォルダへのファイル保存に依存します。  
  * **ホットキーアクセス:** ショートカットキーで起動します。

#### **3.3.2. クロスプラットフォーム**

* **Visual Studio Code (VS Code):**  
  * **機能:** 高機能で拡張性に優れたコードエディタですが、Markdownサポートや豊富な拡張機能により、ノートテイキングツールとしても活用できます 60。  
  * **起動速度:** 一般的に高速ですが、多数の拡張機能を導入すると、軽量エディタに比べて起動が遅くなることがあります。  
  * **ATOK IME連携:** 標準アプリケーションとして動作します。macOS環境でATOKクラウドチェッカーとバックスペース制御文字の相性問題が報告された例があります 64。通常のATOK入力は問題ないと考えられます。  
  * **メモ管理:**  
    * Markdown All in One: Markdown編集を強化します。  
    * Todo Tree: ファイル横断でTODOコメントを管理します。  
    * Dendron / Foam: Zettelkasten方式のノート作成を支援する拡張機能で、知識ベースを構築できます 65。vscode-memoも選択肢の一つです 67。  
    * Obsidian Importer: Obsidianからのノート移行を支援します 69。  
    * タグ付け: Markdownのfrontmatterや特定の拡張機能を利用して実現可能です。  
  * **クラウド同期:**  
    * Settings Sync: VS Codeの設定、拡張機能、キーバインドなどをGitHubまたはMicrosoftアカウント経由でデバイス間で同期する組み込み機能です 70。  
    * Git: 強力なGit統合機能により、ノートリポジトリのバージョン管理や同期（GitHub/GitLabなどとの連携）が可能です 72。  
    * Evernote連携拡張機能: 存在しますが、品質やメンテナンス状況は様々です。一般的な拡張機能のインストール方法に関する記述はありますが 74、VS Code用の特定のEvernote連携拡張機能に関する詳細はありません。  
  * **ホットキーアクセス:** コマンドパレット (Ctrl+Shift+P または F1) から素早くコマンドを実行できます 76。カスタムワークスペースタスクを定義したり、AutoHotkeyのようなOSレベルのツールでグローバルホットキーを設定したりすることも可能です 80。

テキストエディタは高いカスタマイズ性とファイル管理の自由度を提供しますが、ATOK Padのような「クイックメモ」体験を実現するには、相応の設定が必要です。サクラエディタ、Notepad++、VS Codeのようなエディタは、本来テキスト編集のための強力なツールであり、そのままでは専用のメモアプリとは異なります。ATOK Padの素早いホットキーアクセスやシンプルなインターフェースを再現するには、ユーザー自身がショートカットを設定したり、VS Codeの場合は拡張機能を活用したり 65、ファイル管理や同期を手動または他のツールで行う必要があります。その利点は、環境を完全にコントロールでき、プレーンテキスト形式でデータを扱えることです。一方で、初期設定の手間や、設定なしでは専用メモアプリのようなシンプルなUIが得られない点がトレードオフとなります。

### **3.4. クラウド型メモ・ノートサービス**

クラウドベースのメモアプリは、マルチデバイスでの利便性が高く、多様な選択肢があります。

* **Evernote:**  
  * **機能:** リッチテキストノート、ノートブック、タグ、Webクリッパー、画像/PDF内のOCR、クロスプラットフォーム同期といった豊富な機能を持ちます 82。かつてATOK PadはEvernoteとの同期機能を備えていました 1。  
  * **ATOK IME連携:** 通常のアプリケーションとしてATOKと連携するはずです。しかし、一部のMacユーザーからは、Evernoteエディタでの日本語入力に関する不具合（最初の文字が勝手に確定される、特定文字の入力に問題が生じるなど）が報告されており、ATOKまたはEvernote側のIME処理に関連する可能性があります 87。一部ブログではEvernoteとATOKの併用が有用とされていますが 5、動作が重いと感じる可能性も指摘されています 89。  
  * **クラウド同期:** Evernoteのコア機能であり、一般的には信頼性がありますが、ユーザー体験にはばらつきが見られることもあります。  
  * **価格:** 機能制限のある無料プランと、より多くの機能やストレージを提供する有料サブスクリプションがあります 82。  
  * **ユーザー評価:** 機能セットとクロスプラットフォーム対応は評価されていますが、価格改定、UI変更、時折見られるパフォーマンス問題（動作の重さなど）に対する批判もあります 53。  
* **Microsoft OneNote:**  
  * **機能:** 自由なレイアウトが可能なキャンバス、ノートブック/セクション/ページ構造、描画機能、Office製品との連携、クロスプラットフォーム同期が特徴です 32。  
  * **ATOK IME連携:** システムIMEとしてATOKを利用可能です。一部フォーラムでは、ATOKでの入力が特定のウェブテキストフィールドで遅延したり不安定になったりする報告がありますが（OneNote特有ではなく一般的なATOKの問題の可能性）104、あるいはATOKの「テキストサービス」設定が候補表示に影響するケースも指摘されています 105。OneNote自体、一部ユーザーからATOK特有ではない入力遅延が報告されることもあります 98。ATOKの辞書がOneNoteで機能しないといった特有の問題は提供資料からは確認できませんでした 106。  
  * **クラウド同期:** OneDriveベースで、一般的に良好です。  
  * **価格:** Microsoftアカウントで無料利用可能。Microsoft 365契約でストレージ容量が増加します。  
  * **ユーザー評価:** 自由なノート作成やOfficeユーザーに評価されています 98。一部には複雑さや時折の動作の遅さを指摘する声もあります 98。  
* **Google Keep:**  
  * **機能:** シンプルなカード形式のメモ、チェックリスト、リマインダー、画像・音声メモ、Googleサービスとの連携、クロスプラットフォーム対応が特徴です 108。  
  * **ATOK IME連携:** システムIMEとしてATOKを利用可能です。ATOK全般の設定で、どのアプリでも遅延を感じる場合に調整可能な項目があります 115。Bluetoothキーボード使用時のATOKの遅延が一部で指摘されていますが、これはKeep特有の問題ではありません 116。  
  * **クラウド同期:** Google Drive経由で、一般的にシームレスです。  
  * **価格:** 無料です。  
  * **ユーザー評価:** 手軽なメモ作成におけるシンプルさと速度が評価されています 118。ラベルによる整理がフォルダ構造より直感的でないと感じるユーザーもいます 118。  
  * **ホットキー:** Webアプリ内でキーボードショートカットが利用可能です 120。デフォルトでグローバルホットキーによるクイックノート作成機能はありませんが、デスクトップショートカットを作成してウィンドウとして開くことは可能です 121。  
* **Simplenote:**  
  * **機能:** 無料、ミニマルなデザイン、プレーンテキスト/Markdown対応、高速同期、クロスプラットフォーム、タグによる整理が特徴です 16。  
  * **ATOK IME連携:** テキスト中心のアプリであるため、ATOKとの相性は良いと考えられます。ATOKの一般的なパフォーマンスを評価する声があります 16。個人的にATOKが合わなかったという意見もありますが、Simplenote特有の問題ではありません 123。E-Ink端末(BOOX)上のAndroid版ATOKとBluetoothキーボードの組み合わせは、若干の遅延はあるものの良好との報告があります 132。  
  * **クラウド同期:** Simplenoteのコア機能で、一般的に高速かつ信頼性があります 122。  
  * **価格:** 無料です 124。  
  * **ユーザー評価:** テキストメモにおける速度、シンプルさ、クロスプラットフォーム同期が高く評価されています 122。リッチフォーマット非対応は意図的な特徴ですが、一部ユーザーには欠点と映ることもあります。  
  * **ホットキー:** アプリ内でショートカットが利用可能です 126。クイックキャプチャのための組み込みグローバルホットキーはありません。  
* **Joplin:**  
  * **機能:** オープンソース、Markdown対応、ノートブック/タグ、Webクリッパー、エンドツーエンド暗号化、多様なサービス（Dropbox, OneDrive, Joplin Cloudなど）との同期、クロスプラットフォーム対応が特徴です 134。  
  * **Evernoteからの移行:** Evernoteの.enexファイルからのインポートをサポートしており、概ねシームレスに移行可能です 134。ただし、一部ユーザーからはインポート時に空白行や改行が意図通りに処理されないという報告もあります 136。  
  * **ATOK IME連携:** オープンソースアプリとして、システムIMEを使用します。提供資料内にATOKとの特有の互換性問題に関する記述は見られません。  
  * **クラウド同期:** 自己ホスティングやJoplin Cloudなど柔軟な選択肢があります。一部ユーザーからAndroidアプリの同期が不安定との報告があります 142。  
  * **価格:** アプリ自体は無料。Joplin Cloudは有料サービスです 141。  
  * **ユーザー評価:** オープンソースであること、カスタマイズ性、プライバシー保護の観点から評価されています 135。  
  * **ホットキー:** Windowsでは実行ファイルにショートカットキーを割り当てることで、実行中であれば前面に表示させることが可能です 138。組み込みのグローバルホットキーによるクイックキャプチャ機能に関する記述はありません。  
* **Standard Notes:**  
  * **機能:** 無料、オープンソース、プライバシーとエンドツーエンド暗号化に注力、クロスプラットフォーム対応。有料プランでMarkdownサポートや拡張機能が利用可能になります 29。  
  * **ATOK IME連携:** システムIMEを使用するはずです。ATOKとの特有の互換性問題に関する記述は見られません。  
  * **クラウド同期:** 暗号化された同期機能を提供します。  
  * **価格:** 基本的なプレーンテキストノートは無料。テーマ、リッチテキスト/Markdownエディタ、大容量ストレージなどは有料プラン（Productivity, Professional）で提供されます 156。  
  * **ユーザー評価:** セキュリティとプライバシーが高く評価されています 156。App Storeでの評価は4.6/5です 144。有料プランが高価だと感じるユーザーもいます 145。  
  * **ホットキー:** クイックキャプチャのための特有のグローバルホットキーに関する記述はありません。一般的なWindowsのショートカットが適用される可能性があります 29。

クラウドベースのメモアプリは、マルチデバイスでの利便性を提供する一方で、その複雑さや「クイックキャプチャ」の感覚はアプリによって大きく異なります。ここでの「ATOK連携」は、主にATOKをIMEとして使用できることを指し、ATOK Padのような深いレベルでの統合というよりは、時折見られるアプリ固有の入力バグへの対応が焦点となります。EvernoteやOneNoteのような多機能アプリは、ATOK Padのシンプルさと比較すると重厚に感じられるかもしれません 82。Google KeepやSimplenoteのようなよりシンプルな選択肢は、基本的なメモには高速ですが、一部のユーザーにとっては整理機能が不足しているかもしれません 118。「ホットキーアクセス」は通常、アプリ内でのショートカットを指し、ATOK Padのようなグローバルキャプチャ機能は、OSの機能やサードパーティツールを利用しない限り限定的です。Mac版Evernoteでの入力問題の報告 87 などは、IME全般とのアプリ互換性の問題であり、ATOK Padのような専用の機能強化とは異なります。

### **3.5. Mac向け多機能エディタ**

Macプラットフォームには、洗練されたUIとMarkdownサポートを特徴とする多機能なエディタが存在します。これらはATOK Padの直接的な代替というより、より本格的な執筆や情報整理に適しています。

* **Ulysses:**  
  * **機能:** Markdownを中心とした執筆アプリで、ライブラリ管理、豊富なエクスポートオプション、iCloud同期、目標設定、タイプライターモード、カスタマイズ可能な表示といった特徴を持ちます 39。  
  * **ATOK IME連携:** MacアプリとしてシステムIMEを使用します。MacでのATOKの評価は一般的に良好ですが、macOS標準IMEも高性能であるとの意見もあります 38。UlyssesとATOKの深いレベルでの特有の連携機能に関する記述はありません。  
  * **クラウド同期:** iCloud同期がコア機能で、一般的にシームレスかつ高速です 157。同期に関するトラブルシューティング情報も存在します 162。  
  * **価格:** サブスクリプションモデル（月額または年額）です 159。  
  * **ユーザー評価:** 集中できる執筆環境と整理機能が高く評価されています 157。App Storeでの評価は4.7/5です 159。  
  * **ホットキーアクセス:** アプリ内部のショートカットは豊富ですが、ATOK Padのようなグローバルな「クイックキャプチャ」ホットキーは備えていません。  
* **Bear:**  
  * **機能:** Markdownノート、タグシステム、テーマ、スケッチ機能、iCloud同期、クロスプラットフォーム（Appleエコシステム内）対応が特徴です 167。  
  * **ATOK IME連携:** システムIMEを使用します。BearとATOKの深いレベルでの特有の連携機能に関する記述はありません。ATOK *for iOS* \[Professional\] に関する一部の否定的なレビュー 174 は、Bearアプリ自体の評価とは異なります。  
  * **クラウド同期:** iCloud同期（Pro版の機能）に対応しています 180。  
  * **価格:** 機能制限のある無料版と、同期や高度な機能を含むProサブスクリプションがあります 171。  
  * **ユーザー評価:** 美しいUI、軽快な動作、Markdownサポートが評価されています 169。App Storeでの評価は4.4/5です 170。一部で、印刷時にフォントが中国語のように表示される問題が報告されています 177。  
  * **ホットキーアクセス:** アプリ内部のショートカットがあります。macOSでは一部ショートカットのカスタマイズが可能です 175。特有のグローバルな「クイックキャプチャ」ホットキーはありません。  
* **Craft:**  
  * **機能:** 構造化されたドキュメント作成、デイリーノート、タスク管理、AI機能、コラボレーション、クロスプラットフォーム対応（Windows、Web版も含む）が特徴です 184。  
  * **ATOK IME連携:** システムIMEを使用します。CraftとATOKの深いレベルでの特有の連携機能に関する記述はありません。ATOK Proが専門用語に強いという一般的なレビュー 184 や、近年のATOKがゲーム・アニメタイトルにも対応しているという情報 185 はありますが、Craft特有のものではありません。  
  * **クラウド同期:** 独自の同期メカニズムを持ち、一般的に高速とされています 196。  
  * **価格:** 無料プランと、有料のPlusサブスクリプションがあります 196。  
  * **ユーザー評価:** 特にiPadでの直感的なUIが評価されています 186。構造化されたノートやドキュメント作成に適しています。  
  * **ホットキーアクセス:** アプリ内部のショートカットが利用可能です 190。特有のグローバルな「クイックキャプチャ」ホットキーはありません。

Ulysses 157 やBear 173 のようなMac専用（またはAppleエコシステム中心の）ライティングアプリは、洗練された使用感とMarkdownサポートを提供しますが、一般的にATOK Padのような「クイックメモ」ホットキーツールとは異なります。これらのアプリの強みは、構造化された文章作成やAppleエコシステム内での情報整理にあります。これらは執筆やノート作成には優れていますが、通常、現在使用中のアプリケーションから文脈を切り替えることなく、ふとした思いつきを書き留めるための、シンプルなホットキーで即座にポップアップするインターフェースは備えていません。これはATOK Padの重要な特徴の一つでした。これらのアプリの「素早さ」は、アプリがアクティブな状態での内部パフォーマンスや新規ノート作成の容易さに関連しています。

## **4\. 選定における重要な考慮事項**

ATOK Padの代替ツールを選定する際には、いくつかの重要な要素を考慮する必要があります。

* ATOK連携の重要度:  
  単にIMEとしてATOKを使用できるだけで十分なのか、それともATOK Padが持っていた（基本的な入力以外に具体的な連携機能があったかは資料からは不明瞭ですが）ATOKとのより深い連携を求めるのか、という点が重要です。ほとんどの代替ツールは、システムIMEとしてATOKを利用することを許容します。その場合の日本語入力の品質は、ATOK自体の性能と、選択したアプリが標準的なIMEの挙動をどれだけ適切に処理できるかに依存します。  
  ATOK Passportを利用している場合、プラットフォーム間でのIMEの一貫性、クラウド辞書、高度な変換・校正機能といったメリットがあります 6。代替ツールは、これらのATOK Passportの利点を阻害しないものであるべきです。  
* ホットキー／クイック起動のニーズ:  
  アプリケーションのコンテキストを切り替えることなく、グローバルホットキーで即座にメモを作成・アクセスできる機能がどれほど重要か、という点です。  
  macOSのクイックメモはこの種の機能をネイティブで提供しています 35。  
  Windows環境では、AutoHotkeyのようなツール 30 や軽量エディタへのカスタムショートカット設定など、より多くの設定作業が必要になります。  
  一部のアプリは、メニューバーアイコンやアプリ固有のショートカット（アプリがアクティブな場合）を介したクイック入力を提供しています。  
* クラウド同期とマルチデバイスアクセス:  
  コンピュータ、タブレット、スマートフォン間でメモにアクセスできる機能は、現代のワークフローにおいて不可欠です 201。  
  クラウドサービスの信頼性、ストレージ容量制限、コスト（iCloud, OneDrive, Google Drive, Dropbox、あるいは各アプリ独自の同期サービスなど）を考慮する必要があります。  
* シンプルさ vs 多機能性:  
  ATOK Padは非常にシンプルなツールでした 1。ユーザーが求めるのは、Simplenoteのようなミニマルなツールなのか 122、それともEvernote 82 やNotion 108 のような多機能な環境なのか、という選択です。  
  機能が多いほど、学習コストが高くなったり、アプリケーションが重くなったりする可能性があります。  
* コスト (無料、サブスクリプション、買い切り):  
  OS標準ツール、Simplenote、Joplinなどの無料オプションから、Evernote、Ulysses、Bear Pro、Craft Plus、そしてATOK Passport自体のようなサブスクリプションモデルまで、価格帯は様々です。  
* データの永続性とフォーマット:  
  メモがプロプライエタリな形式で保存されるのか、それともプレーンテキストやMarkdownのようなオープンな形式で保存されるのか、という点です。オープンフォーマットは、将来的な互換性や相互運用性の観点から優れています（例：Joplin 141、Simplenote 133、テキストエディタ）。

最適な代替ツールは、ユーザーがATOK Padのどの側面を最も重視していたか、そして現在のワークフローやエコシステムに大きく左右されます。もし純粋にATOKを使ったテキストのクイックキャプチャのためのホットキーアクセスが最重要であれば、OSネイティブのソリューションや高度にカスタマイズされた軽量テキストエディタが最適かもしれません。もしEvernote同期が重要であったなら、現代的なクラウドベースのノートアプリがより適切です。単にATOKと良好に連携するクイックメモツールであれば、選択肢はさらに広がります。ユーザーのOS、他のデバイス、支払い意欲、設定への許容度などが、選択肢を絞り込む上で重要な要素となります。

## **5\. 推奨ツール**

ATOK Padの代替となり得るツールは多岐にわたります。ユーザーの優先事項に応じて、いくつかの推奨ツールを以下に示します。

* ATOK Padがまだ利用可能な場合の条件:  
  ほとんどのユーザーには推奨されません。利用が考えられるのは、非常に古い互換性のあるOS（例：MacユーザーであればmacOS Yosemite以前、WindowsユーザーであればATOK 2010～2017などと互換性のある古いWindows）を使い続けており、サポートが終了した潜在的に安全でないソフトウェアを使用するリスクを受け入れ、信頼性の高い同期や最新機能を必要としない、という極めて限定的な状況のみです。これは多くの妥協を伴うニッチなシナリオと言えます。  
* **ユーザーの優先事項に応じた推奨ツール:**  
  * **最優先事項：ホットキーによる即時メモ起動**  
    * **macOS:** **macOS標準「クイックメモ」** 35。システムIME（ATOK互換）を使用。無料でシステムに統合されています。  
    * **Windows:** **軽量テキストエディタ (例：サクラエディタ, Notepad++) \+ AutoHotkey/カスタムショートカット** 30。設定は必要ですが、速度と制御性を提供します。ATOK互換です。  
  * **最優先事項：ATOK IMEとの快適な連携と高機能な日本語入力**  
    * \*\*任意の動作良好な最新アプリケーション \+ ATOK Passport。\*\*鍵となるのはATOK Passport自体です 16。  
    * ノートアプリとしては、**Simplenote** 122（シンプルさとテキスト中心のため）、**VS Code**（パワーユーザー向け、Markdown/Git連携）60、または**Google Keep** 118（手軽なマルチデバイスメモのため）などが、ATOKの動作を妨げにくい良い候補です。  
    * 既知のIME入力バグがあるアプリは可能であれば避けるべきです（例：Mac版Evernoteの報告 87 には注意）。  
  * **最優先事項：シンプルさとマルチデバイス同期**  
    * **Simplenote:** 122 無料、高速、プレーンテキスト/Markdown対応、優れた同期機能。  
    * **Google Keep:** 118 無料、シンプル、クイックリストやマルチメディアメモに適し、優れた同期機能。  
  * **最優先事項：Evernoteのような多機能性とクラウド連携**  
    * **Evernote:** 82 変更点はあるものの、依然として好むユーザー向け。コストと潜在的なパフォーマンス問題に注意。  
    * **Microsoft OneNote:** 98 Microsoftエコシステムユーザーに適した、自由なレイアウトが可能なツール。  
    * **Joplin:** 134 オープンソース、プライベート重視、良好なEvernoteインポート機能、柔軟な同期オプション。  
  * **最優先事項：Macでの洗練された執筆・整理体験**  
    * **Ulysses:** 157 サブスクリプション型。ライター向けの高機能エディタ、ライブラリ管理。  
    * **Bear:** 169 サブスクリプション型（Pro版で同期）。美しいUI、Markdown、タグ機能。  
  * **一太郎ユーザー向け**  
    * **一太郎Pad:** 19 モバイルでのOCRや一太郎へのノート転送用。デスクトップ版ATOK Padの直接的な代替ではありません。  
* **表1: 主要代替候補ツールの比較**

| ツール名 | 主要機能 | クラウド同期 | 対応OS | 価格 | 長所 | 短所 | ATOK Pad代替としての適合性 |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **macOS標準「クイックメモ」** | グローバルホットキー (Fn+Q), ATOK IME互換, Apple Notes連携, システム統合 | iCloud経由 (Apple Notes) | macOS | 無料 | OSネイティブで最も手軽なホットキーメモ。ATOK入力可。 | Windowsユーザーは利用不可。ATOK固有機能との深い連携はない。 | **高** (macOSユーザーでホットキー起動を最重視する場合) |
| **Windows「付箋」 \+ AutoHotkey等** | デスクトップ常駐, ATOK IME互換, 基本書式設定, Microsoftアカウント同期 | Microsoftアカウント経由 | Windows | 無料 (AutoHotkeyも無料) | 視覚的なリマインダーとして便利。ATOK入力可。AutoHotkeyでホットキーカスタマイズ可能。 | 標準ではグローバルホットキーでの新規作成が一手間。AutoHotkeyの設定が必要。 | **中** (Windowsユーザーで、設定の手間を許容しホットキー起動を実現したい場合) |
| **Simplenote** | プレーンテキスト/Markdown, 高速同期, タグ整理, ATOK IME互換 | 独自 (高速・信頼性高) | Windows, macOS, Linux, iOS, Android, Web | 無料 | 非常にシンプルで高速。マルチデバイス同期が優秀。ATOKとの相性も良い。 | リッチテキスト非対応。多機能性を求めるユーザーには不向き。グローバルホットキーは非搭載。 | **高** (シンプルさ、マルチデバイス同期、ATOKとの基本的な互換性を重視する場合) |
| **Google Keep** | カード型メモ, チェックリスト, リマインダー, 画像・音声メモ, ATOK IME互換, Google連携 | Google Drive経由 | Windows, macOS (Web), iOS, Android, Web | 無料 | 手軽で多機能。Googleサービスとの連携が強力。マルチデバイス同期も良好。ATOK入力可。 | ラベル整理がフォルダより好みが分かれる。グローバルホットキーは非搭載。 | **中～高** (Googleエコシステム利用者で、手軽なマルチデバイスメモをATOKで入力したい場合) |
| **VS Code (メモ用途)** | Markdown, 拡張性 (Foam, Dendron等), Git連携, ATOK IME互換, Settings Sync | Git, Settings Sync, 他拡張機能経由 | Windows, macOS, Linux | 無料 (一部拡張機能は有料の場合あり) | 高度にカスタマイズ可能。Markdownでの強力なメモ管理。Gitによるバージョン管理と同期。ATOK入力可。 | 本来はコードエディタであり、メモ専用としては多機能すぎる可能性。起動が軽量エディタより遅い場合がある。グローバルホットキーは要設定。 | **中** (技術者やMarkdown熟練者で、高機能なメモ環境をATOKと共に構築したい場合。設定の手間を厭わないユーザー向け) |
| **Joplin** | オープンソース, Markdown, Evernoteインポート, E2E暗号化, 多様な同期先, ATOK IME互換 | Dropbox, OneDrive, Nextcloud, Joplin Cloud等 | Windows, macOS, Linux, iOS, Android | 無料 (Joplin Cloudは有料) | プライバシー重視。オープンソース。Evernoteからの移行が容易。ATOK入力可。 | 一部で同期の不安定性が報告されることも。UIが洗練されていないと感じるユーザーもいる可能性。グローバルホットキーは限定的。 | **中～高** (Evernoteからの移行を検討し、プライバシーとオープンソースを重視するATOKユーザー向け) |
| **Ulysses (Macユーザー向け)** | Markdown特化, ライブラリ管理, iCloud同期, 高度な執筆機能, ATOK IME互換 | iCloud | macOS, iOS | サブスクリプション | Macでの洗練された執筆体験。強力な整理機能。ATOK入力可。 | Windowsユーザーは利用不可。サブスクリプションコスト。ATOK Padのようなクイックメモツールではない。 | **低～中** (ATOK Padの代替としては方向性が異なるが、MacでATOKを使い本格的な文章作成・整理を行うユーザーには適している) |
| **Bear (Mac/iOSユーザー向け)** | Markdown, タグ, 美麗なUI, iCloud同期 (Pro版), ATOK IME互換 | iCloud (Pro版) | macOS, iOS | 無料 (基本機能), サブスクリプション (Pro版) | UIが美しく軽快。Markdownとタグによる整理。ATOK入力可。 | Windowsユーザーは利用不可。主要な同期機能は有料。ATOK Padのようなクイックメモツールではない。 | **低～中** (ATOK Padの代替としては方向性が異なるが、AppleエコシステムでATOKを使い、デザイン性の高いメモ環境を求めるユーザーには適している) |

この比較表は、ユーザーが自身のニーズに最適なツールを見つけるための判断材料となることを意図しています。各ツールの長所・短所を理解し、ATOK Padのどの機能を代替したいのかを明確にすることで、より適切な選択が可能になります。

## **6\. 結論**

ATOK Padは、その登場時には独自の価値を提供したものの、開発の停滞と技術の進化により、現在ではほとんどのユーザーにとって陳腐化しており、積極的な利用は推奨されません。セキュリティリスクや最新OSとの互換性の問題も無視できません。

代替ツールは多岐にわたりますが、ATOK Padの全ての側面（特に古いATOKバージョンとの特定の連携の可能性）を完全に再現する単一のツールは存在しないと考えるべきです。しかし、現代のツールは、同期機能、プラットフォームサポート、機能性といった特定の領域でATOK Padを凌駕しています。

最適な代替ツールの選択は、個々のユーザーの優先順位に大きく依存します。

* **ホットキーによる即時起動**を最重視するなら、macOSの「クイックメモ」や、Windowsでの軽量テキストエディタとAutoHotkey等の組み合わせが有効です。  
* **ATOK IMEとの快適な連携**は、現在ではATOK Passportを契約し、それが標準的に動作する多くのアプリケーションで実現できます。特定のアプリとの「深い連携」というよりは、IMEとしてのATOKの性能を活かす形になります。  
* **クラウド同期やシンプルさ**を求めるなら、SimplenoteやGoogle Keepが良い選択肢となります。  
* **多機能性**を重視するなら、Evernote、OneNote、Joplinなどが候補に挙がります。  
* **Macでの洗練された執筆体験**を求めるなら、UlyssesやBearが適しています。

「ATOK Padの代替」を探すという課題は、単に機能的に一致するものを探すのではなく、ATOK支援による素早いメモ取りのための現代的なワークフローを特定することへと変化しています。ATOK Padは過去の産物であり、ユーザーは自身の核となるニーズ（優れた日本語入力による迅速なメモ作成）を見極め、それを最もよく満たす現代的なツールを選択すべきです。それは、OSの機能（例：クイックメモ）とATOK Passportの組み合わせであったり、軽量なクラウド同期アプリの利用であったりするかもしれません。「ATOK連携」の概念は、主にIME自体に関するものであり、特定のコンパニオンアプリに依存するものではなくなっています。

最終的には、いくつかの推奨される無料オプションを実際に試用し、自身のワークフローや主要なニーズに最も合致するものを見つけることをお勧めします。ATOKエコシステムに深く関わっているユーザーにとっては、選択した汎用ノートアプリとATOK Passportが円滑に連携することが重要です。

#### **引用文献**

1. ATOK Pad の使い方（Windows）, 5月 24, 2025にアクセス、 [https://atok.com/useful/valueup/atokpad/index\_2010.html](https://atok.com/useful/valueup/atokpad/index_2010.html)  
2. 「ATOK Pad」をMac App Storeで \- Apple, 5月 24, 2025にアクセス、 [https://apps.apple.com/jp/app/atok-pad/id460883588?mt=12](https://apps.apple.com/jp/app/atok-pad/id460883588?mt=12)  
3. ATOK Pad の使い方（Windows）, 5月 24, 2025にアクセス、 [https://www.atok.com/useful/valueup/atokpad/index\_2017.html](https://www.atok.com/useful/valueup/atokpad/index_2017.html)  
4. FAQトップ［ATOK Pad for iOS］ \- サポート \- JustSystems Corporation, 5月 24, 2025にアクセス、 [https://support.justsystems.com/faq/1032/app/servlet/qasearchtop?MAIN=001004001001005](https://support.justsystems.com/faq/1032/app/servlet/qasearchtop?MAIN=001004001001005)  
5. 【2020 年版】 Mac ユーザーおすすめアプリ 〜ライティングアプリ編〜 Vol.3｜おおとろ \- note, 5月 24, 2025にアクセス、 [https://note.com/digiangler777/n/n80d9be047858](https://note.com/digiangler777/n/n80d9be047858)  
6. ATOK for iOS \[Professional\] | ATOK Passport |【公式】ATOK.com, 5月 24, 2025にアクセス、 [https://atok.com/ios\_pro/](https://atok.com/ios_pro/)  
7. 動作環境 | ATOK Passport |【公式】ATOK.com, 5月 24, 2025にアクセス、 [https://www.atok.com/info/spec.html](https://www.atok.com/info/spec.html)  
8. ATOK for Android \[Professional\] | ATOK Passport |【公式】ATOK.com, 5月 24, 2025にアクセス、 [https://atok.com/android\_pro/](https://atok.com/android_pro/)  
9. ATOK for Android \[Professional\] | ATOK Passport |【公式】ATOK.com, 5月 24, 2025にアクセス、 [https://www.atok.com/android\_pro/](https://www.atok.com/android_pro/)  
10. ATOK for Androidが動作するために必要な環境について \- サポート, 5月 24, 2025にアクセス、 [https://support.justsystems.com/jp/products/atok\_android/faq01.html](https://support.justsystems.com/jp/products/atok_android/faq01.html)  
11. 10年以上Apple製品を愛用してきた僕が、自分なりのMac効率化Tipsをまとめてみた \- note, 5月 24, 2025にアクセス、 [https://note.com/mst727/n/ne0d8a72a2b84](https://note.com/mst727/n/ne0d8a72a2b84)  
12. これは便利\! Ctrlキー2回で呼び出せる全画面メモ「ATOK Pad」 | マイナビニュース, 5月 24, 2025にアクセス、 [https://news.mynavi.jp/article/20100610-atokpad/](https://news.mynavi.jp/article/20100610-atokpad/)  
13. ATOK PadがEvernoteと「メモ同期」ができるようになりました！, 5月 24, 2025にアクセス、 [https://www.atok.com/function/atokpad/](https://www.atok.com/function/atokpad/)  
14. ATOK Passport｜Products \- JustSystems Corporation, 5月 24, 2025にアクセス、 [https://www.justsystems.com/en/products/atok/](https://www.justsystems.com/en/products/atok/)  
15. JUST STORIES \- ATOK \- JustSystems Corporation, 5月 24, 2025にアクセス、 [https://www.justsystems.com/en/stories/atok-passport.html](https://www.justsystems.com/en/stories/atok-passport.html)  
16. ATOK Passportの評判・口コミ 全29件 \- ITreview, 5月 24, 2025にアクセス、 [https://www.itreview.jp/products/atok-passport/reviews](https://www.itreview.jp/products/atok-passport/reviews)  
17. 【必要？】ATOK Passportを使ってみた感想・メリット、デメリット【レビュー】 | yalkey Blog, 5月 24, 2025にアクセス、 [https://yalkey.net/atok-passport/](https://yalkey.net/atok-passport/)  
18. 動作環境 | ATOK Passport |【公式】ATOK.com, 5月 24, 2025にアクセス、 [https://atok.com/info/spec.html](https://atok.com/info/spec.html)  
19. 「一太郎Pad」の特長 | 一太郎Pad \- スマホやタブレットと連携 ..., 5月 24, 2025にアクセス、 [https://www.justsystems.com/jp/products/ichitaropad/features/feature01.html](https://www.justsystems.com/jp/products/ichitaropad/features/feature01.html)  
20. 商品トップ | 一太郎Pad \- スマホやタブレットと連携 一太郎Pad登場 ..., 5月 24, 2025にアクセス、 [https://www.justsystems.com/jp/products/ichitaropad/](https://www.justsystems.com/jp/products/ichitaropad/)  
21. 「一太郎Pad」をApp Storeで, 5月 24, 2025にアクセス、 [https://apps.apple.com/jp/app/%E4%B8%80%E5%A4%AA%E9%83%8Epad/id1490522571](https://apps.apple.com/jp/app/%E4%B8%80%E5%A4%AA%E9%83%8Epad/id1490522571)  
22. iOS用メモアプリ「一太郎Pad」 \- S2ファンサイト, 5月 24, 2025にアクセス、 [https://s2.mukairyoji.com/archives/2726](https://s2.mukairyoji.com/archives/2726)  
23. 動作環境 | 一太郎2025 \- 日本語ワープロソフト | ジャストシステム \- JustSystems Corporation, 5月 24, 2025にアクセス、 [https://www.justsystems.com/jp/products/ichitaro/features/spec.html](https://www.justsystems.com/jp/products/ichitaro/features/spec.html)  
24. 旧バージョン比較 | 一太郎2025 \- 日本語ワープロソフト | ジャストシステム, 5月 24, 2025にアクセス、 [https://www.justsystems.com/jp/products/ichitaro/features/comparing.html](https://www.justsystems.com/jp/products/ichitaro/features/comparing.html)  
25. Windows 標準の「付箋」アプリの上手な使い方 \- 横河レンタ・リース, 5月 24, 2025にアクセス、 [https://www.yrl.com/column/wazaari\_pc/sticky-notes.html](https://www.yrl.com/column/wazaari_pc/sticky-notes.html)  
26. Windows 10の付箋（Sticky Notes）で使用できるショートカットキーについて \- NEC, 5月 24, 2025にアクセス、 [https://support.nec-lavie.jp/qasearch/1007/app/servlet/relatedqa?QID=021160](https://support.nec-lavie.jp/qasearch/1007/app/servlet/relatedqa?QID=021160)  
27. Windows 10 の付箋アプリで何ができる？活用するメリットなどを解説 | Tech & Device TV \- HP, 5月 24, 2025にアクセス、 [https://jp.ext.hp.com/techdevice/windows10sc/39/](https://jp.ext.hp.com/techdevice/windows10sc/39/)  
28. 日本語入力は ATOK がとっても便利なことを知ってもらいたい \- エージェントグロー, 5月 24, 2025にアクセス、 [https://www.agent-grow.com/self20percent/2019/05/13/atok-is-the-best-for-japanese-input/](https://www.agent-grow.com/self20percent/2019/05/13/atok-is-the-best-for-japanese-input/)  
29. ペンでもOK！ サクッとメモを取りたいときに最適なショートカットキー \- 窓の杜, 5月 24, 2025にアクセス、 [https://forest.watch.impress.co.jp/docs/shseri/usefulkeys/1467371.html](https://forest.watch.impress.co.jp/docs/shseri/usefulkeys/1467371.html)  
30. 【AutoHotkey】修飾キーの使い方と使用例 \- オカメJP, 5月 24, 2025にアクセス、 [https://ocamejp.com/autohotkey-modifier/](https://ocamejp.com/autohotkey-modifier/)  
31. AutoHotkeyを使ってWindowsパソコンを快適にカスタマイズ \- YouTube, 5月 24, 2025にアクセス、 [https://www.youtube.com/watch?v=APjG2RODCzc](https://www.youtube.com/watch?v=APjG2RODCzc)  
32. 付箋アプリ Sticky Notesとは？便利な使い方や消えた時の復元方法を解説, 5月 24, 2025にアクセス、 [https://biz.moneyforward.com/work-efficiency/basic/5132/](https://biz.moneyforward.com/work-efficiency/basic/5132/)  
33. ATOKを使っている｜クー \- note, 5月 24, 2025にアクセス、 [https://note.com/iiboshi0808/n/nf5d347940186](https://note.com/iiboshi0808/n/nf5d347940186)  
34. FMV Q\&A \- \[ATOK\] ローマ字漢字入力とカナ漢字入力を切り替える方法を教えてください。, 5月 24, 2025にアクセス、 [https://www.fmworld.net/cs/azbyclub/qanavi/jsp/qacontents.jsp?PID=7110-9315](https://www.fmworld.net/cs/azbyclub/qanavi/jsp/qacontents.jsp?PID=7110-9315)  
35. Macの「メモ」のキーボードショートカットとジェスチャ \- Apple Support, 5月 24, 2025にアクセス、 [https://support.apple.com/ja-jp/guide/notes/apd46c25187e/mac](https://support.apple.com/ja-jp/guide/notes/apd46c25187e/mac)  
36. Macでクイックメモを作成する \- Apple Support, 5月 24, 2025にアクセス、 [https://support.apple.com/ja-jp/guide/notes/apdf028f7034/mac](https://support.apple.com/ja-jp/guide/notes/apdf028f7034/mac)  
37. 【Mac Tips】クイックメモをショートカットキーで爆速で呼び出す方法｜風士郎 \- note, 5月 24, 2025にアクセス、 [https://note.com/fuushirou/n/n9c4cc7b99ab5](https://note.com/fuushirou/n/n9c4cc7b99ab5)  
38. 【レビュー】MacにATOKは必要？ライブ変換搭載のmacOS日本語入力と比較 \- iPhone Mania, 5月 24, 2025にアクセス、 [https://iphone-mania.jp/news-457657/](https://iphone-mania.jp/news-457657/)  
39. 久しぶりにATOKを使ったら最高だった\!\!\! \- ケータイ Watch \- インプレス, 5月 24, 2025にアクセス、 [https://k-tai.watch.impress.co.jp/docs/column/stapaapple/1520433.html](https://k-tai.watch.impress.co.jp/docs/column/stapaapple/1520433.html)  
40. Mac新調したのでアプリや設定の個人的な棚卸し \- Qiita, 5月 24, 2025にアクセス、 [https://qiita.com/kawaz/items/952cb1a86b1da77cd7ab](https://qiita.com/kawaz/items/952cb1a86b1da77cd7ab)  
41. ATOK Pad の使い方（Mac）, 5月 24, 2025にアクセス、 [https://www.atok.com/useful/valueup/atokpad/mac.html](https://www.atok.com/useful/valueup/atokpad/mac.html)  
42. Mac用メモユーザガイド \- Apple サポート (日本) \- Apple Support, 5月 24, 2025にアクセス、 [https://support.apple.com/ja-jp/guide/notes/welcome/mac](https://support.apple.com/ja-jp/guide/notes/welcome/mac)  
43. MS IME、ATOK、Google 日本語入力、一番使いやすいのはどれだ？ATOK信者が比べてみた, 5月 24, 2025にアクセス、 [https://pc.watch.impress.co.jp/docs/topic/feature/1600422.html](https://pc.watch.impress.co.jp/docs/topic/feature/1600422.html)  
44. サクラエディタの評判・口コミ 全686件 \- ITreview, 5月 24, 2025にアクセス、 [https://www.itreview.jp/products/sakuraeditor/reviews](https://www.itreview.jp/products/sakuraeditor/reviews)  
45. サクラエディタをもっと使いやすくするために最初にやる6つのこと \- Qiita, 5月 24, 2025にアクセス、 [https://qiita.com/moromi25/items/70e638a3d47894ca7d6c](https://qiita.com/moromi25/items/70e638a3d47894ca7d6c)  
46. オープンソースで開発されている老舗のテキストエディター「サクラエディタ」 \- 窓の杜, 5月 24, 2025にアクセス、 [https://forest.watch.impress.co.jp/docs/review/527310.html](https://forest.watch.impress.co.jp/docs/review/527310.html)  
47. サクラエディタ, 5月 24, 2025にアクセス、 [https://sakura-editor.github.io/](https://sakura-editor.github.io/)  
48. 1月 1, 1970にアクセス、 [https://sakura-editor.github.io/community.html](https://sakura-editor.github.io/community.html)  
49. 1月 1, 1970にアクセス、 [https://sakura-editor.github.io/bbs.html](https://sakura-editor.github.io/bbs.html)  
50. サクラエディタ ヘルプ目次, 5月 24, 2025にアクセス、 [https://sakura-editor.github.io/help/](https://sakura-editor.github.io/help/)  
51. 共通設定 『全般』プロパティ \- サクラエディタ, 5月 24, 2025にアクセス、 [https://sakura-editor.github.io/help/HLP000081.html](https://sakura-editor.github.io/help/HLP000081.html)  
52. ATOKは不要？「本当に必要か」ATOKユーザーの筆者がレビュー【他IMEとの比較】, 5月 24, 2025にアクセス、 [https://sumaholife-plus.jp/pc\_it/19749/](https://sumaholife-plus.jp/pc_it/19749/)  
53. みんなのケータイ, 5月 24, 2025にアクセス、 [https://k-tai.watch.impress.co.jp/docs/column/minna/index\_c236s736.html](https://k-tai.watch.impress.co.jp/docs/column/minna/index_c236s736.html)  
54. PCサポート | PCネットワークサポートブログ | 株式会社ベンハウス｜姫路でパソコンサポート・ITサポート・ITセキュリティ・複合機・ビジネスフォンなら弊社にお任せ, 5月 24, 2025にアクセス、 [https://www.benhouse.co.jp/blog/category/28483/](https://www.benhouse.co.jp/blog/category/28483/)  
55. ガラホのLTE通信を限界まで使って分かった7つのこと \- ケータイ Watch \- インプレス, 5月 24, 2025にアクセス、 [https://k-tai.watch.impress.co.jp/docs/column/minna/index\_c235s726.html](https://k-tai.watch.impress.co.jp/docs/column/minna/index_c235s726.html)  
56. WindowsエクスプローラのDropboxフォルダ上にあるOfficeファイルが開けない, 5月 24, 2025にアクセス、 [https://www.dropboxforum.com/discussions/107001000/windows%E3%82%A8%E3%82%AF%E3%82%B9%E3%83%97%E3%83%AD%E3%83%BC%E3%83%A9%E3%81%AEdropbox%E3%83%95%E3%82%A9%E3%83%AB%E3%83%80%E4%B8%8A%E3%81%AB%E3%81%82%E3%82%8Boffice%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E3%81%8C%E9%96%8B%E3%81%91%E3%81%AA%E3%81%84/802018](https://www.dropboxforum.com/discussions/107001000/windows%E3%82%A8%E3%82%AF%E3%82%B9%E3%83%97%E3%83%AD%E3%83%BC%E3%83%A9%E3%81%AEdropbox%E3%83%95%E3%82%A9%E3%83%AB%E3%83%80%E4%B8%8A%E3%81%AB%E3%81%82%E3%82%8Boffice%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E3%81%8C%E9%96%8B%E3%81%91%E3%81%AA%E3%81%84/802018)  
57. サクラエディタはWindows11でも動く？ダウンロード対象とインストール方法 \- プロエンジニア, 5月 24, 2025にアクセス、 [https://proengineer.internous.co.jp/content/columnfeature/5319](https://proengineer.internous.co.jp/content/columnfeature/5319)  
58. Notepad++の評判・口コミ 全34件 \- ITreview, 5月 24, 2025にアクセス、 [https://www.itreview.jp/products/notepad-plus-plus/reviews](https://www.itreview.jp/products/notepad-plus-plus/reviews)  
59. 【おすすめ】一太郎の強み | Wordとの比較 注意すべき点もあります, 5月 24, 2025にアクセス、 [https://masugar.com/novel\_ichitaro\_word/](https://masugar.com/novel_ichitaro_word/)  
60. めんどくさがりでもできるVSCodeを使ったノートのとり方とドキュメント化について \- Zenn, 5月 24, 2025にアクセス、 [https://zenn.dev/optimisuke/articles/9e60519d9a506699d701](https://zenn.dev/optimisuke/articles/9e60519d9a506699d701)  
61. 対応機種一覧 \- SPPM Security One, 5月 24, 2025にアクセス、 [https://www.sppm.jp/models/](https://www.sppm.jp/models/)  
62. 【SSS】どこよりも詳しいKeePass自動入力などの設定と使い方 \- やりすぎセキュリティ, 5月 24, 2025にアクセス、 [https://excesssecurity.com/keepass-advanced-auto-type/](https://excesssecurity.com/keepass-advanced-auto-type/)  
63. パソコン同士で手軽にファイルを共有したい！WindowsやMacでのファイル共有方法 \- PC Watch, 5月 24, 2025にアクセス、 [https://pc.watch.impress.co.jp/docs/topic/feature/1447860.html](https://pc.watch.impress.co.jp/docs/topic/feature/1447860.html)  
64. エンジニアのための日本語校正ツール \#VSCode \- Qiita, 5月 24, 2025にアクセス、 [https://qiita.com/masato\_makino/items/3fa7983f0873c95e49e7](https://qiita.com/masato_makino/items/3fa7983f0873c95e49e7)  
65. 【VSCode拡張】Foamを使ってZettelkasten方式でメモを取る方法 \- Zenn, 5月 24, 2025にアクセス、 [https://zenn.dev/a\_kun\_hu/articles/foam-vscode-touch](https://zenn.dev/a_kun_hu/articles/foam-vscode-touch)  
66. dendron \- Visual Studio Marketplace, 5月 24, 2025にアクセス、 [https://marketplace.visualstudio.com/items?itemName=dendron.dendron](https://marketplace.visualstudio.com/items?itemName=dendron.dendron)  
67. VScodeでEvernoteみたいなメモアプリを実現する拡張機能を試してみた｜大城杜鵑, 5月 24, 2025にアクセス、 [https://note.com/token\_oki/n/nf7d298df102c](https://note.com/token_oki/n/nf7d298df102c)  
68. NVDA最新情報, 5月 24, 2025にアクセス、 [https://www.nvda.jp/nvda2024.2jp/ja/changes.html](https://www.nvda.jp/nvda2024.2jp/ja/changes.html)  
69. ObsidianのノートをVS CodeのAI（Cline）を通して活用する 〜ローカルにMarkdown形式で保存しているメリットを活かす使い方 | gihyo.jp, 5月 24, 2025にアクセス、 [https://gihyo.jp/article/2025/05/obsidian-06](https://gihyo.jp/article/2025/05/obsidian-06)  
70. VSCode Settings Syncで「設定同期をオン」にしてデバイス間の設定を共有, 5月 24, 2025にアクセス、 [https://webcreatorfile.com/web/git/871/](https://webcreatorfile.com/web/git/871/)  
71. Visual Studio Code公式の設定同期「Settings Sync」を利用する \- Qiita, 5月 24, 2025にアクセス、 [https://qiita.com/Nuits/items/6204a6b0576b7a4e37ea](https://qiita.com/Nuits/items/6204a6b0576b7a4e37ea)  
72. VSCode \+ Git Graph での Git の使い方メモ \- あぱーブログ, 5月 24, 2025にアクセス、 [https://blog.apar.jp/program/19020/](https://blog.apar.jp/program/19020/)  
73. gitの運用ワークフローのメモ（git-flow、github flow等） \- Qiita, 5月 24, 2025にアクセス、 [https://qiita.com/ta-ke-no-bu/items/a9854deb61419a0d64c7](https://qiita.com/ta-ke-no-bu/items/a9854deb61419a0d64c7)  
74. VSCodeで使いたい便利な拡張機能・プラグイン15選 入れ方も解説【Visual Studio Code】, 5月 24, 2025にアクセス、 [https://www.kannart.co.jp/blog/web-hacks/web-coding/14096/](https://www.kannart.co.jp/blog/web-hacks/web-coding/14096/)  
75. Visual Studio Codeに入れるべき拡張機能【2024年最新版】 \- Qiita, 5月 24, 2025にアクセス、 [https://qiita.com/qrrq/items/0e116a59743874d18cb1](https://qiita.com/qrrq/items/0e116a59743874d18cb1)  
76. VSCodeの便利なショートカットキーや小技を手癖にして生産性をあげよう \- Zenn, 5月 24, 2025にアクセス、 [https://zenn.dev/uniformnext/articles/a611721ba0c551](https://zenn.dev/uniformnext/articles/a611721ba0c551)  
77. VS Code の便利なショートカットキー \#VSCode \- Qiita, 5月 24, 2025にアクセス、 [https://qiita.com/12345/items/64f4372fbca041e949d0](https://qiita.com/12345/items/64f4372fbca041e949d0)  
78. VSCode(VisualStudioCode)の定番機能を一挙解説 \- Qiita, 5月 24, 2025にアクセス、 [https://qiita.com/midiambear/items/bc0e137ed77153cb421c](https://qiita.com/midiambear/items/bc0e137ed77153cb421c)  
79. 【新人エンジニア向け】VSCodeがより便利になる知識【part2】 \- 株式会社アイソルート, 5月 24, 2025にアクセス、 [https://www.isoroot.jp/blog/7540/](https://www.isoroot.jp/blog/7540/)  
80. AutoHotkeyのススメ \- Qiita, 5月 24, 2025にアクセス、 [https://qiita.com/ryoheiszk/items/092cc5d76838cb5a13f1](https://qiita.com/ryoheiszk/items/092cc5d76838cb5a13f1)  
81. クライアントのデバッグ｜AutoHotkey v2, 5月 24, 2025にアクセス、 [https://ahkscript.github.io/ja/docs/v2/AHKL\_DBGPClients.htm](https://ahkscript.github.io/ja/docs/v2/AHKL_DBGPClients.htm)  
82. Evernoteの評判・口コミ｜全1112件のユーザー満足度を紹介！ \- ITトレンド, 5月 24, 2025にアクセス、 [https://it-trend.jp/knowledge\_management/11469/review](https://it-trend.jp/knowledge_management/11469/review)  
83. Evernoteの評判・口コミ 全567件 \- ITreview, 5月 24, 2025にアクセス、 [https://www.itreview.jp/products/evernote/reviews](https://www.itreview.jp/products/evernote/reviews)  
84. 最高のノートアプリ \- Evernoteでノートを整理しましょう, 5月 24, 2025にアクセス、 [https://evernote.com/intl/jp](https://evernote.com/intl/jp)  
85. ATOK Pad の使い方（Windows）, 5月 24, 2025にアクセス、 [https://www.atok.com/useful/valueup/atokpad/index\_ver31.html](https://www.atok.com/useful/valueup/atokpad/index_ver31.html)  
86. iText Pad, 5月 24, 2025にアクセス、 [http://www.jp-lightway.com/appstore/iTextPad/jp/](http://www.jp-lightway.com/appstore/iTextPad/jp/)  
87. Evernoteの日本語入力のバグ? \- Evernote for Mac に関する問題 \- Evernote User Forum, 5月 24, 2025にアクセス、 [https://discussion.evernote.com/forums/topic/151445-evernote%E3%81%AE%E6%97%A5%E6%9C%AC%E8%AA%9E%E5%85%A5%E5%8A%9B%E3%81%AE%E3%83%90%E3%82%B0/](https://discussion.evernote.com/forums/topic/151445-evernote%E3%81%AE%E6%97%A5%E6%9C%AC%E8%AA%9E%E5%85%A5%E5%8A%9B%E3%81%AE%E3%83%90%E3%82%B0/)  
88. Evernote Macで日本語入力の変換文字が消える･･･再び \- Evernote Forum, 5月 24, 2025にアクセス、 [https://discussion.evernote.com/forums/topic/134941-evernote-mac%E3%81%A7%E6%97%A5%E6%9C%AC%E8%AA%9E%E5%85%A5%E5%8A%9B%E3%81%AE%E5%A4%89%E6%8F%9B%E6%96%87%E5%AD%97%E3%81%8C%E6%B6%88%E3%81%88%E3%82%8B%EF%BD%A5%EF%BD%A5%EF%BD%A5%E5%86%8D%E3%81%B3/](https://discussion.evernote.com/forums/topic/134941-evernote-mac%E3%81%A7%E6%97%A5%E6%9C%AC%E8%AA%9E%E5%85%A5%E5%8A%9B%E3%81%AE%E5%A4%89%E6%8F%9B%E6%96%87%E5%AD%97%E3%81%8C%E6%B6%88%E3%81%88%E3%82%8B%EF%BD%A5%EF%BD%A5%EF%BD%A5%E5%86%8D%E3%81%B3/)  
89. 【必見】Evernoteが重い・遅いときの原因と対処法とは？ \- Stock, 5月 24, 2025にアクセス、 [https://www.stock-app.info/media/evernote-heavy/](https://www.stock-app.info/media/evernote-heavy/)  
90. 日本語入力プログラム乗り換え \- Yoshii \- Blog, 5月 24, 2025にアクセス、 [http://yoshii-blog.blogspot.com/2013/08/blog-post\_17.html](http://yoshii-blog.blogspot.com/2013/08/blog-post_17.html)  
91. 【保存版】小説家・ライター向け！2020年版執筆ツールアプリ一覧 \- note, 5月 24, 2025にアクセス、 [https://note.com/mikan\_bo/n/na2bc9e898f63](https://note.com/mikan_bo/n/na2bc9e898f63)  
92. 一周回ってEvernoteがいいんじゃないかと思いつつ、とりあえずobsidian×cursorを使ってみることにした、がNew \- デンノウエレキング, 5月 24, 2025にアクセス、 [https://www.eleki.com/weblog/weblog-38014/](https://www.eleki.com/weblog/weblog-38014/)  
93. Amazon | キングジム(Kingjim) デジタルメモ ポメラ 黒 DM200クロ 本体サイズ, 5月 24, 2025にアクセス、 [https://www.amazon.co.jp/%E3%82%AD%E3%83%B3%E3%82%B0%E3%82%B8%E3%83%A0-KINGJIM-DM200%E3%82%AF%E3%83%AD-%E3%83%87%E3%82%B8%E3%82%BF%E3%83%AB%E3%83%A1%E3%83%A2-DM200%E3%83%96%E3%83%A9%E3%83%83%E3%82%AF/dp/B01LXQZ4WI](https://www.amazon.co.jp/%E3%82%AD%E3%83%B3%E3%82%B0%E3%82%B8%E3%83%A0-KINGJIM-DM200%E3%82%AF%E3%83%AD-%E3%83%87%E3%82%B8%E3%82%BF%E3%83%AB%E3%83%A1%E3%83%A2-DM200%E3%83%96%E3%83%A9%E3%83%83%E3%82%AF/dp/B01LXQZ4WI)  
94. Shared: 2018 tabs \- OneTab, 5月 24, 2025にアクセス、 [https://www.one-tab.com/page/0IjJsIYhTpGGWQT3fi1PyQ](https://www.one-tab.com/page/0IjJsIYhTpGGWQT3fi1PyQ)  
95. ニュース＆トピックス \- GEOSISサポートサイト, 5月 24, 2025にアクセス、 [http://geosis.as-locus.jp/topicmain.aspx](http://geosis.as-locus.jp/topicmain.aspx)  
96. 【2019年版】失敗しない名刺管理ソフト・アプリ選び！人気14サービスの特徴を教えます。, 5月 24, 2025にアクセス、 [https://biz.kakaku.com/guide/19030801/](https://biz.kakaku.com/guide/19030801/)  
97. Windows風のタスク切り替えをMacでも実現する \- クリエイティブハック, 5月 24, 2025にアクセス、 [https://creative89.com/2020/08/15/macos-task-switch/](https://creative89.com/2020/08/15/macos-task-switch/)  
98. OneNoteの評判・口コミ 全284件 \- ITreview, 5月 24, 2025にアクセス、 [https://www.itreview.jp/products/onenote/reviews](https://www.itreview.jp/products/onenote/reviews)  
99. OneNoteがクラウド上のOffice文書を貼りつけるとリアルタイム同期可能に \- PC Watch, 5月 24, 2025にアクセス、 [https://pc.watch.impress.co.jp/docs/news/1148594.html](https://pc.watch.impress.co.jp/docs/news/1148594.html)  
100. 【2025年版】オフィススイートおすすめ10選を徹底比較！具体的な機能・メリット・デメリット・選び方まで紹介 \- NotePM, 5月 24, 2025にアクセス、 [https://notepm.jp/blog/21357](https://notepm.jp/blog/21357)  
101. b.hatena.ne.jp, 5月 24, 2025にアクセス、 [https://b.hatena.ne.jp/labunix/search.data](https://b.hatena.ne.jp/labunix/search.data)  
102. 性能で、スタイルで選べる、ダイナブックシリーズ \- Dynabook, 5月 24, 2025にアクセス、 [https://dynabook.com/pc/catalog/dynabook/catapdf/original/pc-717.pdf](https://dynabook.com/pc/catalog/dynabook/catapdf/original/pc-717.pdf)  
103. Microsoft OneNote デジタル ノート アプリ | Microsoft 365, 5月 24, 2025にアクセス、 [https://www.microsoft.com/ja-jp/microsoft-365/onenote/digital-note-taking-app](https://www.microsoft.com/ja-jp/microsoft-365/onenote/digital-note-taking-app)  
104. 【デスクトップ版】Windows/ATOKで日本語入力に難がある | Vivaldi Forum, 5月 24, 2025にアクセス、 [https://forum.vivaldi.net/topic/80556/%E3%83%87%E3%82%B9%E3%82%AF%E3%83%88%E3%83%83%E3%83%97%E7%89%88-windows-atok%E3%81%A7%E6%97%A5%E6%9C%AC%E8%AA%9E%E5%85%A5%E5%8A%9B%E3%81%AB%E9%9B%A3%E3%81%8C%E3%81%82%E3%82%8B](https://forum.vivaldi.net/topic/80556/%E3%83%87%E3%82%B9%E3%82%AF%E3%83%88%E3%83%83%E3%83%97%E7%89%88-windows-atok%E3%81%A7%E6%97%A5%E6%9C%AC%E8%AA%9E%E5%85%A5%E5%8A%9B%E3%81%AB%E9%9B%A3%E3%81%8C%E3%81%82%E3%82%8B)  
105. テキストエディター「Mery」Ver 2.6.7 を公開、やっと正式版です \- Haijin Boys Online, 5月 24, 2025にアクセス、 [https://www.haijin-boys.com/software/mery/mery-2-6-7](https://www.haijin-boys.com/software/mery/mery-2-6-7)  
106. タグ一覧(ランキング順)【直近１年間/上位25000タグ】【2021/1 更新停止】 \- Qiita, 5月 24, 2025にアクセス、 [https://qiita.com/j5c8k6m8/items/b78a14cb8e1fce4ef6d8](https://qiita.com/j5c8k6m8/items/b78a14cb8e1fce4ef6d8)  
107. プレーンテキストによるタスク管理 \- Zenn, 5月 24, 2025にアクセス、 [https://zenn.dev/sta/books/taskmanagement-kamikudaku/viewer/plaintext](https://zenn.dev/sta/books/taskmanagement-kamikudaku/viewer/plaintext)  
108. 無料のクラウド対応メモアプリおすすめ4選 複数デバイス同期・他人と共同編集可能 \- アプリブ, 5月 24, 2025にアクセス、 [https://app-liv.jp/lifestyle/memo/1024/](https://app-liv.jp/lifestyle/memo/1024/)  
109. 人気のメモ帳アプリを、マニア3人がランキング化！ 一番のおすすめはどれ？ \- 新R25, 5月 24, 2025にアクセス、 [https://r25.jp/articles/928885231197487105](https://r25.jp/articles/928885231197487105)  
110. Google Keepって何？基本的な使い方から便利機能まで徹底解説！, 5月 24, 2025にアクセス、 [https://pcnext.shop/blogs/pc-next-blog/google-keep](https://pcnext.shop/blogs/pc-next-blog/google-keep)  
111. Androidスマホのメモアプリ「Google Keep」をもっと使いこなす小技9選 \- スマホライフPLUS, 5月 24, 2025にアクセス、 [https://sumaholife-plus.jp/smartphone/3637/](https://sumaholife-plus.jp/smartphone/3637/)  
112. 「Galaxy S23 Ultra」、『撮る』『観る』『描く』で楽しめる史上最強のGalaxy \- ケータイ Watch, 5月 24, 2025にアクセス、 [https://k-tai.watch.impress.co.jp/docs/column/mobile\_catchup/1499855.html](https://k-tai.watch.impress.co.jp/docs/column/mobile_catchup/1499855.html)  
113. 【山田祥平のRe:config.sys】あらゆるアプリを同じ操作で \- PC Watch \- インプレス, 5月 24, 2025にアクセス、 [https://pc.watch.impress.co.jp/docs/column/config/1270858.html](https://pc.watch.impress.co.jp/docs/column/config/1270858.html)  
114. Sign in \- Google Accounts, 5月 24, 2025にアクセス、 [https://keep.google.com/](https://keep.google.com/)  
115. \[057055\]入力や変換の速度が遅い場合の確認事項 \- サポート \- JustSystems Corporation, 5月 24, 2025にアクセス、 [https://support.justsystems.com/faq/1032/app/servlet/qadoc?QID=057055](https://support.justsystems.com/faq/1032/app/servlet/qadoc?QID=057055)  
116. 「親指シフト」のすゝめ \- SyntaxCloud, 5月 24, 2025にアクセス、 [https://syn-c.jp/memo/oyayubi-shift/](https://syn-c.jp/memo/oyayubi-shift/)  
117. noteの執筆に純正メモよりATOKPadを使う理由【これで100日の壁を超えた】, 5月 24, 2025にアクセス、 [https://note.com/duppyclub/n/nb06679655e11](https://note.com/duppyclub/n/nb06679655e11)  
118. Google Keepの評判・口コミ 全361件 \- ITreview, 5月 24, 2025にアクセス、 [https://www.itreview.jp/products/google-keep/reviews](https://www.itreview.jp/products/google-keep/reviews)  
119. Google 日本語入力の評判・口コミ 全12件 \- ITreview, 5月 24, 2025にアクセス、 [https://www.itreview.jp/products/google-ime/reviews](https://www.itreview.jp/products/google-ime/reviews)  
120. Google Keep のキーボード ショートカット \- パソコン, 5月 24, 2025にアクセス、 [https://support.google.com/keep/answer/12862970?hl=ja\&co=GENIE.Platform%3DDesktop](https://support.google.com/keep/answer/12862970?hl=ja&co=GENIE.Platform%3DDesktop)  
121. Google Keep ヘルプ, 5月 24, 2025にアクセス、 [https://support.google.com/keep/faq/3316156?hl=ja](https://support.google.com/keep/faq/3316156?hl=ja)  
122. Simplenoteの評判・口コミ 全17件 \- ITreview, 5月 24, 2025にアクセス、 [https://www.itreview.jp/products/simplenote/reviews](https://www.itreview.jp/products/simplenote/reviews)  
123. ２０２２年４月 \- 産婦人科 長尾クリニック（広島市）ホームページ, 5月 24, 2025にアクセス、 [https://www.nagao-clinic.gr.jp/diary/d17.html](https://www.nagao-clinic.gr.jp/diary/d17.html)  
124. 使用ツールの選択とみんなの愛用ツール｜ソナーズマガジン（旧マシュマロマガジン） \- note, 5月 24, 2025にアクセス、 [https://note.com/novel/n/n225253e241b4](https://note.com/novel/n/n225253e241b4)  
125. Simplenoteの価格（料金・費用） \- ITreview, 5月 24, 2025にアクセス、 [https://www.itreview.jp/products/simplenote/price](https://www.itreview.jp/products/simplenote/price)  
126. Simplenote のショートカットキー \#Markdown \- Qiita, 5月 24, 2025にアクセス、 [https://qiita.com/Ouvill/items/1d38512988c0f91fe658](https://qiita.com/Ouvill/items/1d38512988c0f91fe658)  
127. Simplenote のショートカットについて \- Ouvill のブログ, 5月 24, 2025にアクセス、 [https://blog.ouvill.net/blog/2018-03-11-simplenote\_shortcut/](https://blog.ouvill.net/blog/2018-03-11-simplenote_shortcut/)  
128. エンジニアが「殴り書き」するためのアプリ、そろそろどれが一番か決めませんか？【15種＋αを試してみた】 | 株式会社LIG(リグ)｜DX支援・システム開発・Web制作, 5月 24, 2025にアクセス、 [https://liginc.co.jp/436448](https://liginc.co.jp/436448)  
129. 気になったウェブページ \- Hail2u, 5月 24, 2025にアクセス、 [https://hail2u.net/links/](https://hail2u.net/links/)  
130. タグ一覧(アルファベット順)【直近１年間/上位25,000タグ】【2021/1 更新停止】 \#Qiita \- Qiita, 5月 24, 2025にアクセス、 [https://qiita.com/j5c8k6m8/items/6b15a81204a1d458e392](https://qiita.com/j5c8k6m8/items/6b15a81204a1d458e392)  
131. Google Pixel背面をファンクションボタンに！超効率派のメモ作成は「クイックタップ」におまかせ【今日のワークハック】 \- ライフハッカー, 5月 24, 2025にアクセス、 [https://www.lifehacker.jp/article/2303-quickly-take-note-google-pixel-smartphone/](https://www.lifehacker.jp/article/2303-quickly-take-note-google-pixel-smartphone/)  
132. BOOXとATOKで快適執筆生活｜kujirahand \- note, 5月 24, 2025にアクセス、 [https://note.com/kujirahand/n/n2520012c68c9](https://note.com/kujirahand/n/n2520012c68c9)  
133. Simplenote, 5月 24, 2025にアクセス、 [https://simplenote.com/](https://simplenote.com/)  
134. Evernoteを捨てる？2025年、最高のEvernote代替ソフトを発見しよう \- ClickUp, 5月 24, 2025にアクセス、 [https://clickup.com/ja/blog/6718/evernote-alternatives](https://clickup.com/ja/blog/6718/evernote-alternatives)  
135. 【2024年版】Evernoteの代替アプリ15選！代わりになるノートの機能も解説, 5月 24, 2025にアクセス、 [https://www.sungrove.co.jp/alternative-to-evernote/](https://www.sungrove.co.jp/alternative-to-evernote/)  
136. ９年使ったEvernoteに別れを告げ、UpNoteへ移住する｜くまもり, 5月 24, 2025にアクセス、 [https://note.com/naiteikumamori/n/nc771384c1d47](https://note.com/naiteikumamori/n/nc771384c1d47)  
137. Joplin 使い方の小さな小さなヒント \- メモ｜ma33 \- note, 5月 24, 2025にアクセス、 [https://note.com/ma3a3anote/n/ndc377b4bfcd0](https://note.com/ma3a3anote/n/ndc377b4bfcd0)  
138. Global hotkey/shortcut for activating a running Joplin instance? \- Features, 5月 24, 2025にアクセス、 [https://discourse.joplinapp.org/t/global-hotkey-shortcut-for-activating-a-running-joplin-instance/6518](https://discourse.joplinapp.org/t/global-hotkey-shortcut-for-activating-a-running-joplin-instance/6518)  
139. macOS で Visual Studio Code を使うためのアレコレ (2021/01/01) \- Qiita, 5月 24, 2025にアクセス、 [https://qiita.com/satokaz/items/6a6a0d9b6489ec2d1803](https://qiita.com/satokaz/items/6a6a0d9b6489ec2d1803)  
140. 取扱説明書 FOMA F883i \- NTTドコモ, 5月 24, 2025にアクセス、 [https://www.docomo.ne.jp/binary/pdf/support/manual/f883i/F883i\_J\_All.pdf](https://www.docomo.ne.jp/binary/pdf/support/manual/f883i/F883i_J_All.pdf)  
141. Joplin, 5月 24, 2025にアクセス、 [https://joplinapp.org/](https://joplinapp.org/)  
142. Joplin(ジョプリン)は使いづらい？機能や使い方、評判を解説！ \- Stock, 5月 24, 2025にアクセス、 [https://www.stock-app.info/media/joplin/](https://www.stock-app.info/media/joplin/)  
143. EvernoteからJoplinに移行しました \- hagi-tech, 5月 24, 2025にアクセス、 [https://hagi-tech.com/joplin/](https://hagi-tech.com/joplin/)  
144. 「Standard Notes」をApp Storeで, 5月 24, 2025にアクセス、 [https://apps.apple.com/jp/app/standard-notes/id1285392450](https://apps.apple.com/jp/app/standard-notes/id1285392450)  
145. メモ同期アプリの比較｜如月翔也＠ゲームとガジェット好きAmazon Vineレビュアー \- note, 5月 24, 2025にアクセス、 [https://note.com/showya\_kiss/n/nbd7f52eef4dd](https://note.com/showya_kiss/n/nbd7f52eef4dd)  
146. OS:Windows 10 Homeのノートパソコン 人気売れ筋ランキング \- 価格.com, 5月 24, 2025にアクセス、 [https://kakaku.com/pc/note-pc/itemlist.aspx?pdf\_Spec105=26](https://kakaku.com/pc/note-pc/itemlist.aspx?pdf_Spec105=26)  
147. ジャストシステム ATOK 2017 for Windows \[ベーシック\] アカデミック版 1276683, 5月 24, 2025にアクセス、 [https://www.yamada-denkiweb.com/2054865017/](https://www.yamada-denkiweb.com/2054865017/)  
148. Standard 版としてインストールした Notes クライアントを Basic 版として起動する方法, 5月 24, 2025にアクセス、 [https://support.hcl-software.com/csm?id=kb\_article\&sysparm\_article=KB0026082](https://support.hcl-software.com/csm?id=kb_article&sysparm_article=KB0026082)  
149. 全グローバルホットキーを表示して使っているアプリを突き止める無料ツールが公開 \- 窓の杜, 5月 24, 2025にアクセス、 [https://forest.watch.impress.co.jp/docs/news/1459180.html](https://forest.watch.impress.co.jp/docs/news/1459180.html)  
150. 取扱説明書, 5月 24, 2025にアクセス、 [http://153.127.244.43/pdf/2012-11-16/16383.pdf](http://153.127.244.43/pdf/2012-11-16/16383.pdf)  
151. 取扱説明書 ［F-12C］ \- NTTドコモ, 5月 24, 2025にアクセス、 [https://www.docomo.ne.jp/binary/pdf/support/manual/F-12C\_J\_OP\_All.pdf](https://www.docomo.ne.jp/binary/pdf/support/manual/F-12C_J_OP_All.pdf)  
152. HHKBをWindowsとMacで切り替えて使う \- \- グローバルプロジェクトマネージャーへの道, 5月 24, 2025にアクセス、 [http://rinbo88.blog.fc2.com/blog-entry-108.html?sp](http://rinbo88.blog.fc2.com/blog-entry-108.html?sp)  
153. ショートカットキーでShiftキーの不具合 \- MuseScore, 5月 24, 2025にアクセス、 [https://musescore.org/ja/node/366268](https://musescore.org/ja/node/366268)  
154. ATOK for Windows 基本的な使い方, 5月 24, 2025にアクセス、 [https://atok.com/other/support/howtouse/windows/atok35w.pdf](https://atok.com/other/support/howtouse/windows/atok35w.pdf)  
155. タナナことば研究室: 2014年10月 アーカイブ \- 東京外国語大学, 5月 24, 2025にアクセス、 [https://www.tufs.ac.jp/blog/ts/p/tanana/2014/10/](https://www.tufs.ac.jp/blog/ts/p/tanana/2014/10/)  
156. Standard Notes | End-To-End Encrypted Notes App, 5月 24, 2025にアクセス、 [https://standardnotes.com/](https://standardnotes.com/)  
157. Macのテキストエディタは「Ulysses」がイチ推し\! の7つの理由 \- PC Watch, 5月 24, 2025にアクセス、 [https://pc.watch.impress.co.jp/docs/column/macinfo/1323008.html](https://pc.watch.impress.co.jp/docs/column/macinfo/1323008.html)  
158. 外出先で気持ちよく文字入力するなら、やっぱりMacBookでしょ | クリエイティブハック, 5月 24, 2025にアクセス、 [https://creative89.com/2017/06/20/review-macbook/](https://creative89.com/2017/06/20/review-macbook/)  
159. 「Ulysses: テキストエディタ」をApp Storeで \- Apple, 5月 24, 2025にアクセス、 [https://apps.apple.com/jp/app/ulysses-%E3%83%86%E3%82%AD%E3%82%B9%E3%83%88%E3%82%A8%E3%83%87%E3%82%A3%E3%82%BF/id1225570693](https://apps.apple.com/jp/app/ulysses-%E3%83%86%E3%82%AD%E3%82%B9%E3%83%88%E3%82%A8%E3%83%87%E3%82%A3%E3%82%BF/id1225570693)  
160. backspace.fm のtitleとshow noteのword cloudによる可視化 \- GitHub Gist, 5月 24, 2025にアクセス、 [https://gist.github.com/chezou/01f0765b3a980ea4c58e04199d7b1734](https://gist.github.com/chezou/01f0765b3a980ea4c58e04199d7b1734)  
161. タナナことば研究室: 2014年9月 アーカイブ \- 東京外国語大学, 5月 24, 2025にアクセス、 [https://www.tufs.ac.jp/blog/ts/p/tanana/2014/09/](https://www.tufs.ac.jp/blog/ts/p/tanana/2014/09/)  
162. Ulyssesが急にiCloud同期しなくなった時の対処法3点 \- Hacks for Creative Life\!, 5月 24, 2025にアクセス、 [https://hacks.beck1240.com/tech/trouble-shooting/9272/](https://hacks.beck1240.com/tech/trouble-shooting/9272/)  
163. Ulysses, 5月 24, 2025にアクセス、 [https://ulysses.app/](https://ulysses.app/)  
164. Ulysses (Page 1), 5月 24, 2025にアクセス、 [https://ulysses.app/blog/](https://ulysses.app/blog/)  
165. 1月 1, 1970にアクセス、 [https://apps.apple.com/jp/app/ulysses-text-editor/id1225570693?mt=12](https://apps.apple.com/jp/app/ulysses-text-editor/id1225570693?mt=12)  
166. ulysses.app, 5月 24, 2025にアクセス、 [https://ulysses.app/kb](https://ulysses.app/kb)  
167. ミルトークとは？評判･口コミや料金について | SaaS比較サイト \- SheepDog, 5月 24, 2025にアクセス、 [https://sheepdog.co.jp/enquete/milltalk/](https://sheepdog.co.jp/enquete/milltalk/)  
168. 事業者の行政処分情報検索 ｜ 自動車総合安全情報 \- 国土交通省, 5月 24, 2025にアクセス、 [https://www.mlit.go.jp/jidosha/anzen/03punishment/cgi-bin/list.cgi](https://www.mlit.go.jp/jidosha/anzen/03punishment/cgi-bin/list.cgi)  
169. 【Mac対応】メモアプリBearとは？使い方や料金、評判まで紹介 \- Stock, 5月 24, 2025にアクセス、 [https://www.stock-app.info/media/bear/](https://www.stock-app.info/media/bear/)  
170. 「Bear \- プライベートメモ」をApp Storeで \- Apple, 5月 24, 2025にアクセス、 [https://apps.apple.com/jp/app/bear-%E3%83%97%E3%83%A9%E3%82%A4%E3%83%99%E3%83%BC%E3%83%88%E3%83%A1%E3%83%A2/id1016366447](https://apps.apple.com/jp/app/bear-%E3%83%97%E3%83%A9%E3%82%A4%E3%83%99%E3%83%BC%E3%83%88%E3%83%A1%E3%83%A2/id1016366447)  
171. 2023年、契約してよかったサブスク&止めたサブスク一覧｜平野太一 \- note, 5月 24, 2025にアクセス、 [https://note.com/yriica/n/nf0ed6fdf3500](https://note.com/yriica/n/nf0ed6fdf3500)  
172. ITmedia \+D PCUPdate：2006年4月の記事一覧, 5月 24, 2025にアクセス、 [https://www.itmedia.co.jp/pcupdate/news/0604.html](https://www.itmedia.co.jp/pcupdate/news/0604.html)  
173. 【大幅進化】神アプデされた使い勝手抜群のメモアプリ、知ってる？ \- YouTube, 5月 24, 2025にアクセス、 [https://www.youtube.com/watch?v=iNChblTkFhs](https://www.youtube.com/watch?v=iNChblTkFhs)  
174. ATOK \[Professional\] 日本語入力キーボード 4+ \- App Store \- Apple, 5月 24, 2025にアクセス、 [https://apps.apple.com/jp/app/atok-professional-%E6%97%A5%E6%9C%AC%E8%AA%9E%E5%85%A5%E5%8A%9B%E3%82%AD%E3%83%BC%E3%83%9C%E3%83%BC%E3%83%89/id1568070609](https://apps.apple.com/jp/app/atok-professional-%E6%97%A5%E6%9C%AC%E8%AA%9E%E5%85%A5%E5%8A%9B%E3%82%AD%E3%83%BC%E3%83%9C%E3%83%BC%E3%83%89/id1568070609)  
175. ショートカットキーの設定方法は？ \- Parblo Support, 5月 24, 2025にアクセス、 [https://support.parblo.com/hc/ja/articles/900002712523-%E3%82%B7%E3%83%A7%E3%83%BC%E3%83%88%E3%82%AB%E3%83%83%E3%83%88%E3%82%AD%E3%83%BC%E3%81%AE%E8%A8%AD%E5%AE%9A%E6%96%B9%E6%B3%95%E3%81%AF](https://support.parblo.com/hc/ja/articles/900002712523-%E3%82%B7%E3%83%A7%E3%83%BC%E3%83%88%E3%82%AB%E3%83%83%E3%83%88%E3%82%AD%E3%83%BC%E3%81%AE%E8%A8%AD%E5%AE%9A%E6%96%B9%E6%B3%95%E3%81%AF)  
176. カスタムホットキー \- Obsidian 日本語ヘルプ, 5月 24, 2025にアクセス、 [https://publish.obsidian.md/help-ja/%E3%82%AB%E3%82%B9%E3%82%BF%E3%83%9E%E3%82%A4%E3%82%BA/%E3%82%AB%E3%82%B9%E3%82%BF%E3%83%A0%E3%83%9B%E3%83%83%E3%83%88%E3%82%AD%E3%83%BC](https://publish.obsidian.md/help-ja/%E3%82%AB%E3%82%B9%E3%82%BF%E3%83%9E%E3%82%A4%E3%82%BA/%E3%82%AB%E3%82%B9%E3%82%BF%E3%83%A0%E3%83%9B%E3%83%83%E3%83%88%E3%82%AD%E3%83%BC)  
177. 「Bear \- プライベートメモ」をMac App Storeで \- Apple, 5月 24, 2025にアクセス、 [https://apps.apple.com/jp/app/bear-%E3%83%97%E3%83%A9%E3%82%A4%E3%83%99%E3%83%BC%E3%83%88%E3%83%A1%E3%83%A2/id1091189122?mt=12](https://apps.apple.com/jp/app/bear-%E3%83%97%E3%83%A9%E3%82%A4%E3%83%99%E3%83%BC%E3%83%88%E3%83%A1%E3%83%A2/id1091189122?mt=12)  
178. Bear: Markdown Notes 4+ \- Mac App Store, 5月 24, 2025にアクセス、 [https://apps.apple.com/us/app/bear-markdown-notes/id1091189122?mt=12](https://apps.apple.com/us/app/bear-markdown-notes/id1091189122?mt=12)  
179. astah製品のキーボードショートカット, 5月 24, 2025にアクセス、 [https://astah.change-vision.com/ja/tutorial/shortcut-key.html](https://astah.change-vision.com/ja/tutorial/shortcut-key.html)  
180. Bear \- Markdown Notes, 5月 24, 2025にアクセス、 [https://bear.app/](https://bear.app/)  
181. 1月 1, 1970にアクセス、 [https://bear.app/blog/](https://bear.app/blog/)  
182. 1月 1, 1970にアクセス、 [https://apps.apple.com/jp/app/bear-markdown-notes/id1016366447?mt=12](https://apps.apple.com/jp/app/bear-markdown-notes/id1016366447?mt=12)  
183. Lost in space? Bear is here to help. \- Bear App, 5月 24, 2025にアクセス、 [https://bear.app/faq/](https://bear.app/faq/)  
184. ATOK Proの評判・口コミ 全7件 \- ITreview, 5月 24, 2025にアクセス、 [https://www.itreview.jp/products/atok-pro/reviews](https://www.itreview.jp/products/atok-pro/reviews)  
185. デジタルメモ“ポメラDM250”レビュー。文章作成のみのガジェットだけど買ってよかった。「ポメラはいいぞ」とWebライター目線で語らせて | ゲーム・エンタメ最新情報のファミ通.com, 5月 24, 2025にアクセス、 [https://www.famitsu.com/news/202403/27337961.html](https://www.famitsu.com/news/202403/27337961.html)  
186. 最強のメモアプリは？ Craftを使ってみた！｜りょう \- note, 5月 24, 2025にアクセス、 [https://note.com/ryou0312/n/nea32084ace40](https://note.com/ryou0312/n/nea32084ace40)  
187. 注目の神メモアプリ「Craft」の魅力と使い方を徹底解説！【Notionとの違いも解説】 \- YouTube, 5月 24, 2025にアクセス、 [https://www.youtube.com/watch?v=5REj49MFqlU](https://www.youtube.com/watch?v=5REj49MFqlU)  
188. ミニキーボード 有線 USB 小型 英字 キーボード ローマ字 日本語入力, 5月 24, 2025にアクセス、 [https://c-fox.ch/?f=00004146939105\&channel=b3cbba\&from=goods.php%3Fid%3D1469391-27520%26name%3D%E3%83%9F%E3%83%8B%E3%82%AD%E3%83%BC%E3%83%9C%E3%83%BC%E3%83%89+%E6%9C%89%E7%B7%9A+USB+%E5%B0%8F%E5%9E%8B+%E8%8B%B1%E5%AD%97+%E3%82%AD%E3%83%BC%E3%83%9C%E3%83%BC%E3%83%89+%E3%83%AD%E3%83%BC%E3%83%9E%E5%AD%97+%E6%97%A5%E6%9C%AC%E8%AA%9E%E5%85%A5%E5%8A%9B](https://c-fox.ch/?f=00004146939105&channel=b3cbba&from=goods.php?id%3D1469391-27520%26name%3D%E3%83%9F%E3%83%8B%E3%82%AD%E3%83%BC%E3%83%9C%E3%83%BC%E3%83%89+%E6%9C%89%E7%B7%9A+USB+%E5%B0%8F%E5%9E%8B+%E8%8B%B1%E5%AD%97+%E3%82%AD%E3%83%BC%E3%83%9C%E3%83%BC%E3%83%89+%E3%83%AD%E3%83%BC%E3%83%9E%E5%AD%97+%E6%97%A5%E6%9C%AC%E8%AA%9E%E5%85%A5%E5%8A%9B)  
189. 2015, 5月 24, 2025にアクセス、 [http://namazerpenn.sakura.ne.jp/sakana/blog/2015nennblog.htm](http://namazerpenn.sakura.ne.jp/sakana/blog/2015nennblog.htm)  
190. Keyboard Shortcuts (macOS) \- Craft Help Site, 5月 24, 2025にアクセス、 [https://support.craft.do/hc/en-us/articles/360019555557-Keyboard-Shortcuts-macOS](https://support.craft.do/hc/en-us/articles/360019555557-Keyboard-Shortcuts-macOS)  
191. ホットキー・ショートカット一覧 \- Coffee and Craft, 5月 24, 2025にアクセス、 [https://coffee-craft.net/leathercraft\_cad/shortcut\_keys](https://coffee-craft.net/leathercraft_cad/shortcut_keys)  
192. 「サイト Google 打線組んでみた|海外の反応|世界史専門ブログ, 5月 24, 2025にアクセス、 [https://b.hatena.ne.jp/q/%E3%82%B5%E3%82%A4%E3%83%88%20Google%20%20%E6%89%93%E7%B7%9A%E7%B5%84%E3%82%93%E3%81%A7%E3%81%BF%E3%81%9F%7C%E6%B5%B7%E5%A4%96%E3%81%AE%E5%8F%8D%E5%BF%9C%7C%E4%B8%96%E7%95%8C%E5%8F%B2%E5%B0%82%E9%96%80%E3%83%96%E3%83%AD%E3%82%B0-%7C%E3%83%80%E3%82%A4%E3%82%A8%E3%83%83%E3%83%88%E9%80%9F%E5%A0%B1%EF%BC%A02%E3%81%A1%E3%82%83%E3%82%93%E3%81%AD%E3%82%8B%7C%E3%81%8A%E6%96%99%E7%90%86%E9%80%9F%E5%A0%B1%7Chimaginary%E3%81%AE%E6%97%A5%E8%A8%98%7C%E6%98%A0%E7%94%BB%E3%83%8A%E3%82%BF%E3%83%AA%E3%83%BC%7C%E3%82%A2%E3%83%AB%E3%83%95%E3%82%A1%E3%83%AB%E3%83%95%E3%82%A1%E3%83%A2%E3%82%B6%E3%82%A4%E3%82%AF%7CYahoo%21%E7%9F%A5%E6%81%B5%E8%A2%8B%7C%E7%99%BA%E8%A8%80%E5%B0%8F%E7%94%BA%7CIT%E9%80%9F%E5%A0%B1%7C%E3%83%96%E3%83%AD%E3%82%B0%7Cblog%7C%E3%81%AA%E3%82%93%E3%81%AA%E3%81%AE%7C%E8%B3%AA%E5%95%8F%E3%81%82%E3%82%8B%7C%E6%97%A5%E5%88%8A%E3%82%84%E3%81%8D%E3%81%86%E9%80%9F%E5%A0%B1%7CVIPPER%E3%81%AA%E4%BF%BA%7C%E3%81%8B%E3%81%BF%E3%81%82%E3%81%B7%E9%80%9F%E5%A0%B1%7C%E4%BB%8A%E6%97%A5%E3%81%AF%E3%83%92%E3%83%88%E3%83%87%E7%A5%AD%E3%82%8A%E3%81%A0%E3%81%9E%EF%BC%81%7C%E3%81%97%E3%81%A3%E3%81%8D%E3%83%BC%E3%81%AE%E3%83%96%E3%83%AD%E3%82%B0?users=3\&date\_begin=2016-06-30\&sort=popular\&date\_end=2017-06-30\&safe=on\&target=all\&page=72](https://b.hatena.ne.jp/q/%E3%82%B5%E3%82%A4%E3%83%88%20Google%20%20%E6%89%93%E7%B7%9A%E7%B5%84%E3%82%93%E3%81%A7%E3%81%BF%E3%81%9F%7C%E6%B5%B7%E5%A4%96%E3%81%AE%E5%8F%8D%E5%BF%9C%7C%E4%B8%96%E7%95%8C%E5%8F%B2%E5%B0%82%E9%96%80%E3%83%96%E3%83%AD%E3%82%B0-%7C%E3%83%80%E3%82%A4%E3%82%A8%E3%83%83%E3%83%88%E9%80%9F%E5%A0%B1%EF%BC%A02%E3%81%A1%E3%82%83%E3%82%93%E3%81%AD%E3%82%8B%7C%E3%81%8A%E6%96%99%E7%90%86%E9%80%9F%E5%A0%B1%7Chimaginary%E3%81%AE%E6%97%A5%E8%A8%98%7C%E6%98%A0%E7%94%BB%E3%83%8A%E3%82%BF%E3%83%AA%E3%83%BC%7C%E3%82%A2%E3%83%AB%E3%83%95%E3%82%A1%E3%83%AB%E3%83%95%E3%82%A1%E3%83%A2%E3%82%B6%E3%82%A4%E3%82%AF%7CYahoo%21%E7%9F%A5%E6%81%B5%E8%A2%8B%7C%E7%99%BA%E8%A8%80%E5%B0%8F%E7%94%BA%7CIT%E9%80%9F%E5%A0%B1%7C%E3%83%96%E3%83%AD%E3%82%B0%7Cblog%7C%E3%81%AA%E3%82%93%E3%81%AA%E3%81%AE%7C%E8%B3%AA%E5%95%8F%E3%81%82%E3%82%8B%7C%E6%97%A5%E5%88%8A%E3%82%84%E3%81%8D%E3%81%86%E9%80%9F%E5%A0%B1%7CVIPPER%E3%81%AA%E4%BF%BA%7C%E3%81%8B%E3%81%BF%E3%81%82%E3%81%B7%E9%80%9F%E5%A0%B1%7C%E4%BB%8A%E6%97%A5%E3%81%AF%E3%83%92%E3%83%88%E3%83%87%E7%A5%AD%E3%82%8A%E3%81%A0%E3%81%9E%EF%BC%81%7C%E3%81%97%E3%81%A3%E3%81%8D%E3%83%BC%E3%81%AE%E3%83%96%E3%83%AD%E3%82%B0?users=3&date_begin=2016-06-30&sort=popular&date_end=2017-06-30&safe=on&target=all&page=72)  
193. Mac Fan（マックファン） 2023年4月号, 5月 24, 2025にアクセス、 [https://booklive.jp/product/index/title\_id/20000252/vol\_no/227](https://booklive.jp/product/index/title_id/20000252/vol_no/227)  
194. 初心者向け操作TIPS \- StarCraft II: Legacy of the Void 日本語Wiki, 5月 24, 2025にアクセス、 [http://www.sc2jpwiki.com/wiki/%E5%88%9D%E5%BF%83%E8%80%85%E5%90%91%E3%81%91%E6%93%8D%E4%BD%9CTIPS](http://www.sc2jpwiki.com/wiki/%E5%88%9D%E5%BF%83%E8%80%85%E5%90%91%E3%81%91%E6%93%8D%E4%BD%9CTIPS)  
195. CraftLaunch: User Manual \- craftware, 5月 24, 2025にアクセス、 [https://crftwr.github.io/clnch/doc/](https://crftwr.github.io/clnch/doc/)  
196. Craft Docs, 5月 24, 2025にアクセス、 [https://www.craft.do/](https://www.craft.do/)  
197. Explore the Craft Blog \- Craft Docs, 5月 24, 2025にアクセス、 [https://www.craft.do/blog](https://www.craft.do/blog)  
198. 「Craft－ドキュメントとメモエディタ」をApp Storeで \- Apple, 5月 24, 2025にアクセス、 [https://apps.apple.com/jp/app/craft-docs-and-notes-editor/id1487937127](https://apps.apple.com/jp/app/craft-docs-and-notes-editor/id1487937127)  
199. What's new \- Craft Docs, 5月 24, 2025にアクセス、 [https://www.craft.do/whats-new](https://www.craft.do/whats-new)  
200. 日本語入力システム「ATOK Passport」のWindows版に「ATOKハイパーハイブリッドエンジン2」を搭載し、2025年2月3日(月)より提供開始 | ジャストシステム \- JustSystems Corporation, 5月 24, 2025にアクセス、 [https://www.justsystems.com/jp/news/j20241202b.html](https://www.justsystems.com/jp/news/j20241202b.html)  
201. 【2024年】メモアプリのおすすめ15選！良いメモアプリの選び方も説明 \- Notta, 5月 24, 2025にアクセス、 [https://www.notta.ai/blog/memo-app](https://www.notta.ai/blog/memo-app)