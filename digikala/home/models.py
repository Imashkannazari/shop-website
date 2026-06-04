from django.db import models
import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name, allow_unicode=True) or f'category-{self.pk or ""}'.strip('-')
            slug_candidate = base_slug
            counter = 1
            while Category.objects.filter(slug=slug_candidate).exclude(pk=self.pk).exists():
                counter += 1
                slug_candidate = f'{base_slug}-{counter}'
            self.slug = slug_candidate
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)


    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Product (models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, default='',blank=True , null=True)
    price = models.DecimalField(default=0, decimal_places=0, max_digits=12)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    picture = models.ImageField(upload_to = 'upload/product/')
    star = models.IntegerField(default=0, validators = [MaxValueValidator(5),MinValueValidator(0)])
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=0, max_digits=12)

    def __str__(self):
        return self.name


class Order (models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=400 ,default='', blank=False)
    phone = models.CharField(max_length=20, blank=True)
    date = models.DateField(default=datetime.date.today)
    status = models.BooleanField(default=False)


    def __str__(self):
        return self.product