import os
import pandas as pd
from django.core.management.base import BaseCommand
from data_hub.models import Indicator

class Command(BaseCommand):
    help = 'Compares indicators in the database against a source Excel file to find missing ones.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--excel-file',
            type=str,
            required=True,
            help='Path to the source Excel file.'
        )
        parser.add_argument(
            '--sheet-name',
            type=str,
            default='指标字典',
            help='Sheet name containing the indicator list.'
        )
        parser.add_argument(
            '--column-name',
            type=str,
            default='指标名称',
            help='Column name for the indicator names.'
        )
        parser.add_argument(
            '--output',
            type=str,
            default='missing_indicators_report.txt',
            help='Output file for the list of missing indicators.'
        )
        parser.add_argument(
            '--list-sheets',
            action='store_true',
            help='List all sheet names in the Excel file and exit.'
        )
        parser.add_argument(
            '--list-columns',
            action='store_true',
            help='List all column names in the specified sheet and exit.'
        )

    def handle(self, *args, **options):
        excel_file = options['excel_file']
        sheet_name = options['sheet_name']
        column_name = options['column_name']
        output_file = options['output']
        list_sheets = options['list_sheets']
        list_columns = options['list_columns']

        if list_sheets:
            try:
                xls = pd.ExcelFile(excel_file)
                self.stdout.write(self.style.SUCCESS('Available sheets in the Excel file:'))
                for sheet in xls.sheet_names:
                    self.stdout.write(f'- {sheet}')
            except FileNotFoundError:
                self.stderr.write(self.style.ERROR(f'Excel file not found at: {excel_file}'))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f'An error occurred: {e}'))
            return
            
        if list_columns:
            try:
                df = pd.read_excel(excel_file, sheet_name=sheet_name)
                self.stdout.write(self.style.SUCCESS(f'Available columns in sheet "{sheet_name}":'))
                for col in df.columns:
                    self.stdout.write(f'- {col}')
            except Exception as e:
                self.stderr.write(self.style.ERROR(f'An error occurred while reading sheet "{sheet_name}": {e}'))
            return

        self.stdout.write(self.style.SUCCESS('🚀 Starting indicator comparison...'))

        # 1. Get indicators from the source Excel file
        try:
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            if column_name not in df.columns:
                self.stderr.write(self.style.ERROR(f'Column "{column_name}" not found in sheet "{sheet_name}".'))
                return
            source_indicators = set(df[column_name].dropna().astype(str))
            self.stdout.write(f'Found {len(source_indicators)} unique indicators in the source file.')
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f'Excel file not found at: {excel_file}'))
            return
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'An error occurred while reading the Excel file: {e}'))
            return

        # 2. Get indicators from the database
        db_indicators = set(Indicator.objects.values_list('name', flat=True))
        self.stdout.write(f'Found {len(db_indicators)} indicators in the database.')

        # 3. Compare and find the missing ones
        missing_indicators = source_indicators - db_indicators
        
        self.stdout.write(self.style.SUCCESS('\n=== Comparison Report ==='))
        self.stdout.write(f'Source Indicators: {len(source_indicators)}')
        self.stdout.write(f'Database Indicators: {len(db_indicators)}')
        self.stdout.write(f'Missing Indicators: {len(missing_indicators)}')

        # 4. Save the report
        if missing_indicators:
            self.stdout.write(self.style.WARNING(f'\nSaving {len(missing_indicators)} missing indicator names to {output_file}...'))
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    for indicator_name in sorted(list(missing_indicators)):
                        f.write(f'{indicator_name}\n')
                self.stdout.write(self.style.SUCCESS('Report saved successfully.'))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f'Failed to write report file: {e}'))
        else:
            self.stdout.write(self.style.SUCCESS('\nNo missing indicators found. The database is up-to-date.'))

        self.stdout.write(self.style.SUCCESS('✅ Comparison complete.')) 