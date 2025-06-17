#!/usr/bin/env python3
"""
指标扩展脚本 - 从兴证策略Excel文件提取更多指标
目标：从93个指标扩展到500+个指标
"""

import pandas as pd
import json
import re
from datetime import datetime
import os
import sys

# 添加项目路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

class FullIndicatorGenerator:
    def __init__(self, excel_file_path, sheet_name, output_file):
        self.excel_file_path = excel_file_path
        self.sheet_name = sheet_name
        self.output_file = output_file
        self.indicators = {}

    def _generate_indicator_id(self, category, name):
        """Generates a structured and unique indicator ID."""
        category_prefix = re.sub(r'[^A-Z]', '', category.upper())[:4]
        clean_name = re.sub(r'[^\w]', '', name)
        
        base_id = f"{category_prefix}_{clean_name}"
        
        # Ensure uniqueness
        counter = 1
        indicator_id = base_id
        while indicator_id in self.indicators:
            indicator_id = f"{base_id}_{counter}"
            counter += 1
        return indicator_id

    def process_and_generate(self):
        """Reads the Excel sheet and generates the full indicator JSON."""
        print(f"🚀 Processing sheet '{self.sheet_name}' from '{self.excel_file_path}'...")

        try:
            df = pd.read_excel(self.excel_file_path, sheet_name=self.sheet_name)
        except Exception as e:
            print(f"❌ Error reading Excel file: {e}")
            return

        # Define expected columns
        required_columns = ['指标', '大类行业映射', '一级行业映射', '指标类型']
        for col in required_columns:
            if col not in df.columns:
                print(f"❌ Required column '{col}' not found in sheet '{self.sheet_name}'.")
                return
        
        for index, row in df.iterrows():
            indicator_name = row['指标']
            if pd.isna(indicator_name):
                continue

            category_name = row['大类行业映射']
            sub_category_name = row['一级行业映射']
            description = row['指标类型']
            
            indicator_id = self._generate_indicator_id(category_name, indicator_name)

            self.indicators[indicator_id] = {
                "indicator_code": indicator_id,
                "name": indicator_name,
                "name_cn": indicator_name,
                "name_en": "", # To be filled later if needed
                "category": category_name,
                "sub_category_cn": sub_category_name,
                "description_cn": description,
                "data_source": "兴证策略",
                "unit": "", # To be filled later if needed
                "frequency": "Unknown",
            }
        
        print(f"✅ Successfully processed {len(self.indicators)} indicators.")
        self._save_to_json()

    def _save_to_json(self):
        """Saves the processed indicators to a JSON file."""
        full_data = {
            "metadata": {
                "version": "3.0",
                "created_date": datetime.now().strftime("%Y-%m-%d"),
                "total_indicators": len(self.indicators),
                "data_source": "兴证策略行业中观&拥挤度数据库 (Full)",
                "description": "Contains all indicators extracted from the source Excel file."
            },
            "indicators": self.indicators
        }
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(full_data, f, ensure_ascii=False, indent=2)
            
        print(f"💾 Full indicator data saved to: {self.output_file}")

def main():
    """Main execution function."""
    excel_file = "【兴证策略】行业中观&拥挤度数据库（20250530）.xlsx"
    sheet_name = "1.5 中观指标明细"
    output_file = "full_indicators.json"
    
    if not os.path.exists(excel_file):
        print(f"❌ Source Excel file not found: {excel_file}")
        return

    generator = FullIndicatorGenerator(excel_file, sheet_name, output_file)
    generator.process_and_generate()

if __name__ == "__main__":
    main() 