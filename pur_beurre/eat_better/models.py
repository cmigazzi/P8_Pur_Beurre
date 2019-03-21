from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Nutriments(models.Model):
    fat = models.DecimalField(max_digits=4, decimal_places=1)
    sugars = models.DecimalField(max_digits=4, decimal_places=1)
    saturated_fat = models.DecimalField(max_digits=4, decimal_places=1)
    salt = models.DecimalField(max_digits=6, decimal_places=3)


class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=150)
    nutriscore = models.CharField(max_length=1)
    url = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    categories = models.ManyToManyField(Category, through="Hierarchy")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    nutriments = models.ForeignKey(Nutriments, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name


class Hierarchy(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    level = models.IntegerField()

    def __str__(self):
        return f"{self.product}, {self.category}, {self.level}"

    class Meta:
        ordering = ("-level",)
