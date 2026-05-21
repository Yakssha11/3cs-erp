from django.db import models

class Finance(models.Model):
    expense_date = models.DateField()
    nature       = models.CharField(max_length=50)
    building     = models.CharField(max_length=50)
    amount       = models.DecimalField(max_digits=10, decimal_places=2)
    remarks      = models.CharField(max_length=255, blank=True)
    person       = models.CharField(max_length=100)
    Date         = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'finance'

    def __str__(self):
        return f"{self.expense_date} - {self.nature} - ₱{self.amount}"