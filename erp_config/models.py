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

class Building(models.Model):
    TYPE_CHOICES = [
        ('Growing', 'Growing'),
        ('Laying',  'Laying'),
        ('General', 'General'),
    ]
    name      = models.CharField(max_length=100)
    type      = models.CharField(max_length=10, choices=TYPE_CHOICES)
    is_active = models.BooleanField(default=True)
    Date      = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'config_buildings'
        ordering = ['type', 'name']

    def __str__(self):
        return f"{self.name} ({self.type})"

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    Date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'config_categories'
        ordering = ['name']

    def __str__(self):
        return self.name

class Unit(models.Model):
    name = models.CharField(max_length=50, unique=True)
    Date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'config_units'
        ordering = ['name']

    def __str__(self):
        return self.name

class Cause(models.Model):
    name = models.CharField(max_length=100, unique=True)
    Date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'config_causes'
        ordering = ['name']

    def __str__(self):
        return self.name

class SalesTarget(models.Model):
    TYPE_CHOICES = [
        ('Growing', 'Growing'),
        ('Laying',  'Laying'),
    ]
    building       = models.CharField(max_length=100, blank=True)
    type           = models.CharField(max_length=10, choices=TYPE_CHOICES)
    target_revenue = models.DecimalField(max_digits=12, decimal_places=2)
    period_start   = models.DateField()
    period_end     = models.DateField()
    set_by         = models.CharField(max_length=100)
    Date           = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'config_sales_targets'
        ordering = ['-period_start', 'type', 'building']

    def __str__(self):
        if self.type == 'Growing':
            return f"Growing — ₱{self.target_revenue} ({self.period_start} to {self.period_end})"
        return f"{self.building} — ₱{self.target_revenue} ({self.period_start} to {self.period_end})"

class ChickenPriceConfig(models.Model):
    price_chicken  = models.DecimalField(max_digits=10, decimal_places=2)
    effective_date = models.DateField()
    set_by         = models.CharField(max_length=100)
    Date           = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'chicken_price_config'
        ordering = ['-effective_date']

    def __str__(self):
        return f"₱{self.price_chicken} — {self.effective_date}"