from django.db import models

class Customer(models.Model):
    TYPE_CHOICES = [
        ('Wholesaler', 'Wholesaler'),
        ('Retailer',   'Retailer'),
        ('Walk-in',    'Walk-in'),
    ]
    name    = models.CharField(max_length=100)
    contact = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=255, blank=True)
    type    = models.CharField(max_length=20, choices=TYPE_CHOICES)
    Date    = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'customers'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.type})"

class Supplier(models.Model):
    TYPE_CHOICES = [
        ('Hatchery',          'Hatchery'),
        ('Feed Supplier',     'Feed Supplier'),
        ('Medicine Supplier', 'Medicine Supplier'),
        ('General',           'General'),
    ]
    name    = models.CharField(max_length=100)
    contact = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=255, blank=True)
    type    = models.CharField(max_length=20, choices=TYPE_CHOICES)
    Date    = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'suppliers'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.type})"
    
class Material(models.Model):
    item_id     = models.CharField(max_length=10, unique=True)
    name        = models.CharField(max_length=100)
    category    = models.CharField(max_length=100)
    unit        = models.CharField(max_length=50)
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)
    Date        = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'materials'
        ordering = ['name']

    def __str__(self):
        return f"{self.item_id} — {self.name}"