from django.core.management.base import BaseCommand
from django.db import transaction
from data_hub.models import Indicator, IndicatorCategory

class Command(BaseCommand):
    help = 'Clears all indicator categories and indicators from the database.'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('开始清除所有指标和分类数据...'))
        
        try:
            indicator_count = Indicator.objects.all().count()
            category_count = IndicatorCategory.objects.all().count()

            if indicator_count == 0 and category_count == 0:
                self.stdout.write(self.style.SUCCESS('数据库已经为空，无需清除。'))
                return

            # 先删除指标，再删除分类
            Indicator.objects.all().delete()
            IndicatorCategory.objects.all().delete()
            
            self.stdout.write(self.style.SUCCESS(
                f'成功删除 {indicator_count} 个指标和 {category_count} 个分类。'
            ))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'清除数据时发生错误: {e}'))
            # 事务将自动回滚
            raise e 