from django.db import models

from api.account.models import *

from django.contrib.auth import get_user_model

user = get_user_model()

# Create your models here.

class Project(models.Model):
    STATUS_CHOICES = [
        ('Awarded', 'Awarded'),
        ('Live', 'Live'),
        ('Completed', 'Completed'),
        ('Pause', 'Pause'),
    ]
    name = models.CharField(max_length=255, unique=True)
    project_code = models.CharField(max_length=255, unique=True)
    client_name = models.CharField(max_length=255)
    end_client_name = models.CharField(max_length=255)
    project_manager = models.ForeignKey(UserRole, on_delete=models.CASCADE, null=True, blank=True)
    secondary_project_manager = models.ForeignKey(user, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    
    project_status = models.CharField(
        max_length=255,
        choices=STATUS_CHOICES,
        default='Awarded' 
    )

    id_received_date = models.DateField(null=True, blank=True)
    award_date = models.DateField()
    
    client_po = models.CharField(max_length=255, null=True, blank=True)
    max_number = models.IntegerField()  # Max N°
    client_allocation = models.IntegerField()  # Client Allocation
    client_project_number = models.CharField(max_length=255, null=True, blank=True)
    end_client_project_number = models.CharField(max_length=255, null=True, blank=True)
    
    PROGRAMMING_COMPLEXITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    programming_complexity = models.CharField(
        max_length=50,
        choices=PROGRAMMING_COMPLEXITY_CHOICES,
        default='Low',
    )
    
    CURRENCY_CHOICES = [
        ('USD', 'USD (US Dollar)'),
        ('EUR', 'EUR (Euro)'),
        ('INR', 'INR (Indian Rupee)'),
    ]
    currency_invoicing = models.CharField(
        max_length=50,
        choices=CURRENCY_CHOICES,
        default='USD',
    )
    
    SERVICES_CHOICES = [
        ('Consulting', 'Consulting'),
        ('Development', 'Development'),
        ('Support', 'Support'),
    ]
    services = models.CharField(max_length=255, choices=SERVICES_CHOICES)
    
    MANAGEMENT_FEE_CHOICES = [
        ('Percentage', 'Percentage'),
        ('Fixed', 'Fixed'),
    ]
    management_fee = models.CharField(max_length=50, choices=MANAGEMENT_FEE_CHOICES)
    
    description = models.TextField()
    
    def __str__(self):
        return self.name

