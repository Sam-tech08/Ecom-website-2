from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Customer(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.IntegerField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.firstname}{self.lastname}'


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(max_length=10000, default='')
    image = models.ImageField(upload_to='upload/product/')
    is_sale = models.BooleanField(default=False)
    sale_value = models.DecimalField(default=0, max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name



