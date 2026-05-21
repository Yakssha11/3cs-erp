from django.db import models

class EggProduction(models.Model):
    flock_id        = models.IntegerField()
    building        = models.CharField(max_length=50)
    collection_date = models.DateField()
    total_eggs      = models.IntegerField()
    good_eggs       = models.IntegerField()
    cracked_eggs    = models.IntegerField()
    hen_count       = models.IntegerField()
    production_rate = models.DecimalField(max_digits=5, decimal_places=2)
    price_per_egg   = models.DecimalField(max_digits=10, decimal_places=2)
    total_revenue   = models.DecimalField(max_digits=10, decimal_places=2)
    recorded_by     = models.CharField(max_length=100)
    remarks         = models.CharField(max_length=255, blank=True)
    Date            = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'egg_production'
        ordering = ['-collection_date']

    def __str__(self):
        return f"{self.building} — {self.collection_date} — {self.good_eggs} eggs"
