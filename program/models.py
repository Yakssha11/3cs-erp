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

class ProgramStep(models.Model):
    METHOD_CHOICES = [
        ('Drinking Water', 'Drinking Water'),
        ('Eye Drop',       'Eye Drop'),
        ('Injection',      'Injection'),
        ('Spray',          'Spray'),
    ]
    UNIT_CHOICES = [
        ('ml',     'ml'),
        ('g',      'g'),
        ('L',      'L'),
        ('tablet', 'tablet'),
        ('drop',   'drop'),
    ]
    PER_CHOICES = [
        ('chick', 'chick'),
        ('liter', 'liter'),
        ('kg',    'kg'),
    ]
    program     = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='steps')
    week        = models.PositiveIntegerField()
    day         = models.PositiveIntegerField()
    medicine    = models.CharField(max_length=100)  # must match stock item_name
    dose_amount = models.DecimalField(max_digits=8, decimal_places=2)
    dose_unit   = models.CharField(max_length=10, choices=UNIT_CHOICES)
    dose_per    = models.CharField(max_length=10, choices=PER_CHOICES)
    method      = models.CharField(max_length=20, choices=METHOD_CHOICES)
    remarks     = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['week', 'day']

    def __str__(self):
        return f"Week {self.week} Day {self.day} - {self.medicine}"