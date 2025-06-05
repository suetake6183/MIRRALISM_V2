#!/usr/bin/env python3
"""
MIRRALISM V2 高度依存関係分析システム
循環依存・深層的依存関係問題の徹底検出

作成日: 2025年6月5日
目的: より厳密な依存関係整合性チェック
"""

import os
import ast
import sys
import json
import logging
import networkx as nx  # グラフ分析用
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Set, Tuple, Optional
from collections import defaultdict, deque
import re


class AdvancedDependencyAnalyzer:
    """高度依存関係分析システム"""

    def __init__(self, project_root: str = None):
        if project_root:
            self.project_root = Path(project_root)
        else:
            current_path = Path(__file__).resolve()
            self.project_root = current_path.parent.parent.parent

        self.logger = self._setup_logging()
        self.dependency_graph = nx.DiGraph()
        self.import_patterns = []

        self.logger.info(f"🔬 高度依存関係分析システム初期化完了 - プロジェクトルート: {self.project_root}")

    def _setup_logging(self) -> logging.Logger:
        """ログ設定"""
        logger = logging.getLogger("AdvancedDependencyAnalyzer")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def deep_import_analysis(self) -> Dict[str, Any]:
        """深層import分析"""
        self.logger.info("🔬 深層import分析開始...")

        analysis_results = {
            "python_files_analyzed": 0,
            "import_statements": [],
            "potential_issues": [],
            "dependency_graph_stats": {},
            "circular_dependencies": [],
            "unused_imports": [],
            "missing_dependencies": [],
        }

        # Python ファイルの収集
        python_files = list(self.project_root.rglob("*.py"))
        excluded_patterns = [
            ".git",
            "__pycache__",
            ".pytest_cache",
            ".mypy_cache",
            ".mirralism/backups",
        ]
        python_files = [
            f
            for f in python_files
            if not any(pattern in str(f) for pattern in excluded_patterns)
        ]

        self.logger.info(f"📊 分析対象: {len(python_files)} Python ファイル")

        for py_file in python_files:
            try:
                analysis_results["python_files_analyzed"] += 1
                file_imports = self._analyze_file_imports(py_file)
                analysis_results["import_statements"].extend(file_imports)

                # 依存関係グラフ構築
                self._build_dependency_graph(py_file, file_imports)

            except Exception as e:
                self.logger.error(f"❌ ファイル分析エラー: {py_file} - {e}")

        # 循環依存検出
        analysis_results[
            "circular_dependencies"
        ] = self._detect_circular_dependencies_advanced()

        # 未使用import検出
        analysis_results["unused_imports"] = self._detect_unused_imports()

        # 依存関係グラフ統計
        analysis_results["dependency_graph_stats"] = {
            "total_nodes": self.dependency_graph.number_of_nodes(),
            "total_edges": self.dependency_graph.number_of_edges(),
            "strongly_connected_components": len(
                list(nx.strongly_connected_components(self.dependency_graph))
            ),
            "longest_path": self._find_longest_dependency_path(),
        }

        self.logger.info(f"🔬 深層分析完了")
        return analysis_results

    def _analyze_file_imports(self, file_path: Path) -> List[Dict[str, Any]]:
        """ファイルのimport文を詳細分析"""
        imports = []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # AST解析
            tree = ast.parse(content)

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(
                            {
                                "file": str(file_path.relative_to(self.project_root)),
                                "line": node.lineno,
                                "type": "import",
                                "module": alias.name,
                                "alias": alias.asname,
                                "level": 0,
                                "is_local": self._is_local_module(alias.name),
                                "raw_code": f"import {alias.name}",
                            }
                        )

                elif isinstance(node, ast.ImportFrom):
                    module_name = node.module or ""
                    for alias in node.names:
                        imports.append(
                            {
                                "file": str(file_path.relative_to(self.project_root)),
                                "line": node.lineno,
                                "type": "from_import",
                                "module": module_name,
                                "name": alias.name,
                                "alias": alias.asname,
                                "level": node.level,
                                "is_local": self._is_local_module(module_name),
                                "raw_code": f"from {module_name} import {alias.name}",
                            }
                        )

        except SyntaxError as e:
            self.logger.warning(f"⚠️ 構文エラー: {file_path}:{e.lineno} - {e.msg}")
        except Exception as e:
            self.logger.error(f"❌ import分析エラー: {file_path} - {e}")

        return imports

    def _is_local_module(self, module_name: str) -> bool:
        """ローカルモジュールかどうかの判定"""
        if not module_name:
            return False

        # 標準ライブラリ・外部パッケージの除外
        external_packages = {
            "numpy",
            "pandas",
            "sklearn",
            "requests",
            "json",
            "os",
            "sys",
            "datetime",
            "pathlib",
            "typing",
            "collections",
            "itertools",
            "sqlite3",
            "logging",
            "subprocess",
            "hashlib",
            "shutil",
            "openai",
            "anthropic",
            "sqlalchemy",
            "httpx",
            "pyyaml",
            "python-dotenv",
            "black",
            "flake8",
            "isort",
            "mypy",
            "bandit",
            "pre-commit",
            "pytest",
            "cryptography",
            "rich",
            "colorama",
            "tqdm",
            "click",
            "python-dateutil",
            "joblib",
        }

        base_module = module_name.split(".")[0]

        # プロジェクト内モジュールの判定
        project_modules = {
            "Core",
            "API",
            "Prototype",
            "Interface",
            "Data",
            "MyBrain",
            "scripts",
        }

        return (
            base_module in project_modules
            or base_module not in external_packages
            and not base_module.startswith("_")
        )

    def _build_dependency_graph(self, file_path: Path, imports: List[Dict[str, Any]]):
        """依存関係グラフの構築"""
        file_node = str(file_path.relative_to(self.project_root))

        if not self.dependency_graph.has_node(file_node):
            self.dependency_graph.add_node(file_node)

        for imp in imports:
            if imp["is_local"]:
                # ローカルモジュールの場合、対応するファイルを探す
                target_files = self._resolve_module_to_files(imp["module"])

                for target_file in target_files:
                    if target_file != file_node:  # 自己参照除外
                        self.dependency_graph.add_edge(
                            file_node, target_file, import_info=imp
                        )

    def _resolve_module_to_files(self, module_name: str) -> List[str]:
        """モジュール名からファイルパスへの解決"""
        files = []

        # ドット記法をファイルパスに変換
        path_parts = module_name.split(".")

        # 可能なファイルパスを生成
        potential_paths = [
            "/".join(path_parts) + ".py",
            "/".join(path_parts) + "/__init__.py",
        ]

        for potential_path in potential_paths:
            full_path = self.project_root / potential_path
            if full_path.exists():
                files.append(str(Path(potential_path)))

        return files

    def _detect_circular_dependencies_advanced(self) -> List[Dict[str, Any]]:
        """高度な循環依存検出"""
        circular_deps = []

        try:
            # 強連結成分の検出
            strongly_connected = list(
                nx.strongly_connected_components(self.dependency_graph)
            )

            for component in strongly_connected:
                if len(component) > 1:  # 複数ノードの循環
                    # 最短循環パスを見つける
                    component_list = list(component)
                    subgraph = self.dependency_graph.subgraph(component)

                    # 循環の詳細分析
                    try:
                        cycle = nx.find_cycle(subgraph)
                        cycle_info = {
                            "type": "circular_dependency",
                            "files_involved": component_list,
                            "cycle_length": len(cycle),
                            "cycle_path": [edge[0] for edge in cycle] + [cycle[-1][1]],
                            "severity": "high" if len(component) > 3 else "medium",
                            "description": f"循環依存検出: {len(component)}ファイル間",
                        }
                        circular_deps.append(cycle_info)

                    except nx.NetworkXNoCycle:
                        # 自己循環の場合
                        for node in component:
                            if self.dependency_graph.has_edge(node, node):
                                circular_deps.append(
                                    {
                                        "type": "self_dependency",
                                        "file": node,
                                        "severity": "low",
                                        "description": f"自己参照: {node}",
                                    }
                                )

        except Exception as e:
            self.logger.error(f"❌ 循環依存検出エラー: {e}")

        return circular_deps

    def _detect_unused_imports(self) -> List[Dict[str, Any]]:
        """未使用import検出"""
        unused_imports = []

        # 簡易実装: より詳細な解析は別途実装可能
        for py_file in self.project_root.rglob("*.py"):
            if any(
                excluded in str(py_file)
                for excluded in [".git", "__pycache__", ".mirralism/backups"]
            ):
                continue

            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # AST解析でimport文と使用箇所をチェック
                tree = ast.parse(content)
                imports_in_file = []
                names_used = set()

                # import文の収集
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports_in_file.append(
                                {
                                    "name": alias.asname or alias.name.split(".")[0],
                                    "full_name": alias.name,
                                    "line": node.lineno,
                                    "type": "import",
                                }
                            )
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            for alias in node.names:
                                imports_in_file.append(
                                    {
                                        "name": alias.asname or alias.name,
                                        "full_name": f"{node.module}.{alias.name}",
                                        "line": node.lineno,
                                        "type": "from_import",
                                    }
                                )

                # 使用されている名前の収集
                for node in ast.walk(tree):
                    if isinstance(node, ast.Name):
                        names_used.add(node.id)

                # 未使用import検出
                for imp in imports_in_file:
                    if imp["name"] not in names_used and imp["name"] != "__future__":
                        unused_imports.append(
                            {
                                "file": str(py_file.relative_to(self.project_root)),
                                "line": imp["line"],
                                "import_name": imp["name"],
                                "full_import": imp["full_name"],
                                "type": imp["type"],
                                "severity": "low",
                                "description": f"未使用import: {imp['name']}",
                            }
                        )

            except Exception as e:
                self.logger.error(f"❌ 未使用import検出エラー: {py_file} - {e}")

        return unused_imports

    def _find_longest_dependency_path(self) -> int:
        """最長依存パスの検出"""
        try:
            if nx.is_directed_acyclic_graph(self.dependency_graph):
                return nx.dag_longest_path_length(self.dependency_graph)
            else:
                return -1  # 循環があるため測定不可
        except:
            return 0

    def generate_comprehensive_report(self) -> Dict[str, Any]:
        """包括的分析レポートの生成"""
        self.logger.info("📋 包括的レポート生成開始...")

        analysis_results = self.deep_import_analysis()

        # サマリー統計
        summary = {
            "analysis_timestamp": datetime.now().isoformat(),
            "total_python_files": analysis_results["python_files_analyzed"],
            "total_imports": len(analysis_results["import_statements"]),
            "local_imports": len(
                [
                    imp
                    for imp in analysis_results["import_statements"]
                    if imp["is_local"]
                ]
            ),
            "external_imports": len(
                [
                    imp
                    for imp in analysis_results["import_statements"]
                    if not imp["is_local"]
                ]
            ),
            "circular_dependencies_count": len(
                analysis_results["circular_dependencies"]
            ),
            "unused_imports_count": len(analysis_results["unused_imports"]),
            "dependency_complexity": analysis_results["dependency_graph_stats"],
            "overall_health_score": self._calculate_health_score(analysis_results),
        }

        # 詳細レポート
        full_report = {
            "summary": summary,
            "detailed_analysis": analysis_results,
            "recommendations": self._generate_recommendations(analysis_results),
        }

        # レポート保存
        report_file = (
            self.project_root
            / ".mirralism"
            / "reports"
            / f"advanced_dependency_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        report_file.parent.mkdir(parents=True, exist_ok=True)

        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(full_report, f, indent=2, ensure_ascii=False)

        self.logger.info(f"📋 レポート保存完了: {report_file}")
        return full_report

    def _calculate_health_score(self, analysis_results: Dict[str, Any]) -> float:
        """依存関係健全性スコア計算 (0-100)"""
        score = 100.0

        # 循環依存のペナルティ
        circular_penalty = len(analysis_results["circular_dependencies"]) * 10
        score -= min(circular_penalty, 30)

        # 未使用importのペナルティ
        unused_penalty = len(analysis_results["unused_imports"]) * 0.5
        score -= min(unused_penalty, 10)

        # 複雑度ペナルティ
        graph_stats = analysis_results["dependency_graph_stats"]
        if graph_stats["total_nodes"] > 0:
            complexity_ratio = graph_stats["total_edges"] / graph_stats["total_nodes"]
            if complexity_ratio > 3:  # 平均して各ファイルが3つ以上の依存関係
                score -= (complexity_ratio - 3) * 5

        return max(0.0, min(100.0, score))

    def _generate_recommendations(self, analysis_results: Dict[str, Any]) -> List[str]:
        """改善提案の生成"""
        recommendations = []

        if analysis_results["circular_dependencies"]:
            recommendations.append("🔄 循環依存を解消してください。リファクタリングや抽象レイヤーの導入を検討。")

        if analysis_results["unused_imports"]:
            recommendations.append("🧹 未使用importを削除してコードをクリーンに保ってください。")

        graph_stats = analysis_results["dependency_graph_stats"]
        if graph_stats["total_nodes"] > 0:
            complexity_ratio = graph_stats["total_edges"] / graph_stats["total_nodes"]
            if complexity_ratio > 4:
                recommendations.append("📊 依存関係が複雑です。モジュール分割や依存注入の検討をお勧めします。")

        if graph_stats["longest_path"] > 10:
            recommendations.append("📏 依存チェーンが長すぎます。より平坦な構造への再設計を検討してください。")

        if not recommendations:
            recommendations.append("✅ 依存関係は健全な状態です。現在の構造を維持してください。")

        return recommendations


def main():
    """メイン実行関数"""
    analyzer = AdvancedDependencyAnalyzer()
    report = analyzer.generate_comprehensive_report()

    # 結果表示
    print("\n" + "=" * 80)
    print("🔬 MIRRALISM V2 高度依存関係分析結果")
    print("=" * 80)

    summary = report["summary"]
    print(f"📊 分析ファイル数: {summary['total_python_files']}")
    print(f"📋 総import数: {summary['total_imports']}")
    print(f"🏠 ローカルimport: {summary['local_imports']}")
    print(f"📦 外部import: {summary['external_imports']}")
    print(f"🔄 循環依存: {summary['circular_dependencies_count']}件")
    print(f"🧹 未使用import: {summary['unused_imports_count']}件")
    print(f"💯 健全性スコア: {summary['overall_health_score']:.1f}/100")

    complexity = summary["dependency_complexity"]
    print(f"\n📈 依存関係複雑度:")
    print(f"  - ノード数: {complexity['total_nodes']}")
    print(f"  - エッジ数: {complexity['total_edges']}")
    print(f"  - 最長パス: {complexity['longest_path']}")

    print("\n💡 推奨事項:")
    for rec in report["recommendations"]:
        print(f"  {rec}")

    if summary["circular_dependencies_count"] > 0:
        print("\n🔄 循環依存詳細:")
        for circ in report["detailed_analysis"]["circular_dependencies"][:3]:
            print(f"  - {circ['description']}")
            print(f"    関与ファイル: {', '.join(circ.get('files_involved', [])[:3])}")

    print("=" * 80)


if __name__ == "__main__":
    main()
