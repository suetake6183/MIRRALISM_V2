#!/usr/bin/env python3
"""
基本機能テスト
============

MIRRALISM V2の基本機能をテストするCI/CD用テスト
"""

import pytest
import sys
from pathlib import Path

# プロジェクトルート追加
sys.path.append(str(Path(__file__).parent.parent.parent))


class TestBasicFunctionality:
    """基本機能テスト"""
    
    def test_python_version(self):
        """Python バージョンテスト"""
        assert sys.version_info >= (3, 9), "Python 3.9以上が必要"
    
    def test_core_imports(self):
        """コアモジュールインポートテスト"""
        try:
            # 基本ライブラリ
            import numpy
            import pandas
            import requests
            assert True
        except ImportError as e:
            pytest.fail(f"基本ライブラリインポート失敗: {e}")
    
    def test_project_structure(self):
        """プロジェクト構造テスト"""
        project_root = Path(__file__).parent.parent.parent
        
        required_dirs = [
            "Core",
            "scripts", 
            "tests",
            "Documentation"
        ]
        
        for dir_name in required_dirs:
            dir_path = project_root / dir_name
            assert dir_path.exists(), f"必須ディレクトリが不存在: {dir_name}"
    
    def test_requirements_file(self):
        """requirements.txt存在テスト"""
        project_root = Path(__file__).parent.parent.parent
        requirements_file = project_root / "requirements.txt"
        assert requirements_file.exists(), "requirements.txt が不存在"
        
        # 内容確認
        content = requirements_file.read_text()
        assert "pytest" in content, "pytest が requirements.txt に不存在"
        assert "black" in content, "black が requirements.txt に不存在"
    
    def test_mirralism_constraint_system(self):
        """MIRRALISM制約システムテスト"""
        # 基本的な制約チェック
        project_root = Path(__file__).parent.parent.parent
        
        # ファイル数制限チェック (500ファイル以下)
        total_files = sum(1 for _ in project_root.rglob("*.py"))
        assert total_files < 500, f"Pythonファイル数が制限超過: {total_files}"
        
        # REDIRECTファイル禁止チェック（隔離済みファイルは除外）
        redirect_files = [f for f in project_root.rglob("*REDIRECT*") 
                         if ".mirralism/quarantine" not in str(f)]
        assert len(redirect_files) == 0, f"REDIRECTファイル検出: {redirect_files}"


class TestFileOrganizer:
    """ファイル整理システムテスト"""
    
    def test_organizer_config_exists(self):
        """整理設定ファイル存在テスト"""
        project_root = Path(__file__).parent.parent.parent
        config_file = project_root / "scripts" / "organizer_config.json"
        assert config_file.exists(), "organizer_config.json が不存在"
    
    def test_organizer_script_exists(self):
        """整理スクリプト存在テスト"""
        project_root = Path(__file__).parent.parent.parent
        script_file = project_root / "scripts" / "file_organizer.py"
        assert script_file.exists(), "file_organizer.py が不存在"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])