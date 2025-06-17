import pandas as pd
from django.core.management.base import BaseCommand
from data_hub.models import Indicator
from django.db.models import Q

class Command(BaseCommand):
    help = 'Cleans and enriches indicator metadata using a source Excel file.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--excel-file',
            type=str,
            required=False, # No longer required if only cleaning
            help='Path to the source Excel file for enrichment.'
        )
        parser.add_argument(
            '--sheet-name',
            type=str,
            default='1.5 中观指标明细',
            help='Sheet name containing the indicator details.'
        )
        parser.add_argument(
            '--clean-only',
            action='store_true',
            help='Only perform the cleaning phase.'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simulate the process without making any changes to the database.'
        )

    def handle(self, *args, **options):
        excel_file = options['excel_file']
        sheet_name = options['sheet_name']
        is_dry_run = options['dry_run']
        clean_only = options['clean_only']

        if is_dry_run:
            self.stdout.write(self.style.WARNING('--- DRY RUN MODE ---'))

        # 1. Cleaning Phase: Delete invalid indicators
        self.stdout.write(self.style.SUCCESS('--- Phase 1: Cleaning invalid indicators ---'))
        invalid_indicators_query = Q(name__iexact='noname') | Q(name__isnull=True) | Q(name__exact='') | Q(name__startswith='Unnamed:')
        invalid_indicators = Indicator.objects.filter(invalid_indicators_query)
        count_to_delete = invalid_indicators.count()

        if count_to_delete > 0:
            self.stdout.write(f'Found {count_to_delete} invalid indicators to delete.')
            if not is_dry_run:
                deleted_count, _ = invalid_indicators.delete()
                self.stdout.write(self.style.SUCCESS(f'Successfully deleted {deleted_count} invalid indicators.'))
        else:
            self.stdout.write('No invalid indicators found. Database is clean.')

        if clean_only:
            self.stdout.write(self.style.SUCCESS('--- Clean-only mode finished ---'))
            return
            
        if not excel_file:
            self.stderr.write(self.style.ERROR('Error: --excel-file is required unless --clean-only is specified.'))
            return

        # 2. Enrichment Phase: Update sub_category and description
        self.stdout.write(self.style.SUCCESS('\n--- Phase 2: Enriching indicator metadata ---'))
        
        try:
            self.stdout.write(f'Reading data from {excel_file} [Sheet: {sheet_name}]...')
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            # Standardize column names for easier access, but handle non-string columns
            df.columns = [col.strip() if isinstance(col, str) else col for col in df.columns]
            
            indicator_map = {item['指标']: item for item in df.to_dict('records')}
            self.stdout.write(f'Successfully loaded {len(indicator_map)} unique indicators from Excel.')

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f'Excel file not found at: {excel_file}'))
            return
        except KeyError as e:
            self.stderr.write(self.style.ERROR(f'Column not found in Excel sheet: {e}. Please check sheet_name and column names.'))
            return
        
        indicators_to_update = []
        updated_count = 0
        not_found_count = 0

        all_indicators = Indicator.objects.all()
        self.stdout.write(f'Processing {all_indicators.count()} indicators from the database...')

        for indicator in all_indicators:
            source_data = indicator_map.get(indicator.name)
            
            if source_data:
                new_sub_category = str(source_data.get('一级行业映射', ''))
                new_description = str(source_data.get('指标类型', ''))
                
                if indicator.sub_category != new_sub_category or indicator.description != new_description:
                    indicator.sub_category = new_sub_category
                    indicator.description = new_description
                    indicators_to_update.append(indicator)
                    updated_count += 1
            else:
                not_found_count += 1
        
        if not is_dry_run and indicators_to_update:
            self.stdout.write(f'Updating {len(indicators_to_update)} indicators in the database...')
            Indicator.objects.bulk_update(indicators_to_update, ['sub_category', 'description'])
            self.stdout.write(self.style.SUCCESS('Bulk update complete.'))

        # 3. Final Report
        self.stdout.write(self.style.SUCCESS('\n--- Refinement Report ---'))
        self.stdout.write(f"Indicators updated: {updated_count}")
        self.stdout.write(f"Indicators not found in source Excel (skipped): {not_found_count}")
        if is_dry_run:
            self.stdout.write(self.style.WARNING('NOTE: No changes were saved to the database (dry run).'))
        self.stdout.write(self.style.SUCCESS('--- Process Finished ---'))
