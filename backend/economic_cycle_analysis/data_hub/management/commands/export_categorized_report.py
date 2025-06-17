from django.core.management.base import BaseCommand
from data_hub.models import Indicator
from collections import defaultdict

class Command(BaseCommand):
    help = 'Exports all indicators to a categorized Markdown file.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            default='categorized_indicators_report.md',
            help='Output Markdown file path.'
        )

    def handle(self, *args, **options):
        output_file = options['output']
        self.stdout.write(self.style.SUCCESS(f'Generating categorized report at {output_file}...'))

        try:
            # Eager load the category to avoid N+1 queries
            indicators = Indicator.objects.select_related('category').order_by('category__name', 'name')
            
            # Group indicators by category
            categorized_indicators = defaultdict(list)
            for indicator in indicators:
                category_name = indicator.category.name if indicator.category else '未分类'
                categorized_indicators[category_name].append(indicator)

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("# 全部分类指标报告\n\n")
                f.write(f"报告生成时间: {indicators.first().updated_at.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"指标总数: {indicators.count()}\n\n")

                # Sort categories for consistent output
                for category_name in sorted(categorized_indicators.keys()):
                    f.write(f"## {category_name} (共 {len(categorized_indicators[category_name])} 项)\n\n")
                    for indicator in categorized_indicators[category_name]:
                        f.write(f"- **{indicator.name}**\n")
                        f.write(f"  - **ID**: `{indicator.code}`\n")
                        f.write(f"  - **子分类**: {indicator.sub_category}\n")
                        f.write(f"  - **描述**: {indicator.description}\n\n")
            
            self.stdout.write(self.style.SUCCESS(f'Successfully generated report with {indicators.count()} indicators.'))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'An error occurred: {e}')) 