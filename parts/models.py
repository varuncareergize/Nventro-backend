from django.db import models


class Part(models.Model):

    STATUS_CHOICES = [
        ('IN_STOCK', 'In Stock'),
        ('LOW_STOCK', 'Low Stock'),
        ('OUT_OF_STOCK', 'Out Of Stock'),
    ]

    part_number = models.CharField(max_length=100, unique=True)
    part_name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)

    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='parts/', blank=True, null=True)

    stock_quantity = models.PositiveIntegerField(default=0)
    minimum_stock = models.PositiveIntegerField(default=5)

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='IN_STOCK'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.stock_quantity == 0:
            self.status = 'OUT_OF_STOCK'
        elif self.stock_quantity <= self.minimum_stock:
            self.status = 'LOW_STOCK'
        else:
            self.status = 'IN_STOCK'

        super().save(*args, **kwargs)

    def __str__(self):
        return self.part_name

# Create your models here.

class PartUsage(models.Model):

    part = models.ForeignKey(
        Part,
        on_delete=models.CASCADE,
        related_name='usages'
    )

    vehicle = models.ForeignKey(
        'fleet.Vehicle',
        on_delete=models.CASCADE,
        related_name='part_usages'
    )

    quantity_used = models.PositiveIntegerField()

    technician_name = models.CharField(max_length=100)

    remarks = models.TextField(
        blank=True,
        null=True
    )

    used_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.part.part_name} - {self.vehicle.vehicle_name}"
    

class PartTransaction(models.Model):

    TRANSACTION_TYPES = [
        ('PURCHASE', 'Purchase'),
        ('USED', 'Used'),
        ('ADJUSTMENT', 'Adjustment'),
    ]

    part = models.ForeignKey(
        Part,
        on_delete=models.CASCADE,
        related_name='transactions'
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES
    )

    quantity = models.PositiveIntegerField()

    remarks = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.part.part_name} - {self.transaction_type}"