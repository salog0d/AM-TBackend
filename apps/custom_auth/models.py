from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


# Create your models here.
class CustomUser(AbstractUser):
    """
    CustomUser Model
    This model extends Django's built-in AbstractUser to provide additional fields and functionality
    specific to the application's requirements. It introduces roles, disciplines, and other custom
    attributes for user management.
    
    Attributes:
        ROLE_CHOICES (tuple): Defines the possible roles a user can have:
            - 'athlete': Represents an athlete.
            - 'coach': Represents a coach.
            - 'admin': Represents an administrator.
        DISCIPLINE_CHOICES (tuple): Defines the possible disciplines a user can be associated with,
        such as 'Athletics', 'Soccer', 'Basketball', etc.
        profile_picture (ImageField): Optional field to store the user's profile picture.
        role (CharField): Specifies the user's role, with a default value of 'athlete'.
        name (CharField): Optional field to store the user's full name.
        discipline (CharField): Specifies the user's discipline, chosen from DISCIPLINE_CHOICES.
        date_of_birth (DateField): Optional field to store the user's date of birth.
        phone_number (CharField): Optional field to store the user's phone number.
        email (EmailField): Stores the user's email address, which must be unique.
        coach (ForeignKey): A self-referential field to assign a coach to an athlete. Only users with
            the role 'coach' can be assigned as a coach. This field is optional and only applicable
            for users with the role 'athlete'.
    """
    
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
    
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='admin')
    name = models.CharField(max_length=100, blank=True)
    username = models.CharField(max_length=150, unique=True)
    discipline = models.CharField(max_length=100, choices=DISCIPLINE_CHOICES)
    date_of_birth = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True)
    coach = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='athletes',
        limit_choices_to={'role': 'coach'}
    )

    def clean(self):
        """
        Validates the model's data before saving. Ensures:
            - Athletes must have a coach assigned.
            - The assigned coach must have the role of 'coach'.
            - Only athletes can have a coach assigned.
        """
        # Solo aplicamos estas validaciones si no es una creación inicial
        if self.pk:  # Si existe una primary key, el objeto ya existe
            if self.role == 'athlete' and self.coach is None:
                raise ValidationError('Un atleta debe tener un coach asignado')
            
            if self.coach and self.coach.role != 'coach':
                raise ValidationError('El usuario asignado como coach debe tener el rol de coach')
            
            if self.role != 'athlete' and self.coach is not None:
                raise ValidationError('Solo los atletas pueden tener un coach asignado')
            
            if self.role == 'coach' and self.coach is not None:
                raise ValidationError('Un coach no puede tener asignado otro coach')

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to call the clean method before saving.
        """
        try:
            self.clean()
        except ValidationError as e:
            # Log or handle the error appropriately
            print(f"Validation error: {e}")
            raise
        super().save(*args, **kwargs)
    
    def is_athlete(self):
        """Returns True if the user's role is 'athlete'."""
        return self.role == 'athlete'
    
    def is_coach(self):
        """Returns True if the user's role is 'coach'."""
        return self.role == 'coach'
    
    def is_admin(self):
        """Returns True if the user's role is 'admin'."""
        return self.role == 'admin'
    
    def __str__(self):
        """Returns the user's name as the string representation of the object."""
        return self.name if self.name else self.username