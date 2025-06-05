#!/usr/bin/env python3
"""
MIRRALISM V2 統合マイグレーションインストーラー
============================================

完全な環境移行とセットアップを自動化するインストーラー
- 段階的マイグレーション実行
- バックアップ・ロールバック機能
- 依存関係チェック・インストール
- 品質保証・検証システム
"""

import datetime
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# プロジェクトルートディレクトリ
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT / "scripts"))

try:
    from auto_migrate_organizer import MigrationOrganizer
    from file_organizer import FlexibleFileOrganizer
except ImportError:
    print("⚠️ 依存モジュールが見つかりません。セットアップを続行します...")


class MirralismMigrationInstaller:
    """MIRRALISM統合マイグレーションインストーラー"""

    def __init__(self, project_root: Optional[Path] = None):
        self.root_dir = project_root or PROJECT_ROOT
        self.backup_dir = self.root_dir / ".mirralism" / "backups"
        self.config_dir = self.root_dir / ".mirralism"
        self.log_file = self.config_dir / "migration_install.log"
        
        # ログディレクトリ作成
        self.config_dir.mkdir(exist_ok=True)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # 設定読み込み
        self.config = self._load_config()
        
        # インストール状態
        self.installation_state = {
            "phase": "none",
            "timestamp": None,
            "backup_id": None,
            "completed_steps": []
        }

    def _load_config(self) -> Dict:
        """設定ファイル読み込み"""
        config_file = self.config_dir / "migration_config.json"
        default_config = {
            "version": "2.0.0",
            "features": {
                "personality_learning": True,
                "client_intelligence": True,
                "strategic_manager": True,
                "quality_assurance": True
            },
            "dependencies": {
                "python": ">=3.9",
                "node": ">=18.0.0",
                "git": ">=2.30"
            },
            "migration_phases": [
                "backup",
                "dependency_check",
                "file_organization",
                "core_migration",
                "configuration",
                "validation",
                "cleanup"
            ]
        }
        
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self._log(f"設定読み込みエラー: {e}", "warning")
                
        return default_config

    def _log(self, message: str, level: str = "info") -> None:
        """ログ記録"""
        timestamp = datetime.datetime.now().isoformat()
        log_entry = f"[{timestamp}] {level.upper()}: {message}"
        
        print(f"{'🔧' if level == 'info' else '⚠️' if level == 'warning' else '❌'} {message}")
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + "\n")

    def create_backup(self) -> str:
        """完全バックアップ作成"""
        backup_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f"pre_migration_{backup_id}"
        
        self._log(f"バックアップ作成開始: {backup_id}")
        
        # 重要ディレクトリのバックアップ
        critical_dirs = [
            "Core/PersonalityLearning",
            "Data",
            "Clients",
            "Documentation",
            "scripts"
        ]
        
        backup_path.mkdir(parents=True, exist_ok=True)
        
        for dir_name in critical_dirs:
            source_dir = self.root_dir / dir_name
            if source_dir.exists():
                dest_dir = backup_path / dir_name
                try:
                    shutil.copytree(source_dir, dest_dir, dirs_exist_ok=True)
                    self._log(f"バックアップ完了: {dir_name}")
                except Exception as e:
                    self._log(f"バックアップエラー {dir_name}: {e}", "error")
        
        # 設定ファイルのバックアップ
        config_files = [
            ".gitignore",
            "CLAUDE.md",
            "README.md",
            "requirements.txt",
            "package.json"
        ]
        
        for file_name in config_files:
            source_file = self.root_dir / file_name
            if source_file.exists():
                try:
                    shutil.copy2(source_file, backup_path / file_name)
                    self._log(f"設定ファイルバックアップ: {file_name}")
                except Exception as e:
                    self._log(f"設定ファイルバックアップエラー {file_name}: {e}", "error")
        
        self._log(f"バックアップ完了: {backup_path}")
        return backup_id

    def check_dependencies(self) -> bool:
        """依存関係チェック"""
        self._log("依存関係チェック開始")
        
        checks = []
        
        # Python バージョンチェック
        try:
            python_version = sys.version_info
            if python_version >= (3, 9):
                checks.append(("Python", True, f"{python_version.major}.{python_version.minor}"))
            else:
                checks.append(("Python", False, f"要求: >=3.9, 現在: {python_version.major}.{python_version.minor}"))
        except Exception as e:
            checks.append(("Python", False, str(e)))
        
        # Node.js チェック
        try:
            result = subprocess.run(['node', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                checks.append(("Node.js", True, result.stdout.strip()))
            else:
                checks.append(("Node.js", False, "node コマンドが見つかりません"))
        except Exception:
            checks.append(("Node.js", False, "node コマンドが見つかりません"))
        
        # Git チェック
        try:
            result = subprocess.run(['git', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                checks.append(("Git", True, result.stdout.strip()))
            else:
                checks.append(("Git", False, "git コマンドが見つかりません"))
        except Exception:
            checks.append(("Git", False, "git コマンドが見つかりません"))
        
        # 結果表示
        all_passed = True
        for name, passed, info in checks:
            status = "✅" if passed else "❌"
            self._log(f"{status} {name}: {info}")
            if not passed:
                all_passed = False
        
        return all_passed

    def organize_files(self) -> bool:
        """ファイル整理実行"""
        self._log("ファイル整理開始")
        
        try:
            # 既存のマイグレーション整理ツールを使用
            organizer = MigrationOrganizer()
            results = organizer.pre_migration_cleanup()
            
            self._log(f"ファイル整理完了: {results['moved']}ファイル移動")
            return results['errors'] == 0
            
        except Exception as e:
            self._log(f"ファイル整理エラー: {e}", "error")
            return False

    def migrate_core_systems(self) -> bool:
        """コアシステム移行"""
        self._log("コアシステム移行開始")
        
        migration_tasks = [
            self._migrate_personality_learning,
            self._migrate_client_intelligence,
            self._migrate_configuration_files,
            self._setup_directory_structure
        ]
        
        for task in migration_tasks:
            try:
                if not task():
                    return False
            except Exception as e:
                self._log(f"移行タスクエラー {task.__name__}: {e}", "error")
                return False
        
        return True

    def _migrate_personality_learning(self) -> bool:
        """PersonalityLearning システム移行"""
        self._log("PersonalityLearning 移行中...")
        
        # データベースファイルの統合確認
        db_file = self.root_dir / "Core" / "PersonalityLearning" / "MIRRALISM_UNIFIED.db"
        if db_file.exists():
            self._log("MIRRALISM_UNIFIED.db 確認済み")
        else:
            self._log("MIRRALISM_UNIFIED.db が見つかりません", "warning")
        
        # Pythonスクリプトの確認
        scripts = [
            "unified_system.py",
            "database.py",
            "mirralism_personality_engine_basic.py"
        ]
        
        scripts_dir = self.root_dir / "Core" / "PersonalityLearning"
        for script in scripts:
            script_path = scripts_dir / script
            if script_path.exists():
                self._log(f"スクリプト確認済み: {script}")
            else:
                self._log(f"スクリプトが見つかりません: {script}", "warning")
        
        return True

    def _migrate_client_intelligence(self) -> bool:
        """Client Intelligence システム移行"""
        self._log("Client Intelligence 移行中...")
        
        # Clientsディレクトリ構造確認
        clients_dir = self.root_dir / "Clients"
        required_subdirs = [
            "Analysis", "Database", "Execution", 
            "Outputs", "Profiles", "Systems"
        ]
        
        for subdir in required_subdirs:
            subdir_path = clients_dir / subdir
            if subdir_path.exists():
                self._log(f"Clientsサブディレクトリ確認済み: {subdir}")
            else:
                subdir_path.mkdir(parents=True, exist_ok=True)
                self._log(f"Clientsサブディレクトリ作成: {subdir}")
        
        return True

    def _migrate_configuration_files(self) -> bool:
        """設定ファイル移行"""
        self._log("設定ファイル移行中...")
        
        # .mirralismディレクトリの確認・作成
        if not self.config_dir.exists():
            self.config_dir.mkdir(parents=True, exist_ok=True)
            self._log(".mirralismディレクトリ作成完了")
        
        # 設定ファイルの作成
        config_file = self.config_dir / "migration_config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
        
        return True

    def _setup_directory_structure(self) -> bool:
        """ディレクトリ構造セットアップ"""
        self._log("ディレクトリ構造セットアップ中...")
        
        required_dirs = [
            ".mirralism/reports",
            ".mirralism/cache",
            ".mirralism/logs",
            "Data/temp",
            "Data/sync_config",
            "Interface/components",
            "Interface/dashboards",
            "API/exports",
            "API/webhooks"
        ]
        
        for dir_path in required_dirs:
            full_path = self.root_dir / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
            self._log(f"ディレクトリ作成: {dir_path}")
        
        return True

    def validate_installation(self) -> bool:
        """インストール検証"""
        self._log("インストール検証開始")
        
        validation_checks = [
            self._validate_file_structure,
            self._validate_dependencies,
            self._validate_configurations,
            self._validate_core_systems
        ]
        
        all_passed = True
        for check in validation_checks:
            try:
                if not check():
                    all_passed = False
            except Exception as e:
                self._log(f"検証エラー {check.__name__}: {e}", "error")
                all_passed = False
        
        return all_passed

    def _validate_file_structure(self) -> bool:
        """ファイル構造検証"""
        self._log("ファイル構造検証中...")
        
        critical_paths = [
            "Core/PersonalityLearning",
            "Clients",
            "Documentation",
            "scripts",
            ".mirralism"
        ]
        
        for path in critical_paths:
            full_path = self.root_dir / path
            if not full_path.exists():
                self._log(f"重要パスが見つかりません: {path}", "error")
                return False
        
        self._log("ファイル構造検証完了")
        return True

    def _validate_dependencies(self) -> bool:
        """依存関係検証"""
        return self.check_dependencies()

    def _validate_configurations(self) -> bool:
        """設定検証"""
        self._log("設定検証中...")
        
        # CLAUDE.md の存在確認
        claude_md = self.root_dir / "CLAUDE.md"
        if not claude_md.exists():
            self._log("CLAUDE.md が見つかりません", "error")
            return False
        
        # package.json の存在確認
        package_json = self.root_dir / "package.json"
        if package_json.exists():
            self._log("package.json 確認済み")
        
        return True

    def _validate_core_systems(self) -> bool:
        """コアシステム検証"""
        self._log("コアシステム検証中...")
        
        # PersonalityLearning システム検証
        personality_dir = self.root_dir / "Core" / "PersonalityLearning"
        if not (personality_dir / "unified_system.py").exists():
            self._log("unified_system.py が見つかりません", "error")
            return False
        
        self._log("コアシステム検証完了")
        return True

    def rollback(self, backup_id: str) -> bool:
        """ロールバック実行"""
        backup_path = self.backup_dir / f"pre_migration_{backup_id}"
        
        if not backup_path.exists():
            self._log(f"バックアップが見つかりません: {backup_id}", "error")
            return False
        
        self._log(f"ロールバック開始: {backup_id}")
        
        try:
            # バックアップから復元
            for item in backup_path.iterdir():
                dest_path = self.root_dir / item.name
                if item.is_dir():
                    if dest_path.exists():
                        shutil.rmtree(dest_path)
                    shutil.copytree(item, dest_path)
                else:
                    shutil.copy2(item, dest_path)
                
                self._log(f"復元完了: {item.name}")
            
            self._log("ロールバック完了")
            return True
            
        except Exception as e:
            self._log(f"ロールバックエラー: {e}", "error")
            return False

    def run_full_migration(self) -> bool:
        """完全マイグレーション実行"""
        self._log("MIRRALISM V2 完全マイグレーション開始")
        
        # フェーズごとの実行
        phases = [
            ("backup", lambda: self.create_backup()),
            ("dependency_check", lambda: self.check_dependencies()),
            ("file_organization", lambda: self.organize_files()),
            ("core_migration", lambda: self.migrate_core_systems()),
            ("validation", lambda: self.validate_installation())
        ]
        
        backup_id = None
        
        for phase_name, phase_func in phases:
            self._log(f"フェーズ開始: {phase_name}")
            self.installation_state["phase"] = phase_name
            
            try:
                if phase_name == "backup":
                    backup_id = phase_func()
                    self.installation_state["backup_id"] = backup_id
                    success = backup_id is not None
                else:
                    success = phase_func()
                
                if success:
                    self.installation_state["completed_steps"].append(phase_name)
                    self._log(f"フェーズ完了: {phase_name}")
                else:
                    self._log(f"フェーズ失敗: {phase_name}", "error")
                    if backup_id:
                        self._log("ロールバックを実行しますか？")
                    return False
                    
            except Exception as e:
                self._log(f"フェーズエラー {phase_name}: {e}", "error")
                return False
        
        self._log("🎉 MIRRALISM V2 マイグレーション完全成功！")
        self.installation_state["phase"] = "completed"
        self.installation_state["timestamp"] = datetime.datetime.now().isoformat()
        
        return True

    def get_status(self) -> Dict:
        """インストール状態取得"""
        return {
            "installation_state": self.installation_state,
            "config": self.config,
            "log_file": str(self.log_file),
            "project_root": str(self.root_dir)
        }


def main():
    """メインエントリーポイント"""
    import argparse
    
    parser = argparse.ArgumentParser(description="MIRRALISM V2 Migration Installer")
    parser.add_argument("command", choices=[
        "full", "backup", "check", "migrate", "validate", 
        "rollback", "status", "organize"
    ], help="実行するコマンド")
    parser.add_argument("--backup-id", help="ロールバック用バックアップID")
    parser.add_argument("--project-root", help="プロジェクトルートディレクトリ")
    
    args = parser.parse_args()
    
    # インストーラー初期化
    project_root = Path(args.project_root) if args.project_root else None
    installer = MirralismMigrationInstaller(project_root)
    
    print("🚀 MIRRALISM V2 Migration Installer")
    print("=" * 50)
    
    # コマンド実行
    success = False
    
    try:
        if args.command == "full":
            success = installer.run_full_migration()
        elif args.command == "backup":
            backup_id = installer.create_backup()
            success = backup_id is not None
            if success:
                print(f"バックアップID: {backup_id}")
        elif args.command == "check":
            success = installer.check_dependencies()
        elif args.command == "migrate":
            success = installer.migrate_core_systems()
        elif args.command == "validate":
            success = installer.validate_installation()
        elif args.command == "rollback":
            if not args.backup_id:
                print("❌ --backup-id が必要です")
                return
            success = installer.rollback(args.backup_id)
        elif args.command == "status":
            status = installer.get_status()
            print(json.dumps(status, indent=2, ensure_ascii=False))
            success = True
        elif args.command == "organize":
            success = installer.organize_files()
        
    except KeyboardInterrupt:
        print("\n⚠️ ユーザーによって中断されました")
        return
    except Exception as e:
        installer._log(f"予期しないエラー: {e}", "error")
        success = False
    
    # 結果表示
    if success:
        print("\n✅ 操作が正常に完了しました")
    else:
        print("\n❌ 操作が失敗しました")
        print(f"詳細ログ: {installer.log_file}")


if __name__ == "__main__":
    main()