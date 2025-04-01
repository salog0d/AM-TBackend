from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('athlete', 'Athlete'),
        ('coach', 'Coach'),
        ('admin', 'Admin'),
    )
    DISCIPLINE_CHOICES = (
        ('athletics', 'Athletics'),
        ('soccer', 'Soccer'),
        ('volleyball', 'Volleyball'),
        ('basketball', 'Basketball'),
        ('tennis', 'Tennis'),
        ('rugby', 'Rugby'),
        ('american_football', 'American Football'),
        ('swimming', 'Swimming'),
        ('taekwondo', 'Taekwondo'),
        ('flag_football', 'Flag Football'),
        ('futsal', 'Futsal'),
        ('beach_volleyball', 'Beach Volleyball'),
        ('table_tennis', 'Table Tennis'),
        ('martial_arts', 'Martial Arts'),
        ('boxing', 'Boxing'),
        ('physical_conditioning', 'Physical Conditioning'),
        ('gap_training', 'GAP (Glutes, Abs, Legs)'),
        ('investigation', 'Investigation')
    )
    """
    Custom user model that extends the default Django User model.
    """
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='athlete')
    name = models.CharField(max_length=100, blank=True)
    discipline = models.CharField(max_length=100, choices=DISCIPLINE_CHOICES)
    date_of_birth = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField(unique=True)

    def is_athlete(self):
        return self.role == 'athlete'
    
    def is_coach(self):
        return self.role == 'coach'
    
    def is_admin(self):
        return self.role == 'admin'

    def __str__(self):
        return self.name