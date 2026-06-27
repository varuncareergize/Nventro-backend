from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    image = models.ImageField(upload_to='companies/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Vehicle(models.Model):

    STATUS_CHOICES = [
        ('READY', 'Ready'),
        ('REPAIR', 'In Repair'),
        ('OVERDUE', 'Overdue'),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='vehicles',
        null=True,
        blank=True,
        default=1
    )

    si_no = models.PositiveIntegerField(blank=True, null=True)
    vehicle_name = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=50, blank=True)
    plate_number = models.CharField(max_length=30, blank=True)
    vehicle_using_by = models.CharField(max_length=100, blank=True, null=True)
    service_km = models.PositiveIntegerField(default=0)
    current_km = models.PositiveIntegerField(default=0)
    balance_service_km = models.PositiveIntegerField(default=0)
    model_year = models.CharField(max_length=100, blank=True, null=True)
    ards_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='READY'
    )
    insurance_upto = models.DateField(blank=True, null=True)
    registration_upto = models.DateField(blank=True, null=True)
    vehicle_image = models.ImageField(upload_to='vehicles/', blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.vehicle_name