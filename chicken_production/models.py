from django.db import models
from flock.models import Flock

class ChickenProduction(models.Model):
    flock           = models.ForeignKey(Flock, on_delete=models.SET_NULL, null=True, db_constraint=False)
    growing_house   = models.CharField(max_length=100)
    harvest_date    = models.DateField()
    total_harvested = models.PositiveIntegerField()
    good_chickens   = models.PositiveIntegerField()
    rejected        = models.PositiveIntegerField()
    flock_count     = models.PositiveIntegerField()
    harvest_rate    = models.DecimalField(max_digits=5, decimal_places=2)
    price_per_chicken = models.DecimalField(max_digits=10, decimal_places=2)
    total_revenue   = models.DecimalField(max_digits=12, decimal_places=2)
    recorded_by     = models.CharField(max_length=100)
    remarks         = models.CharField(max_length=255, blank=True)
    Date            = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'chicken_production'
        ordering = ['-harvest_date']

    def __str__(self):
        return f"{self.growing_house} — {self.harvest_date} — {self.total_harvested} chickens"