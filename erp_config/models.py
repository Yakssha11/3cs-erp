from django.db import models

class EggPriceConfig(models.Model):
    price_per_egg  = models.DecimalField(max_digits=10, decimal_places=2)
    effective_date = models.DateField()
    set_by         = models.CharField(max_length=100)
    Date           = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'egg_price_config'
        ordering = ['-effective_date']

    def __str__(self):
        return f"₱{self.price_per_egg} — {self.effective_date}"

# Create your models here.
