from django.db import models

class LayingFlock(models.Model):
    batch_name    = models.CharField(max_length=100)
    building      = models.CharField(max_length=50)
    start_count   = models.IntegerField()
    current_count = models.IntegerField()
    date_placed   = models.DateField()
    supplier      = models.CharField(max_length=100, blank=True)
    status        = models.CharField(max_length=20)
    notes         = models.TextField(blank=True)
    Date          = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'laying_flocks'

    def __str__(self):
        return f"{self.batch_name} — {self.building}"

class LayingMortality(models.Model):
    flock         = models.ForeignKey(LayingFlock, on_delete=models.CASCADE)
    building      = models.CharField(max_length=50)
    death_date    = models.DateField()
    count         = models.IntegerField()
    cause         = models.CharField(max_length=100, blank=True)
    recorded_by   = models.CharField(max_length=100)
    remarks       = models.CharField(max_length=255, blank=True)
    Date          = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'laying_mortality'

    def __str__(self):
        return f"{self.flock.batch_name} — {self.death_date} — {self.count} deaths"