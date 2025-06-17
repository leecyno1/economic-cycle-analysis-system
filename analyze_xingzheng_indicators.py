#!/usr/bin/env python3
"""
分析兴证策略行业中观&拥挤度数据库的指标体系
"""

import pandas as pd
import numpy as np
from collections import defaultdict

def analyze_xingzheng_indicators():
    """分析兴证策略的行业指标体系"""
    
    file_path = '【兴证策略】行业中观&拥挤度数据库（20250530）.xlsx'
    
    print("=== 兴证策略行业指标体系分析 ===\n")
    
    # 1. 分析工作表结构
    xl = pd.ExcelFile(file_path)
    print(f"工作表数量: {len(xl.sheet_names)}")
    for i, sheet in enumerate(xl.sheet_names):
        print(f"{i+1}. {sheet}")
    
    # 2. 分析中观指标明细
    print("\n=== 中观指标明细分析 ===")
    df = pd.read_excel(file_path, sheet_name='1.5 中观指标明细', header=1)
    print(f"总指标数量: {len(df)}")
    print(f"数据维度: {df.shape}")
    
    # 3. 分析行业分类体系
    print("\n=== 行业分类体系 ===")
    
    # 获取前几列的分类信息
    classification_cols = []
    for i in range(min(6, len(df.columns))):
        col = df.columns[i]
        if isinstance(col, str) and col not in ['nan', 'NaN']:
            classification_cols.append(col)
    
    print(f"分类列: {classification_cols}")
    
    # 统计各级分类
    industry_hierarchy = defaultdict(lambda: defaultdict(set))
    
    for idx, row in df.iterrows():
        if len(classification_cols) >= 3:
            level1 = str(row[classification_cols[0]]) if pd.notna(row[classification_cols[0]]) else 'Unknown'
            level2 = str(row[classification_cols[1]]) if pd.notna(row[classification_cols[1]]) else 'Unknown'
            level3 = str(row[classification_cols[2]]) if pd.notna(row[classification_cols[2]]) else 'Unknown'
            
            if level1 != 'nan' and level2 != 'nan':
                industry_hierarchy[level1][level2].add(level3)
    
    # 输出行业层级结构
    print("\n=== 行业层级结构 ===")
    for level1, level2_dict in industry_hierarchy.items():
        print(f"\n【{level1}】 ({len(level2_dict)}个二级行业)")
        for level2, level3_set in level2_dict.items():
            level3_list = [x for x in level3_set if x != 'nan' and x != 'Unknown']
            if level3_list:
                print(f"  ├─ {level2} ({len(level3_list)}个细分)")
                for level3 in sorted(level3_list)[:3]:  # 只显示前3个
                    print(f"      └─ {level3}")
                if len(level3_list) > 3:
                    print(f"      └─ ... 还有{len(level3_list)-3}个")
    
    # 4. 分析具体指标
    print("\n=== 具体指标分析 ===")
    
    # 提取指标名称（通常在第4列或第5列）
    indicator_col = None
    for i in range(3, min(8, len(df.columns))):
        col = df.columns[i]
        if isinstance(col, str) and '指标' not in col and col not in ['nan', 'NaN']:
            # 检查这一列是否包含指标名称
            sample_values = df[col].dropna().head(10)
            if len(sample_values) > 0:
                indicator_col = col
                break
    
    if indicator_col:
        print(f"指标列: {indicator_col}")
        indicators = df[indicator_col].dropna().unique()
        print(f"指标数量: {len(indicators)}")
        
        # 按行业分类统计指标
        indicator_by_industry = defaultdict(list)
        for idx, row in df.iterrows():
            if pd.notna(row[indicator_col]):
                level1 = str(row[classification_cols[0]]) if pd.notna(row[classification_cols[0]]) else 'Unknown'
                level2 = str(row[classification_cols[1]]) if pd.notna(row[classification_cols[1]]) else 'Unknown'
                indicator_name = str(row[indicator_col])
                
                if level1 != 'nan' and level2 != 'nan':
                    indicator_by_industry[f"{level1}-{level2}"].append(indicator_name)
        
        print("\n=== 各行业指标数量统计 ===")
        for industry, indicators in sorted(indicator_by_industry.items()):
            print(f"{industry}: {len(indicators)}个指标")
    
    # 5. 输出示例指标
    print("\n=== 指标示例 ===")
    for idx, row in df.head(20).iterrows():
        row_info = []
        for i in range(min(5, len(classification_cols) + 2)):
            if i < len(df.columns) and pd.notna(row.iloc[i]):
                val = str(row.iloc[i])
                if val != 'nan':
                    row_info.append(val)
        
        if len(row_info) >= 3:
            print(f"{idx+1}. {' | '.join(row_info)}")
    
    return df, industry_hierarchy

if __name__ == "__main__":
    df, hierarchy = analyze_xingzheng_indicators() 