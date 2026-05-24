from django.db import models

class GrowingSale(models.Model):
    flock          = models.ForeignKey('flock.Flock', on_delete=models.SET_NULL, null=True, db_constraint=False)
    customer       = models.ForeignKey('master_data.Customer', on_delete=models.SET_NULL, null=True, blank=True, db_constraint=False)
    quantity       = models.PositiveIntegerField()
    price_per_head = models.DecimalField(max_digits=10, decimal_places=2)
    total_revenue  = models.DecimalField(max_digits=12, decimal_places=2)
    sale_date      = models.DateField()
    remarks        = models.CharField(max_length=255, blank=True)
    recorded_by    = models.CharField(max_length=100)
    Date           = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'growing_sales'
        ordering = ['-sale_date']

    def __str__(self):
        return f"Sale — {self.quantity} heads — ₱{self.total_revenue}"

class LayingSale(models.Model):
    building       = models.CharField(max_length=100)
    customer       = models.ForeignKey('master_data.Customer', on_delete=models.SET_NULL, null=True, blank=True, db_constraint=False)
    eggs_sold      = models.PositiveIntegerField()
    price_per_egg  = models.DecimalField(max_digits=8, decimal_places=2)
    total_revenue  = models.DecimalField(max_digits=12, decimal_places=2)
    sale_date      = models.DateField()
    remarks        = models.CharField(max_length=255, blank=True)
    recorded_by    = models.CharField(max_length=100)
    Date           = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'laying_sales'
        ordering = ['-sale_date']

    def __str__(self):
        return f"{self.building} — {self.eggs_sold} eggs — ₱{self.total_revenue}"