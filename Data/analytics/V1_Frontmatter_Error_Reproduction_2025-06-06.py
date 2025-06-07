#!/usr/bin/env python3
"""
V1 Frontmatter エラー再現・分析システム
=====================================

目的: V1で発生していたfrontmatterエラーを再現し、
     根本原因を特定してV2での予防策を策定

作成日: 2025年6月6日
"""

import json
import re
import yaml
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class V1FrontmatterErrorReproducer:
    """V1 Frontmatterエラー再現システム"""
    
    def __init__(self):
        self.error_patterns = []
        self.reproduction_results = {}
        
    def reproduce_v1_manual_yaml_parsing(self, content: str) -> Dict[str, Any]:
        """
        V1の手動YAML解析を再現
        data_review_system.py:71-81 の実装を再現
        """
        logger.info("V1手動YAML解析エラーを再現中...")
        
        metadata = {}
        errors = []
        
        try:
            # V1の実装を忠実に再現
            if content.startswith('---'):
                yaml_end = content.find('---', 3)
                if yaml_end > 0:
                    yaml_content = content[3:yaml_end]
                    for line in yaml_content.strip().split('\n'):
                        if ':' in line:
                            # V1の致命的実装: split(':', 1)のみ
                            key, value = line.split(':', 1)
                            metadata[key.strip()] = value.strip()
                        else:
                            errors.append(f"コロン欠如行: {line}")
                else:
                    errors.append("終了区切り文字(---)が見つからない")
            else:
                errors.append("開始区切り文字(---)が見つからない")
                
        except Exception as e:
            errors.append(f"解析例外: {e}")
            
        return {
            "parsed_metadata": metadata,
            "errors": errors,
            "method": "v1_manual_parsing"
        }
    
    def reproduce_v1_datetime_bugs(self, raw_datetime: str) -> Dict[str, Any]:
        """
        V1の時刻処理バグを再現
        notion_integration.py:173-232 の問題を再現
        """
        logger.info(f"V1時刻処理バグを再現中: {raw_datetime}")
        
        errors = []
        warnings = []
        
        try:
            # V1の複雑すぎる修正ロジックを再現
            if not raw_datetime:
                # 空の場合は現在時刻を使用（V1の仕様）
                now = datetime.now(timezone.utc)
                fixed_time = now.isoformat()
                warnings.append(f"空の時刻データを修正: {fixed_time}")
                return {
                    "original": raw_datetime,
                    "fixed": fixed_time,
                    "errors": errors,
                    "warnings": warnings,
                    "fix_type": "empty_to_current"
                }
            
            # V1のパターンマッチング（問題あり）
            if re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", raw_datetime):
                # 完全形式のパース試行
                try:
                    dt = datetime.fromisoformat(raw_datetime.replace("Z", "+00:00"))
                    return {
                        "original": raw_datetime,
                        "fixed": dt.isoformat(),
                        "errors": errors,
                        "warnings": warnings,
                        "fix_type": "complete_format"
                    }
                except Exception as e:
                    errors.append(f"完全形式パースエラー: {e}")
            
            # 日付のみパターン（バグの温床）
            if re.match(r"^\d{4}-\d{2}-\d{2}$", raw_datetime):
                try:
                    dt = datetime.fromisoformat(f"{raw_datetime}T00:00:00+00:00")
                    fixed_time = dt.isoformat()
                    warnings.append(f"不完全な時刻データを修正: {raw_datetime} → {fixed_time}")
                    return {
                        "original": raw_datetime,
                        "fixed": fixed_time,
                        "errors": errors,
                        "warnings": warnings,
                        "fix_type": "date_only_to_full"
                    }
                except Exception as e:
                    errors.append(f"日付のみパースエラー: {e}")
            
            # その他の失敗パターン
            errors.append(f"認識できない時刻フォーマット: {raw_datetime}")
            now = datetime.now(timezone.utc)
            fixed_time = now.isoformat()
            errors.append(f"現在時刻で代替: {fixed_time}")
            
            return {
                "original": raw_datetime,
                "fixed": fixed_time,
                "errors": errors,
                "warnings": warnings,
                "fix_type": "fallback_to_current"
            }
            
        except Exception as e:
            errors.append(f"時刻修正処理エラー: {e}")
            now = datetime.now(timezone.utc)
            return {
                "original": raw_datetime,
                "fixed": now.isoformat(),
                "errors": errors,
                "warnings": warnings,
                "fix_type": "exception_fallback"
            }
    
    def generate_problematic_frontmatter_samples(self) -> List[Dict[str, Any]]:
        """V1で問題となったfrontmatterサンプルを生成"""
        
        samples = [
            {
                "name": "Type A: YAML構文エラー",
                "content": """---
source: SuperWhisper: Fixed)
created: 2025-05-19T14:18:00
classification: 📥 Inbox Raw
quality_score: 0.80
noise_level: 0.00
notion_id: 1f8d94d4-29bc-8082-9053-d21006631eac
personality_learning_ready: False
content_source: Notionページブロック
---""",
                "expected_errors": ["不正な括弧", "絵文字によるパース失敗"]
            },
            {
                "name": "Type B: データ型不整合",
                "content": """---
source: SuperWhisper
created: "not_a_date"
classification: 📥 Inbox Raw
quality_score: "not_a_number"
noise_level: null
notion_id: 1f8d94d4-29bc-8082-9053-d21006631eac
personality_learning_ready: "not_a_boolean"
content_source: Notionページブロック
---""",
                "expected_errors": ["データ型不一致", "不正な値"]
            },
            {
                "name": "Type C: フィールド重複・欠落",
                "content": """---
source: SuperWhisper
source: SuperWhisper (duplicate)
created: 2025-05-19T14:18:00+00:00
# missing required fields
quality_score: 0.80
# noise_level missing
notion_id: 1f8d94d4-29bc-8082-9053-d21006631eac
datetime_fix_applied: True
processing_version: v2.1_datetime_fixed
content_source: Notionページブロック
extra_field: "should not be here"
---""",
                "expected_errors": ["重複フィールド", "必須フィールド欠落", "予期しないフィールド"]
            },
            {
                "name": "Type D: 複雑なYAML構造エラー",
                "content": """---
source: SuperWhisper
created: 2025-05-19T14:18:00+00:00
classification: 📥 Inbox Raw
metadata:
  - invalid: yaml: structure:
  - missing_quotes: this is a problem
  - nested:
      level: 2
      problems: [1, 2, "3"]
quality_score: 0.80
---""",
                "expected_errors": ["ネスト構造エラー", "リスト構造エラー"]
            }
        ]
        
        return samples
    
    def test_standard_yaml_parsing(self, content: str) -> Dict[str, Any]:
        """標準YAMLパーサーでの解析結果"""
        try:
            # YAML部分を抽出
            if content.startswith('---'):
                yaml_end = content.find('---', 3)
                if yaml_end > 0:
                    yaml_content = content[3:yaml_end]
                    parsed_data = yaml.safe_load(yaml_content)
                    return {
                        "parsed_data": parsed_data,
                        "success": True,
                        "method": "standard_yaml_parser"
                    }
            
            return {
                "parsed_data": None,
                "success": False,
                "error": "YAML区切り文字が見つからない",
                "method": "standard_yaml_parser"
            }
            
        except yaml.YAMLError as e:
            return {
                "parsed_data": None,
                "success": False,
                "error": f"YAML解析エラー: {e}",
                "method": "standard_yaml_parser"
            }
        except Exception as e:
            return {
                "parsed_data": None,
                "success": False,
                "error": f"一般エラー: {e}",
                "method": "standard_yaml_parser"
            }
    
    def run_comprehensive_error_reproduction(self) -> Dict[str, Any]:
        """包括的エラー再現テスト"""
        logger.info("V1 frontmatterエラー包括的再現テスト開始")
        
        samples = self.generate_problematic_frontmatter_samples()
        results = {
            "test_timestamp": datetime.now().isoformat(),
            "sample_count": len(samples),
            "results": [],
            "summary": {
                "v1_manual_parsing_failures": 0,
                "standard_yaml_parsing_failures": 0,
                "datetime_processing_issues": 0
            }
        }
        
        for sample in samples:
            logger.info(f"テスト実行: {sample['name']}")
            
            # V1手動解析テスト
            v1_result = self.reproduce_v1_manual_yaml_parsing(sample['content'])
            
            # 標準YAML解析テスト
            standard_result = self.test_standard_yaml_parsing(sample['content'])
            
            # 時刻処理テスト（作成日時がある場合）
            datetime_results = []
            if v1_result['parsed_metadata'].get('created'):
                datetime_test = self.reproduce_v1_datetime_bugs(
                    v1_result['parsed_metadata']['created']
                )
                datetime_results.append(datetime_test)
            
            # 結果記録
            test_result = {
                "sample_name": sample['name'],
                "sample_content": sample['content'],
                "expected_errors": sample['expected_errors'],
                "v1_manual_parsing": v1_result,
                "standard_yaml_parsing": standard_result,
                "datetime_processing": datetime_results,
                "comparison": {
                    "v1_had_errors": len(v1_result['errors']) > 0,
                    "standard_had_errors": not standard_result['success'],
                    "v1_vs_standard": "V1のみエラー" if len(v1_result['errors']) > 0 and standard_result['success'] else
                                     "両方エラー" if len(v1_result['errors']) > 0 and not standard_result['success'] else
                                     "両方成功" if len(v1_result['errors']) == 0 and standard_result['success'] else
                                     "標準のみエラー"
                }
            }
            
            results['results'].append(test_result)
            
            # サマリー更新
            if len(v1_result['errors']) > 0:
                results['summary']['v1_manual_parsing_failures'] += 1
            if not standard_result['success']:
                results['summary']['standard_yaml_parsing_failures'] += 1
            if any(len(dt_result['errors']) > 0 for dt_result in datetime_results):
                results['summary']['datetime_processing_issues'] += 1
        
        # 特別な時刻処理テスト
        datetime_test_cases = [
            "",  # 空文字
            "2025-05-19",  # 日付のみ
            "2025-05-19T14:18:00",  # タイムゾーンなし
            "2025-05-19T14:18:00Z",  # UTC
            "2025-05-19T14:18:00+09:00",  # JST
            "invalid-date",  # 不正フォーマット
            "2025-13-45T25:70:70",  # 存在しない日時
        ]
        
        datetime_test_results = []
        for test_case in datetime_test_cases:
            dt_result = self.reproduce_v1_datetime_bugs(test_case)
            datetime_test_results.append(dt_result)
            if len(dt_result['errors']) > 0:
                results['summary']['datetime_processing_issues'] += 1
        
        results['datetime_edge_cases'] = datetime_test_results
        
        # エラー率計算
        total_tests = len(samples)
        results['summary']['error_rates'] = {
            "v1_manual_parsing_error_rate": results['summary']['v1_manual_parsing_failures'] / total_tests,
            "standard_yaml_parsing_error_rate": results['summary']['standard_yaml_parsing_failures'] / total_tests,
            "improvement_potential": (results['summary']['v1_manual_parsing_failures'] - results['summary']['standard_yaml_parsing_failures']) / total_tests
        }
        
        logger.info("エラー再現テスト完了")
        return results
    
    def generate_v2_prevention_recommendations(self, test_results: Dict[str, Any]) -> List[str]:
        """V2での予防策推奨事項生成"""
        
        recommendations = []
        
        # YAML解析改善
        v1_errors = test_results['summary']['v1_manual_parsing_failures']
        standard_errors = test_results['summary']['standard_yaml_parsing_failures']
        
        if v1_errors > standard_errors:
            recommendations.append(
                f"標準YAMLパーサー採用により{v1_errors - standard_errors}件のエラーを予防可能"
            )
        
        # 時刻処理改善
        datetime_issues = test_results['summary']['datetime_processing_issues']
        if datetime_issues > 0:
            recommendations.append(
                f"ISO 8601強制実装により{datetime_issues}件の時刻エラーを予防"
            )
        
        # 具体的技術推奨
        recommendations.extend([
            "PyYAML/ruamel.yaml等の検証済みライブラリ使用",
            "Frontmatter schema定義とバリデーション実装",
            "datetime処理の統一モジュール化",
            "エラーハンドリングの段階的実装",
            "ユニットテストによる回帰テスト確保"
        ])
        
        return recommendations


def main():
    """エラー再現テスト実行"""
    reproducer = V1FrontmatterErrorReproducer()
    
    # 包括的テスト実行
    results = reproducer.run_comprehensive_error_reproduction()
    
    # 結果保存
    output_path = Path("Data/analytics/v1_frontmatter_error_reproduction_results.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    
    # 推奨事項生成
    recommendations = reproducer.generate_v2_prevention_recommendations(results)
    
    # レポート出力
    print("=" * 60)
    print("V1 Frontmatterエラー再現テスト結果")
    print("=" * 60)
    print(f"テストサンプル数: {results['sample_count']}")
    print(f"V1手動解析エラー: {results['summary']['v1_manual_parsing_failures']}")
    print(f"標準YAML解析エラー: {results['summary']['standard_yaml_parsing_failures']}")
    print(f"時刻処理問題: {results['summary']['datetime_processing_issues']}")
    print()
    print("エラー率:")
    for key, rate in results['summary']['error_rates'].items():
        print(f"  {key}: {rate:.1%}")
    print()
    print("V2予防策推奨事項:")
    for i, rec in enumerate(recommendations, 1):
        print(f"  {i}. {rec}")
    print()
    print(f"詳細結果: {output_path}")


if __name__ == "__main__":
    main()