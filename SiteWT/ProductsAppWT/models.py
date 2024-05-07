from django.db import models

# Create your models here.
class Product(models.Model):
    def __str__(self):
        return self.name

    ticker = models.CharField(max_length=100)
    name = models.CharField(max_length=100)


class Historical(models.Model):
    def __str__(self):
        return self.ticker_id

    ticker_id = models.IntegerField()
    timestamp = models.CharField(max_length=100)
    open= models.DecimalField(max_digits=10, decimal_places=2)
    high= models.DecimalField(max_digits=10, decimal_places=2)
    low= models.DecimalField(max_digits=10, decimal_places=2)
    close= models.DecimalField(max_digits=10, decimal_places=2)