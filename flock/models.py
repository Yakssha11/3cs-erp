from django.db import models

class Flock(models.Model):
    batch_name    = models.CharField(max_length=100)
    growing_house = models.CharField(max_length=50)
    start_count   = models.IntegerField()
    current_count = models.IntegerField()
    date_placed   = models.DateField()
    supplier      = models.CharField(max_length=100, blank=True)
    status        = models.CharField(max_length=20)
    notes         = models.TextField(blank=True)
    Date          = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'flocks'

    def __str__(self):
        return f"{self.batch_name} - {self.growing_house}"

class Mortality(models.Model):
    flock         = models.ForeignKey(Flock, on_delete=models.CASCADE)
    growing_house = models.CharField(max_length=50)
    death_date    = models.DateField()
    count         = models.IntegerField()
    cause         = models.CharField(max_length=100, blank=True)
    recorded_by   = models.CharField(max_length=100)
    remarks       = models.CharField(max_length=255, blank=True)
    Date          = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'mortality'

    def __str__(self):
        return f"{self.flock.batch_name} - {self.death_date} - {self.count} deaths"
    
class FlockSnapshot(models.Model):
    flock             = models.ForeignKey(Flock, on_delete=models.CASCADE)
    batch_name        = models.CharField(max_length=100)
    growing_house     = models.CharField(max_length=50)
    week_number       = models.IntegerField()
    snapshot_date     = models.DateField()
    start_count       = models.IntegerField()
    deaths_this_week  = models.IntegerField()
    count_at_snapshot = models.IntegerField()
    Date              = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'flock_snapshots'

    def __str__(self):
        return f"{self.batch_name} — Week {self.week_number}"