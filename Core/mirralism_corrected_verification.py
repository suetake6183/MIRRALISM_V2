#!/usr/bin/env python3
"""
MIRRALISM Corrected Verification System
修正された客観的検証システム

CTOの指摘を受けて統計バグを完全修正
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import re


def get_accurate_file_statistics(project_root: Path) -> Dict[str, Any]:
    """正確なファイル統計取得"""
    print("📊 正確な統計計算実行中...")

    actual_files = []
    redirect_files = []
    personality_files = []

    for file_path in project_root.rglob("*"):
        if not file_path.is_file():
            continue

        relative_path = str(file_path.relative_to(project_root))

        # 隔離ディレクトリを除外
        if (
            "/.mirralism/" in relative_path
            or relative_path.startswith(".mirralism/")
            or "/.git/" in relative_path
            or relative_path.startswith(".git/")
        ):
            continue

        actual_files.append(file_path)

        # REDIRECT検索
        if re.search(r"redirect", file_path.name, re.IGNORECASE):
            redirect_files.append(file_path)

        # personality_learning検索
        if "personality_learning" in file_path.name.lower():
            personality_files.append(file_path)

    # 統計計算
    total_files = len(actual_files)
    redirect_count = len(redirect_files)
    personality_count = len(personality_files)

    redirect_ratio = (redirect_count / total_files * 100) if total_files > 0 else 0
    constraint_compliance = 100 - redirect_ratio
    personality_compliance = 100 if personality_count <= 1 else 0
    overall_compliance = (constraint_compliance + personality_compliance) / 2

    results = {
        "total_actual_files": total_files,
        "redirect_files_count": redirect_count,
        "personality_files_count": personality_count,
        "redirect_ratio_percent": redirect_ratio,
        "constraint_compliance": constraint_compliance,
        "personality_compliance": personality_compliance,
        "overall_compliance": overall_compliance,
        "redirect_file_paths": [
            str(f.relative_to(project_root)) for f in redirect_files
        ],
        "personality_file_paths": [
            str(f.relative_to(project_root)) for f in personality_files
        ],
    }

    print(f"📊 正確な統計完了:")
    print(f"  実ファイル数: {total_files}")
    print(f"  REDIRECTファイル: {redirect_count}個 ({redirect_ratio:.1f}%)")
    print(f"  personality_learning: {personality_count}個")
    print(f"  制約遵守率: {overall_compliance:.1f}%")

    return results


def perform_external_verification(project_root: Path) -> Dict[str, Any]:
    """外部コマンドによる検証"""
    print("🔍 外部コマンド検証実行中...")

    results = {}

    # find コマンド（REDIRECT）
    try:
        result = subprocess.run(
            [
                "find",
                str(project_root),
                "-name",
                "*redirect*",
                "-o",
                "-name",
                "*REDIRECT*",
                "-not",
                "-path",
                "*/.mirralism/*",
                "-not",
                "-path",
                "*/.git/*",
                "-type",
                "f",
            ],
            capture_output=True,
            text=True,
        )

        found_files = [
            line.strip() for line in result.stdout.split("\n") if line.strip()
        ]

        results["find_redirect"] = {
            "exit_code": result.returncode,
            "found_files": found_files,
            "count": len(found_files),
        }
    except Exception as e:
        results["find_redirect"] = {"error": str(e)}

    # find コマンド（personality_learning）
    try:
        result = subprocess.run(
            [
                "find",
                str(project_root),
                "-name",
                "*personality_learning*",
                "-not",
                "-path",
                "*/.mirralism/*",
                "-not",
                "-path",
                "*/.git/*",
                "-type",
                "f",
            ],
            capture_output=True,
            text=True,
        )

        found_files = [
            line.strip() for line in result.stdout.split("\n") if line.strip()
        ]

        results["find_personality"] = {
            "exit_code": result.returncode,
            "found_files": found_files,
            "count": len(found_files),
            "singleton_compliant": len(found_files) <= 1,
        }
    except Exception as e:
        results["find_personality"] = {"error": str(e)}

    print("🔍 外部コマンド検証完了")
    return results


def calculate_corrected_score(
    statistics: Dict[str, Any], external: Dict[str, Any]
) -> float:
    """修正された品質スコア算出"""
    scores = []

    # 統計ベースのスコア
    scores.append(statistics["overall_compliance"])

    # 外部検証ベースのスコア
    redirect_clean = external.get("find_redirect", {}).get("count", 1) == 0
    scores.append(100.0 if redirect_clean else 0.0)

    personality_clean = external.get("find_personality", {}).get(
        "singleton_compliant", False
    )
    scores.append(100.0 if personality_clean else 0.0)

    return sum(scores) / len(scores) if scores else 0.0


def main():
    """メイン実行"""
    print("🔍 MIRRALISM Corrected Verification System")
    print("=" * 50)
    print("CTOの指摘を受けた統計バグ修正版")
    print()

    project_root = Path(".").resolve()

    try:
        # 正確な統計計算
        statistics = get_accurate_file_statistics(project_root)

        # 外部コマンド検証
        external = perform_external_verification(project_root)

        # 修正されたスコア算出
        corrected_score = calculate_corrected_score(statistics, external)

        # 結果表示
        print("\n" + "=" * 50)
        print("🏆 修正された検証結果")
        print("=" * 50)

        print(f"修正された品質スコア: {corrected_score:.1f}%")
        print(
            f"品質レベル: {'EXCELLENT' if corrected_score >= 95.0 else 'GOOD' if corrected_score >= 80.0 else 'NEEDS_IMPROVEMENT'}"
        )

        print(f"\n📊 正確な統計:")
        print(f"  実プロジェクトファイル: {statistics['total_actual_files']}個")
        print(f"  REDIRECTファイル: {statistics['redirect_files_count']}個")
        print(f"  personality_learning: {statistics['personality_files_count']}個")
        print(f"  制約遵守率: {statistics['overall_compliance']:.1f}%")

        print(f"\n🔍 外部検証:")
        print(
            f"  find REDIRECT: {external.get('find_redirect', {}).get('count', 'エラー')}個"
        )
        print(
            f"  find personality: {external.get('find_personality', {}).get('count', 'エラー')}個"
        )

        cto_ready = corrected_score >= 95.0
        print(f"\nCTO承認準備: {'✅ 完了' if cto_ready else '❌ 要改善'}")

        if corrected_score >= 95.0:
            print("\n🎉 真の技術的完璧性達成！")
            print("✅ 統計バグ修正による正確な測定")
            print("✅ 客観的検証による信頼性確保")
            print("✅ CTOの指摘に完全準拠")
        else:
            print(f"\n⚠️ 品質スコア: {corrected_score:.1f}%")
            print("🔧 追加の改善が必要")

        # レポート保存
        report = {
            "verification_type": "corrected_objective_verification",
            "timestamp": datetime.now().isoformat(),
            "statistics": statistics,
            "external_verification": external,
            "corrected_quality_score": corrected_score,
            "cto_approval_ready": cto_ready,
            "bug_fixes": ["exclusion_pattern_correction", "accurate_file_counting"],
        }

        report_path = Path(".mirralism/verification")
        report_path.mkdir(parents=True, exist_ok=True)

        with open(
            report_path
            / f"corrected_verification_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"\n✅ 修正された検証完了")

    except Exception as e:
        print(f"\n❌ 検証エラー: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
