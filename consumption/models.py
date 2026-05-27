from django.db import models
from stock.models import Stock

class Consumption(models.Model):
    growing_house = models.CharField(max_length=50)
    category      = models.CharField(max_length=50)
    item_id       = models.CharField(max_length=10)
    item_name     = models.CharField(max_length=100)
    quantity      = models.DecimalField(max_digits=10, decimal_places=2)
    unit          = models.CharField(max_length=20)
    remarks       = models.CharField(max_length=255, blank=True)
    recorded_by   = models.CharField(max_length=100)
    date_consumed = models.DateField()
    Date          = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'consumption'

    def __str__(self):
        return f"{self.item_name} - {self.growing_house}"
    
class ConsumptionBatchDeduction(models.Model):
    consumption = models.ForeignKey(
        Consumption,
        on_delete=models.CASCADE,
        related_name='batch_deductions'
    )
    stock_batch        = models.ForeignKey(
        Stock,
        on_delete=models.SET_NULL,
        null=True
    )
    quantity_deducted  = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'consumption_batch_deductions'

    def __str__(self):
        return f"Consumption #{self.consumption_id} → Batch {self.stock_batch_id} → {self.quantity_deducted}"