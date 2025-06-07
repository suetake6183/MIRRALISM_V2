#!/usr/bin/env python3
"""
MIRRALISM Date Integrity Validation System
Purpose: 日付エラーの予防的検出・修正システム
Design: 制約ファースト設計による品質保証

Created: 2025-06-07
Version: 1.0.0
"""

import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging
from dataclasses import dataclass


@dataclass
class DateValidationResult:
    """日付検証結果"""
    is_valid: bool
    file_path: str
    detected_date: Optional[str]
    system_date: str
    deviation_days: Optional[int]
    severity: str
    recommendation: str


class MIRRALISMDateValidator:
    """MIRRALISM日付整合性検証システム"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.validation_log = self.project_root / "Data" / "validation" / "date_integrity.log"
        self.validation_log.parent.mkdir(parents=True, exist_ok=True)
        
        # 日付制約設定
        self.max_future_days = 1  # 未来日付許容範囲（1日）
        self.max_past_days = 365  # 過去日付許容範囲（1年）
        
        # ログ設定
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.validation_log),
                logging.StreamHandler()
            ]
        )
        
        logging.info("🔍 MIRRALISM Date Integrity System initialized")
        
    def get_system_date(self) -> datetime:
        """正確なシステム日付取得"""
        return datetime.now(timezone(timedelta(hours=9)))  # JST
        
    def extract_dates_from_json(self, file_path: Path) -> List[str]:
        """JSONファイルから日付文字列を抽出"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # ISO 8601形式の日付パターン
            date_pattern = r'"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2})"'
            dates = re.findall(date_pattern, content)
            
            return dates
            
        except Exception as e:
            logging.error(f"Failed to extract dates from {file_path}: {e}")
            return []
            
    def validate_date_string(self, date_str: str) -> Tuple[bool, Optional[datetime]]:
        """日付文字列の妥当性検証"""
        try:
            # ISO 8601形式の解析
            parsed_date = datetime.fromisoformat(date_str)
            return True, parsed_date
        except ValueError:
            return False, None
            
    def check_date_constraints(self, parsed_date: datetime, system_date: datetime) -> Dict[str, any]:
        """日付制約チェック"""
        delta = (parsed_date - system_date).days
        
        result = {
            "deviation_days": delta,
            "is_future": delta > 0,
            "is_past": delta < 0,
            "within_future_limit": delta <= self.max_future_days,
            "within_past_limit": delta >= -self.max_past_days,
            "severity": "NORMAL"
        }
        
        # 重大度判定
        if delta > self.max_future_days:
            result["severity"] = "CRITICAL"  # 未来日付
        elif delta < -self.max_past_days:
            result["severity"] = "HIGH"      # 古すぎる日付
        elif abs(delta) > 30:
            result["severity"] = "MEDIUM"    # 1ヶ月以上の差異
        elif abs(delta) > 7:
            result["severity"] = "LOW"       # 1週間以上の差異
            
        return result
        
    def validate_file(self, file_path: Path) -> List[DateValidationResult]:
        """ファイル内の全日付を検証"""
        results = []
        system_date = self.get_system_date()
        
        dates = self.extract_dates_from_json(file_path)
        
        if not dates:
            # 日付が見つからない場合
            results.append(DateValidationResult(
                is_valid=False,
                file_path=str(file_path),
                detected_date=None,
                system_date=system_date.isoformat(),
                deviation_days=None,
                severity="WARNING",
                recommendation="No date fields found in JSON file"
            ))
            return results
            
        for date_str in dates:
            is_valid_format, parsed_date = self.validate_date_string(date_str)
            
            if not is_valid_format:
                results.append(DateValidationResult(
                    is_valid=False,
                    file_path=str(file_path),
                    detected_date=date_str,
                    system_date=system_date.isoformat(),
                    deviation_days=None,
                    severity="CRITICAL",
                    recommendation="Invalid date format detected"
                ))
                continue
                
            constraints = self.check_date_constraints(parsed_date, system_date)
            
            is_valid = (constraints["within_future_limit"] and 
                       constraints["within_past_limit"])
            
            recommendation = self._generate_recommendation(constraints)
            
            results.append(DateValidationResult(
                is_valid=is_valid,
                file_path=str(file_path),
                detected_date=date_str,
                system_date=system_date.isoformat(),
                deviation_days=constraints["deviation_days"],
                severity=constraints["severity"],
                recommendation=recommendation
            ))
            
        return results
        
    def _generate_recommendation(self, constraints: Dict) -> str:
        """推奨修正アクションの生成"""
        deviation = constraints["deviation_days"]
        severity = constraints["severity"]
        
        if severity == "CRITICAL":
            if constraints["is_future"]:
                return f"URGENT: Future date detected (+{deviation} days). Correct to current date."
            else:
                return f"URGENT: Extremely old date (-{abs(deviation)} days). Verify data integrity."
        elif severity == "HIGH":
            return f"Review date accuracy: {abs(deviation)} days deviation from current date."
        elif severity == "MEDIUM":
            return f"Consider date verification: {abs(deviation)} days deviation."
        elif severity == "LOW":
            return f"Minor date deviation: {abs(deviation)} days. Monitor for patterns."
        else:
            return "Date within acceptable range."
            
    def scan_directory(self, directory: Path, pattern: str = "*.json") -> List[DateValidationResult]:
        """ディレクトリ内の全JSONファイルをスキャン"""
        all_results = []
        
        for file_path in directory.rglob(pattern):
            if file_path.is_file():
                file_results = self.validate_file(file_path)
                all_results.extend(file_results)
                
        return all_results
        
    def generate_validation_report(self, results: List[DateValidationResult]) -> Dict:
        """検証レポート生成"""
        report = {
            "scan_timestamp": self.get_system_date().isoformat(),
            "total_files_scanned": len(set(r.file_path for r in results)),
            "total_dates_checked": len(results),
            "validation_summary": {
                "valid_dates": len([r for r in results if r.is_valid]),
                "invalid_dates": len([r for r in results if not r.is_valid]),
                "by_severity": {}
            },
            "critical_issues": [r for r in results if r.severity == "CRITICAL"],
            "high_priority_issues": [r for r in results if r.severity == "HIGH"],
            "recommendations": []
        }
        
        # 重大度別集計
        for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "NORMAL", "WARNING"]:
            count = len([r for r in results if r.severity == severity])
            report["validation_summary"]["by_severity"][severity] = count
            
        # 推奨アクション
        if report["critical_issues"]:
            report["recommendations"].append("🚨 Immediate action required for CRITICAL date errors")
        if report["high_priority_issues"]:
            report["recommendations"].append("⚠️ Review HIGH priority date inconsistencies")
            
        return report
        
    def fix_date_in_file(self, file_path: Path, old_date: str, new_date: str) -> bool:
        """ファイル内の日付を自動修正"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 日付文字列を置換
            updated_content = content.replace(f'"{old_date}"', f'"{new_date}"')
            
            if content != updated_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                    
                logging.info(f"✅ Date fixed in {file_path}: {old_date} → {new_date}")
                return True
            else:
                logging.warning(f"⚠️ No changes made to {file_path}")
                return False
                
        except Exception as e:
            logging.error(f"❌ Failed to fix date in {file_path}: {e}")
            return False
            
    def auto_fix_critical_dates(self, results: List[DateValidationResult]) -> int:
        """CRITICAL重大度の日付を自動修正"""
        fixed_count = 0
        system_date = self.get_system_date()
        
        for result in results:
            if result.severity == "CRITICAL" and result.detected_date:
                # 現在時刻に近い適切な日付を生成
                fixed_date = system_date.isoformat()
                
                if self.fix_date_in_file(Path(result.file_path), result.detected_date, fixed_date):
                    fixed_count += 1
                    
        return fixed_count


def main():
    """メイン実行"""
    validator = MIRRALISMDateValidator()
    
    # PersonalityLearningディレクトリをスキャン
    scan_directory = validator.project_root / "Core" / "PersonalityLearning"
    
    logging.info(f"🔍 Starting date validation scan: {scan_directory}")
    
    results = validator.scan_directory(scan_directory)
    
    # レポート生成
    report = validator.generate_validation_report(results)
    
    # 結果表示
    print("🔍 MIRRALISM Date Integrity Validation Report")
    print("=" * 55)
    print(f"📅 Scan Time: {report['scan_timestamp']}")
    print(f"📁 Files Scanned: {report['total_files_scanned']}")
    print(f"🔢 Dates Checked: {report['total_dates_checked']}")
    print()
    print("📊 Validation Summary:")
    print(f"  ✅ Valid Dates: {report['validation_summary']['valid_dates']}")
    print(f"  ❌ Invalid Dates: {report['validation_summary']['invalid_dates']}")
    print()
    print("🚨 Issues by Severity:")
    for severity, count in report['validation_summary']['by_severity'].items():
        if count > 0:
            icon = {"CRITICAL": "🚨", "HIGH": "⚠️", "MEDIUM": "🔶", "LOW": "🔸", "NORMAL": "✅", "WARNING": "⚡"}
            print(f"  {icon.get(severity, '📊')} {severity}: {count}")
    
    # 重要な問題の詳細表示
    if report['critical_issues']:
        print("\n🚨 Critical Issues Requiring Immediate Attention:")
        for issue in report['critical_issues']:
            print(f"  - {issue.file_path}: {issue.recommendation}")
            
    # 推奨アクション
    if report['recommendations']:
        print("\n💡 Recommendations:")
        for rec in report['recommendations']:
            print(f"  {rec}")
            
    # レポート保存
    report_path = validator.project_root / "Data" / "validation" / f"date_validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False, default=str)
        
    print(f"\n📄 Detailed report saved: {report_path}")


if __name__ == "__main__":
    main()