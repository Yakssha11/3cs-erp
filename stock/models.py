from django.db import models

class Stock(models.Model):
    item_id      = models.CharField(max_length=10, unique=True)
    name         = models.CharField(max_length=100)
    price        = models.DecimalField(max_digits=10, decimal_places=2)
    quantity     = models.IntegerField()
    category     = models.CharField(max_length=50)
    growing_house = models.CharField(max_length=50, blank=True)
    unit         = models.CharField(max_length=20, blank=True)
    date         = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'stocks'

    def __str__(self):
        return f"{self.item_id} - {self.name}"