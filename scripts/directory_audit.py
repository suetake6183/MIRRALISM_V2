#!/usr/bin/env python3
"""
MIRRALISM ディレクトリ構造監査スクリプト
=====================================

設計書で指定されているディレクトリと実際の構造を比較し、
不足・過剰・マイグレーション時の問題を特定
"""

import os


def audit_directories():
    """ディレクトリ構造監査実行"""

    # 設計書で指定されている完全ディレクトリ構造
    design_dirs = {
        # Core System
        "Core/PersonalityLearning/",
        "Core/Classification/",
        "Core/Search/",
        "Core/Learning/",
        "Core/intake/",
        # Prototype Environment
        "Prototype/experiments/",
        "Prototype/testing/",
        "Prototype/development/",
        # API Integration
        "API/exports/",
        "API/integrations/",
        "API/integrations/superwhisper/",
        "API/webhooks/",
        # Documentation
        "Documentation/decisions/",
        "Documentation/guides/",
        "Documentation/migration/",
        "Documentation/reports/",
        "Documentation/strategy/",
        "Documentation/technical/",
        # Interface
        "Interface/components/",
        "Interface/dashboards/",
        "Interface/workflows/",
        # Data Management
        "Data/analytics/",
        "Data/imports/",
        "Data/migrated/",
        "Data/raw/",
        "Data/sync_config/",
        "Data/temp/",
        # Client Management
        "Clients/Database/",
        "Clients/Outputs/",
        "Clients/Templates/",
        "Clients/History/",
        "Clients/ProjectCycle/",
        # Content Creation
        "Contents/Archives/",
        "Contents/Patterns/",
        "Contents/Insights/",
        "Contents/Templates/",
        # Scripts
        "scripts/",
    }

    # 実際に存在するディレクトリを取得
    actual_dirs = set()
    for root, dirs, files in os.walk("."):
        for d in dirs:
            if not d.startswith("."):
                path = os.path.join(root, d)[2:] + "/"
                actual_dirs.add(path)

    # 比較分析
    missing = design_dirs - actual_dirs
    existing = design_dirs & actual_dirs
    extra = actual_dirs - design_dirs

    # 結果出力
    print("🔍 MIRRALISM ディレクトリ構造監査結果")
    print("=" * 50)

    print(f"\n📊 統計情報:")
    print(f"   設計書指定ディレクトリ: {len(design_dirs)}個")
    print(f"   実際存在ディレクトリ: {len(actual_dirs)}個")
    print(f"   設計通り存在: {len(existing)}個")
    print(f"   不足ディレクトリ: {len(missing)}個")
    print(f"   設計外ディレクトリ: {len(extra)}個")
    print(f"   設計整合率: {len(existing)/len(design_dirs)*100:.1f}%")

    if missing:
        print(f"\n❌ 不足ディレクトリ（{len(missing)}個）:")
        for d in sorted(missing):
            print(f"   - {d}")

    if extra:
        print(f"\n⚠️ 設計外ディレクトリ（{len(extra)}個）:")
        for d in sorted(extra):
            print(f"   - {d}")

    # マイグレーション時のリスク評価
    print(f"\n🚨 マイグレーション時のリスク評価:")

    critical_missing = []
    important_missing = []

    for d in missing:
        if any(
            keyword in d
            for keyword in [
                "PersonalityLearning",
                "integrations",
                "Database",
                "Archives",
            ]
        ):
            critical_missing.append(d)
        else:
            important_missing.append(d)

    if critical_missing:
        print(f"   🔴 重大リスク（{len(critical_missing)}個）: コア機能・データ格納不能")
        for d in critical_missing:
            print(f"      - {d}")

    if important_missing:
        print(f"   🟡 中程度リスク（{len(important_missing)}個）: 機能配置不明確")
        for d in important_missing:
            print(f"      - {d}")

    # 修正スクリプト生成
    if missing:
        print(f"\n🔧 修正用コマンド:")
        print("   mkdir -p \\")
        for i, d in enumerate(sorted(missing)):
            prefix = "     " if i > 0 else "     "
            suffix = " \\" if i < len(missing) - 1 else ""
            print(f"{prefix}{d.rstrip('/')}{suffix}")

    return {
        "total_design": len(design_dirs),
        "total_actual": len(actual_dirs),
        "missing_count": len(missing),
        "integrity_rate": len(existing) / len(design_dirs) * 100,
        "missing_dirs": missing,
        "critical_missing": critical_missing,
    }


if __name__ == "__main__":
    audit_directories()
