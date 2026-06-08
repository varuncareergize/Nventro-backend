from django.db import models

class Vehicle(models.Model):

    STATUS_CHOICES = [
        ('READY', 'Ready'),
        ('REPAIR', 'In Repair'),
        ('OVERDUE', 'Overdue'),
    ]

    vehicle_name = models.CharField(max_length=100)
    vehicle_code = models.CharField(max_length=50, unique=True)
    plate_number = models.CharField(max_length=30)
    vehicle_image = models.ImageField(upload_to='vehicles/', blank=True, null=True)

    vehicle_type = models.CharField(max_length=50)
    month = models.CharField(max_length=7, blank=True, null=True)  # Format: YYYY-MM
    monthly_start_mileage = models.PositiveIntegerField(default=0)
    monthly_end_mileage = models.PositiveIntegerField(default=0)
    kt_number = models.CharField(max_length=50, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    fuel_level = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    oil_level = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    battery_health = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=100
    )

    assigned_driver = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    next_service_date = models.DateField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='READY'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.vehicle_name