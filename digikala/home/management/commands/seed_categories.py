from django.core.management.base import BaseCommand
from django.utils.text import slugify

from home.models import Category, Product


class Command(BaseCommand):
    help = 'Create default categories and auto-assign products'

    def handle(self, *args, **options):
        default_categories = [
            'موبایل',
            'تبلت',
            'لپ تاپ',
            'لوازم جانبی',
            'ساعت هوشمند',
            'هدفون',
            'اسپیکر',
            'سایر',
        ]

        category_map = {}
        for category_name in default_categories:
            category, _ = Category.objects.get_or_create(name=category_name)
            if not category.slug:
                category.slug = slugify(category_name, allow_unicode=True)
                category.save(update_fields=['slug'])
            category_map[category_name] = category

        keyword_rules = {
            'موبایل': ['iphone', 'galaxy', 'samsung', 'xiaomi', 'redmi', 'phone', 'mobile'],
            'تبلت': ['ipad', 'tablet', 'tab'],
            'لپ تاپ': ['laptop', 'macbook', 'notebook'],
            'ساعت هوشمند': ['watch', 'smart watch', 'smartwatch'],
            'هدفون': ['headphone', 'earbud', 'airpods', 'buds', 'هدست', 'هدفون'],
            'اسپیکر': ['speaker', 'اسپیکر'],
            'لوازم جانبی': ['charger', 'case', 'cover', 'cable', 'adapter', 'power bank'],
        }

        assigned_count = 0
        for product in Product.objects.all():
            name = (product.name or '').lower()
            selected_category = category_map['سایر']

            for category_name, keywords in keyword_rules.items():
                if any(keyword in name for keyword in keywords):
                    selected_category = category_map[category_name]
                    break

            if product.category_id != selected_category.id:
                product.category = selected_category
                product.save(update_fields=['category'])
                assigned_count += 1

        self.stdout.write(self.style.SUCCESS('Categories ensured successfully.'))
        self.stdout.write(self.style.SUCCESS(f'Products reassigned: {assigned_count}'))
