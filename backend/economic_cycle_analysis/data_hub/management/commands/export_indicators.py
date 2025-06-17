import csv
from django.core.management.base import BaseCommand
from data_hub.models import Indicator, IndicatorCategory

class Command(BaseCommand):
    help = 'Exports all indicators to a CSV file.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            default='indicators_export.csv',
            help='Output CSV file path.'
        )

    def handle(self, *args, **options):
        output_file = options['output']
        self.stdout.write(self.style.SUCCESS(f'Exporting indicators to {output_file}...'))

        try:
            indicators = Indicator.objects.all().order_by('category__name', 'name')
            
            field_names = [field.name for field in Indicator._meta.fields if field.name not in ['id']]
            # Make sure 'category_name' is in the header, not 'category'
            header = [f if f != 'category' else 'category_name' for f in field_names]

            with open(output_file, 'w', newline='', encoding='utf-8-sig') as csvfile: # Use utf-8-sig for Excel compatibility
                writer = csv.writer(csvfile)
                
                writer.writerow(header)
                
                for indicator in indicators:
                    row = []
                    for field_name in field_names:
                        if field_name == 'category':
                            value = indicator.category.name if indicator.category else ''
                        else:
                            value = getattr(indicator, field_name)
                        row.append(value)
                    writer.writerow(row)

            self.stdout.write(self.style.SUCCESS(f'Successfully exported {indicators.count()} indicators to {output_file}'))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'An error occurred: {e}')) 