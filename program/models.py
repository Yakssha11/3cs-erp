from django.db import models

class Program(models.Model):
    TYPE_CHOICES = [
        ('Growing', 'Growing'),
        ('Laying',  'Laying'),
    ]
    name        = models.CharField(max_length=100)
    type        = models.CharField(max_length=10, choices=TYPE_CHOICES)
    description = models.TextField(blank=True)
    Date        = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.type})"


class ProgramBatch(models.Model):
    program      = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='batches')
    flock_id     = models.IntegerField()
    flock_type   = models.CharField(max_length=10)  # 'Growing' or 'Laying'
    date_started = models.DateField()
    notes        = models.CharField(max_length=255, blank=True)
    Date         = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_started']

    def __str__(self):
        return f"{self.program.name} — {self.flock_name}"

    @property
    def flock(self):
        if self.flock_type == 'Growing':
            from flock.models import Flock
            return Flock.objects.filter(pk=self.flock_id).first()
        else:
            from laying_flock.models import LayingFlock
            return LayingFlock.objects.filter(pk=self.flock_id).first()

    @property
    def population(self):
        f = self.flock
        return f.current_count if f else 0

    @property
    def flock_name(self):
        f = self.flock
        return f.batch_name if f else '—'

    @property
    def flock_house(self):
        f = self.flock
        if not f:
            return '—'
        return f.growing_house if self.flock_type == 'Growing' else f.building

    def step_date(self, week, day):
        from datetime import timedelta
        return self.date_started + timedelta(days=(week * 7) + day - 1)


class ProgramStep(models.Model):
    METHOD_CHOICES = [
        ('Drinking Water', 'Drinking Water'),
        ('Eye Drop',       'Eye Drop'),
        ('Injection',      'Injection'),
        ('Spray',          'Spray'),
    ]
    PER_CHOICES = [
        ('chick', 'chick'),
        ('liter', 'liter'),
        ('kg',    'kg'),
    ]

    program            = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='steps')
    cycle              = models.PositiveIntegerField(default=1)
    week               = models.PositiveIntegerField()
    day                = models.PositiveIntegerField()
    medicine           = models.CharField(max_length=10, blank=True)
    dose_amount        = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    dose_unit          = models.CharField(max_length=50, blank=True)
    dose_per           = models.CharField(max_length=10, choices=PER_CHOICES, blank=True)
    method             = models.CharField(max_length=20, choices=METHOD_CHOICES, blank=True)
    remarks            = models.CharField(max_length=255, blank=True)
    feed               = models.CharField(max_length=10, blank=True)
    feed_rate_per_bird = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    feed_unit          = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['cycle', 'week', 'day']

    def __str__(self):
        return f"Cycle {self.cycle} Week {self.week} Day {self.day} - {self.medicine}"

    @property
    def medicine_name(self):
        from master_data.models import Material
        if not self.medicine:
            return '—'
        m = Material.objects.filter(item_id=self.medicine).first()
        return m.name if m else self.medicine

    @property
    def feed_name(self):
        from master_data.models import Material
        if not self.feed:
            return '—'
        m = Material.objects.filter(item_id=self.feed).first()
        return m.name if m else self.feed