#!/usr/bin/env python3
"""
完整分析兴证策略915个专业指标
7大类行业 × 37个二级行业 × 200+细分领域
"""

import pandas as pd
import numpy as np
from collections import defaultdict

def analyze_xingzheng_complete():
    """完整分析兴证策略的915个指标体系"""
    
    file_path = '【兴证策略】行业中观&拥挤度数据库（20250530）.xlsx'
    
    print("=== 兴证策略915个指标完整分析 ===\n")
    
    # 读取中观指标明细
    df = pd.read_excel(file_path, sheet_name='1.5 中观指标明细', header=1)
    
    print(f"📊 总指标数量: {len(df)}")
    print(f"📈 数据维度: {df.shape}")
    print(f"📋 列名: {list(df.columns)}\n")
    
    # 1. 分析7大类行业
    print("=== 🏭 7大类行业分析 ===")
    level1_col = None
    for col in df.columns:
        if '一级' in str(col) or '大类' in str(col) or col in ['行业分类', '行业类别']:
            level1_col = col
            break
    
    if level1_col:
        level1_industries = df[level1_col].value_counts()
        print(f"一级行业数量: {len(level1_industries)}")
        for i, (industry, count) in enumerate(level1_industries.items(), 1):
            if pd.notna(industry):
                print(f"  {i}. {industry}: {count}个指标")
    else:
        print("未找到一级行业分类列")
    
    # 2. 分析37个二级行业
    print(f"\n=== 🏢 二级行业分析 ===")
    level2_col = None
    for col in df.columns:
        if '二级' in str(col) or '子行业' in str(col):
            level2_col = col
            break
    
    if level2_col:
        level2_industries = df[level2_col].value_counts()
        print(f"二级行业数量: {len(level2_industries)}")
        print("前20个二级行业:")
        for i, (industry, count) in enumerate(level2_industries.head(20).items(), 1):
            if pd.notna(industry):
                print(f"  {i}. {industry}: {count}个指标")
    else:
        print("未找到二级行业分类列")
    
    # 3. 分析200+细分领域
    print(f"\n=== 🔬 细分领域分析 ===")
    level3_col = None
    for col in df.columns:
        if '三级' in str(col) or '细分' in str(col) or '子类' in str(col):
            level3_col = col
            break
    
    if level3_col:
        level3_industries = df[level3_col].value_counts()
        print(f"细分领域数量: {len(level3_industries)}")
        print("前15个细分领域:")
        for i, (industry, count) in enumerate(level3_industries.head(15).items(), 1):
            if pd.notna(industry):
                print(f"  {i}. {industry}: {count}个指标")
    else:
        print("未找到细分领域分类列")
    
    # 4. 分析指标类型
    print(f"\n=== 📊 指标类型分析 ===")
    indicator_type_col = None
    for col in df.columns:
        if '指标类型' in str(col) or '类型' in str(col) or '分类' in str(col):
            indicator_type_col = col
            break
    
    if indicator_type_col:
        indicator_types = df[indicator_type_col].value_counts()
        print(f"指标类型数量: {len(indicator_types)}")
        for i, (type_name, count) in enumerate(indicator_types.items(), 1):
            if pd.notna(type_name):
                print(f"  {i}. {type_name}: {count}个指标")
    
    # 5. 分析指标名称和数据源
    print(f"\n=== 📋 指标详情分析 ===")
    indicator_name_col = None
    data_source_col = None
    
    for col in df.columns:
        if '指标名称' in str(col) or '名称' in str(col):
            indicator_name_col = col
        if '数据源' in str(col) or '来源' in str(col):
            data_source_col = col
    
    if indicator_name_col:
        print(f"指标名称列: {indicator_name_col}")
        print("前10个指标名称:")
        for i, name in enumerate(df[indicator_name_col].head(10), 1):
            if pd.notna(name):
                print(f"  {i}. {name}")
    
    if data_source_col:
        data_sources = df[data_source_col].value_counts()
        print(f"\n数据源分布:")
        for source, count in data_sources.head(10).items():
            if pd.notna(source):
                print(f"  {source}: {count}个指标")
    
    # 6. 构建完整的指标体系结构
    print(f"\n=== 🏗️ 指标体系结构构建 ===")
    
    # 创建层级结构
    hierarchy = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    
    for idx, row in df.iterrows():
        level1 = row.get(level1_col, '未分类') if level1_col else '未分类'
        level2 = row.get(level2_col, '未分类') if level2_col else '未分类'
        level3 = row.get(level3_col, '未分类') if level3_col else '未分类'
        indicator = row.get(indicator_name_col, f'指标_{idx}') if indicator_name_col else f'指标_{idx}'
        
        if pd.notna(level1) and pd.notna(level2) and pd.notna(indicator):
            hierarchy[level1][level2][level3].append(indicator)
    
    print("完整指标体系结构:")
    total_indicators = 0
    for level1, level2_dict in hierarchy.items():
        if pd.notna(level1) and level1 != '未分类':
            level1_count = sum(len(indicators) for level3_dict in level2_dict.values() for indicators in level3_dict.values())
            print(f"\n🏭 {level1} ({level1_count}个指标)")
            
            for level2, level3_dict in level2_dict.items():
                if pd.notna(level2) and level2 != '未分类':
                    level2_count = sum(len(indicators) for indicators in level3_dict.values())
                    print(f"  🏢 {level2} ({level2_count}个指标)")
                    
                    for level3, indicators in level3_dict.items():
                        if pd.notna(level3) and level3 != '未分类' and len(indicators) > 0:
                            print(f"    🔬 {level3} ({len(indicators)}个指标)")
                            total_indicators += len(indicators)
    
    print(f"\n📊 统计汇总:")
    print(f"  总指标数量: {total_indicators}")
    print(f"  一级行业数量: {len([k for k in hierarchy.keys() if pd.notna(k) and k != '未分类'])}")
    print(f"  二级行业数量: {sum(len([k for k in v.keys() if pd.notna(k) and k != '未分类']) for v in hierarchy.values())}")
    print(f"  细分领域数量: {sum(len([k for level3_dict in v.values() for k in level3_dict.keys() if pd.notna(k) and k != '未分类']) for v in hierarchy.values())}")
    
    return hierarchy, df

if __name__ == "__main__":
    hierarchy, df = analyze_xingzheng_complete() 