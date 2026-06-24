from django.db import models
from fleet.models import Vehicle


class VehicleService(models.Model):

    SERVICE_TYPES = [
        ('ROUTINE', 'Routine Maintenance'),
        ('REPAIR', 'Repair'),
        ('BREAKDOWN', 'Breakdown'),
        ('ACCIDENT', 'Accident'),
        ('INSPECTION', 'Inspection'),
    ]

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='services'
    )

    service_date = models.DateField()

    odometer_reading = models.PositiveIntegerField()

    service_type = models.CharField(
        max_length=20,
        choices=SERVICE_TYPES
    )

    estimated_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    actual_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    work_performed = models.TextField(
        blank=True,
        null=True
    )

    breakdown_details = models.TextField(
        blank=True,
        null=True
    )

    accident_details = models.TextField(
        blank=True,
        null=True
    )

    workshop_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    mechanic_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    next_service_due_km = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    next_service_date = models.DateField(
        blank=True,
        null=True
    )

    vehicle_downtime_days = models.PositiveIntegerField(
        default=0
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.vehicle.vehicle_name} - {self.service_date}"
# Create your models here.

class ServiceItem(models.Model):

    name = models.CharField(
        max_length=150,
        unique=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

class VehicleServiceItem(models.Model):

    service = models.ForeignKey(
        VehicleService,
        on_delete=models.CASCADE,
        related_name='service_items'
    )

    item = models.ForeignKey(
        ServiceItem,
        on_delete=models.CASCADE
    )

    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.service.id} - {self.item.name}"


class ServiceDocument(models.Model):

    service = models.ForeignKey(
        VehicleService,
        on_delete=models.CASCADE,
        related_name='documents'
    )

    file = models.FileField(
        upload_to='service_documents/'
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Document {self.id}"

class Part(models.Model):

    part_name = models.CharField(max_length=200)

    part_number = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return self.part_name

class ServicePart(models.Model):

    service = models.ForeignKey(
        VehicleService,
        on_delete=models.CASCADE,
        related_name='parts_used'
    )

    part = models.ForeignKey(
        Part,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)