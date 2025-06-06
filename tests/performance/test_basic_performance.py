#!/usr/bin/env python3
"""
基本パフォーマンステスト
========================

GitHub Actions CI/CD用の軽量パフォーマンステスト
"""

import time
import pytest


def test_basic_performance():
    """基本的なパフォーマンステスト"""
    start_time = time.time()
    
    # 軽量な処理をテスト
    data = list(range(1000))
    result = sum(data)
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    # 1秒以内で完了することを確認
    assert execution_time < 1.0
    assert result == 499500  # 0から999の合計
    
    print(f"✅ パフォーマンステスト完了: {execution_time:.3f}秒")


def test_memory_efficiency():
    """メモリ効率テスト"""
    import sys
    
    # 軽量なメモリ使用量テスト
    data = [i for i in range(100)]
    memory_size = sys.getsizeof(data)
    
    # 合理的なメモリ使用量であることを確認
    assert memory_size < 10000  # 10KB未満
    
    print(f"✅ メモリ効率テスト完了: {memory_size}バイト")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])