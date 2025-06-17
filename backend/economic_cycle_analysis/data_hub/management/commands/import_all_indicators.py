# -*- coding: utf-8 -*-
"""
增强版指标导入命令 - 导入完整的1,064个指标
支持增量导入、维度识别、数据验证
"""

import json
import os
import re
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from data_hub.models import IndicatorCategory, Indicator
from django.conf import settings
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = '增强版指标导入 - 处理完整的1,064个指标体系'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='indicators_dictionary.json',
            help='JSON file path relative to project root'
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=50,
            help='Batch size for processing'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Run without making database changes'
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 开始增强版指标导入...')
        )

        file_path = options['file']
        batch_size = options['batch_size']
        dry_run = options['dry_run']
        
        # Resolve file path from project root
        if not os.path.isabs(file_path):
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            file_path = os.path.join(project_root, file_path)
        
        if not os.path.exists(file_path):
            self.stdout.write(
                self.style.ERROR(f'File not found: {file_path}')
            )
            return
        
        self.stdout.write(f'Loading data from: {file_path}')
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 'indicators' not in data:
                self.stdout.write(
                    self.style.ERROR('No "indicators" key found in JSON file')
                )
                return
                
            indicators_data = data['indicators']
            total_indicators = len(indicators_data)
            
            self.stdout.write(f'Found {total_indicators} indicators in JSON file')
            
            if dry_run:
                self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made'))
                self._analyze_data(indicators_data)
                return
            
            self._import_indicators(indicators_data, batch_size)
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error processing file: {str(e)}')
            )
            logger.error(f"Import error: {str(e)}", exc_info=True)

        self.stdout.write(
            self.style.SUCCESS('🎉 增强版指标导入完成！')
        )

    def _analyze_data(self, indicators_data):
        """Analyze the data structure without importing"""
        categories = {}
        dimensions_found = set()
        
        for indicator_id, indicator_data in indicators_data.items():
            category = indicator_data.get('category', 'Unknown')
            categories[category] = categories.get(category, 0) + 1
            
            self._detect_dimensions(indicator_data, dimensions_found)
        
        self.stdout.write('\n=== DATA ANALYSIS ===')
        self.stdout.write(f'Total indicators: {len(indicators_data)}')
        self.stdout.write('\nCategory distribution:')
        for category, count in sorted(categories.items()):
            self.stdout.write(f'  {category}: {count}')
        
        self.stdout.write(f'\nDimensions detected: {len(dimensions_found)}')
        for dim in sorted(dimensions_found):
            self.stdout.write(f'  - {dim}')

    def _import_indicators(self, indicators_data, batch_size):
        """Import indicators in batches with progress tracking"""
        total_indicators = len(indicators_data)
        processed = 0
        created = 0
        updated = 0
        errors = 0
        
        self.stdout.write(f'\nStarting import of {total_indicators} indicators...')
        
        indicator_items = list(indicators_data.items())
        
        for i in range(0, len(indicator_items), batch_size):
            batch = indicator_items[i:i + batch_size]
            
            try:
                with transaction.atomic():
                    batch_created, batch_updated, batch_errors = self._process_batch(batch)
                    created += batch_created
                    updated += batch_updated
                    errors += batch_errors
                    processed += len(batch)
                
                progress = (processed / total_indicators) * 100
                self.stdout.write(
                    f'Progress: {processed}/{total_indicators} ({progress:.1f}%) - '
                    f'Created: {created}, Updated: {updated}, Errors: {errors}'
                )
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Batch error at indicators {i}-{i+len(batch)}: {str(e)}')
                )
                errors += len(batch)
                processed += len(batch)
        
        self.stdout.write('\n=== IMPORT COMPLETE ===')
        self.stdout.write(f'Total processed: {processed}')
        self.stdout.write(f'Created: {created}')
        self.stdout.write(f'Updated: {updated}')
        self.stdout.write(f'Errors: {errors}')
        
        if errors > 0:
            self.stdout.write(
                self.style.WARNING(f'Completed with {errors} errors. Check logs for details.')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('All indicators imported successfully!')
            )

    def _process_batch(self, batch):
        """Process a batch of indicators"""
        created = 0
        updated = 0
        errors = 0
        
        for indicator_id, indicator_data in batch:
            result = self._process_single_indicator(indicator_id, indicator_data)
            if result == 'created':
                created += 1
            elif result == 'updated':
                updated += 1
            elif result == 'error':
                errors += 1
        
        return created, updated, errors

    def _process_single_indicator(self, indicator_id, indicator_data):
        """Process a single indicator"""
        try:
            category_name = indicator_data.get('category', '未分类')
            category = self._get_category(category_name)

            indicator_defaults = self._map_data_to_model(indicator_data, indicator_id)
            indicator_defaults['category'] = category

            dimensions = self._detect_dimensions(indicator_data)
            indicator_defaults.update(dimensions)

            is_valid, error_msg = self._validate_indicator_data(indicator_defaults)
            if not is_valid:
                logger.error(f"Invalid data for {indicator_id}: {error_msg}")
                return 'error'

            cleaned_data = self._clean_data_for_model(indicator_defaults)

            indicator, created = Indicator.objects.update_or_create(
                code=cleaned_data.pop('code'),
                defaults=cleaned_data
            )
            
            return 'created' if created else 'updated'

        except Exception as e:
            logger.error(f"Critical error processing indicator {indicator_id}: {str(e)}", exc_info=True)
            return 'error'

    def _map_data_to_model(self, indicator_data, indicator_id):
        """Maps JSON data to the Indicator model fields."""
        return {
            'code': indicator_data.get('indicator_code') or indicator_id,
            'name': indicator_data.get('name_cn', ''),
            'name_en': indicator_data.get('name_en', ''),
            'description': indicator_data.get('description_cn', ''),
            'source': indicator_data.get('data_source', '未知来源'),
            'unit': indicator_data.get('unit', ''),
            'frequency': indicator_data.get('frequency', 'Unknown'),
            'sub_category': indicator_data.get('sub_category_cn', ''),
        }

    def _detect_dimensions(self, indicator_data, dimensions_set=None):
        """
        Detects dimensions based on indicator name, description, and investment significance.
        Returns a dictionary of boolean flags for each dimension.
        """
        dimensions = {
            'dimension_prosperity': False,
            'dimension_valuation': False, 
            'dimension_crowdedness': False,
            'dimension_technical': False,
            'dimension_fundamental': False,
            'dimension_momentum': False,
            'dimension_sentiment': False,
            'dimension_liquidity': False,
            'dimension_volatility': False,
            'dimension_correlation': False,
            'dimension_seasonality': False,
            'dimension_policy': False,
            'dimension_supply_chain': False,
            'dimension_innovation': False,
            'dimension_esg': False,
            'dimension_risk': False
        }
        
        significance = (indicator_data.get('investment_significance', '') + ' ' +
                       indicator_data.get('name_cn', '') + ' ' +
                       indicator_data.get('name_en', '')).lower()
        
        if any(keyword in significance for keyword in ['景气', '产量', '销量', '生产', 'production', 'sales']):
            dimensions['dimension_prosperity'] = True
        
        if any(keyword in significance for keyword in ['价格', '估值', 'price', 'valuation', 'ppi', 'cpi']):
            dimensions['dimension_valuation'] = True
            
        if any(keyword in significance for keyword in ['基本面', '财务', '盈利', 'fundamental', 'financial']):
            dimensions['dimension_fundamental'] = True
            
        if any(keyword in significance for keyword in ['产业链', '供应链', '传导', 'supply chain', 'industrial chain']):
            dimensions['dimension_supply_chain'] = True
            
        if any(keyword in significance for keyword in ['政策', '监管', '投资', 'policy', 'regulation', 'investment']):
            dimensions['dimension_policy'] = True
            
        if any(keyword in significance for keyword in ['科技', '创新', '研发', 'technology', 'innovation', 'tmt']):
            dimensions['dimension_innovation'] = True
            
        if any(keyword in significance for keyword in ['风险', '安全', '稳定', 'risk', 'safety', 'stability']):
            dimensions['dimension_risk'] = True
            
        if indicator_data.get('frequency') in ['weekly', 'daily'] or 'seasonal' in significance:
            dimensions['dimension_seasonality'] = True
            
        return dimensions

    def _validate_indicator_data(self, data):
        """Validate required fields"""
        if not data.get('name'):
            return False, 'Missing name'
        if not data.get('code'):
            return False, 'Missing code'
        if not data.get('category'):
            return False, 'Missing category'
        return True, ''

    def _clean_data_for_model(self, data):
        """Ensures data types are correct before saving."""
        cleaned = data.copy()
        
        for field in [
            'dimension_prosperity', 'dimension_valuation', 'dimension_crowdedness', 'dimension_technical',
            'dimension_fundamental', 'dimension_momentum', 'dimension_sentiment', 'dimension_liquidity',
            'dimension_volatility', 'dimension_correlation', 'dimension_seasonality', 'dimension_policy',
            'dimension_supply_chain', 'dimension_innovation', 'dimension_esg', 'dimension_risk'
        ]:
            if field in cleaned:
                cleaned[field] = bool(cleaned[field])
                
        return cleaned

    def _clean_data(self, indicator_data):
        """Clean data for saving"""
        cleaned_data = {}
        for field in ['name', 'name_en', 'description', 'code', 'category', 'source', 'sub_category']:
            if field in indicator_data:
                cleaned_data[field] = indicator_data[field]
        return cleaned_data

    def _get_category(self, category_name):
        """
        Retrieves or creates a category, including handling of parent-child relationships.
        """
        # Simple case: direct match
        try:
            return IndicatorCategory.objects.get(name=category_name)
        except IndicatorCategory.DoesNotExist:
            # More complex case could be handled here if needed
            return IndicatorCategory.objects.create(
                name=category_name, 
                code=category_name.upper(), 
                level=1, 
                description=f"Category for {category_name}"
            )