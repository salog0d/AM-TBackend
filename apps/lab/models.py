from django.db import models
from apps.custom_auth.models import CustomUser

class Test(models.Model):
    """
    Represents a physical test type with associated metadata.
    Attributes:
        UNIT_CHOICES (tuple): A set of predefined unit options for measuring test results.
            - 'seconds': Measured in seconds.
            - 'minutes': Measured in minutes.
            - 'meters': Measured in meters.
            - 'centimeters': Measured in centimeters.
            - 'kilograms': Measured in kilograms.
            - 'repetitions': Measured in repetitions.
            - 'score': Measured as a score.
        CATEGORIES (tuple): A set of predefined categories for classifying the test.
            - 'strength': Tests related to strength.
            - 'endurance': Tests related to endurance.
            - 'speed': Tests related to speed.
            - 'flexibility': Tests related to flexibility.
            - 'agility': Tests related to agility.
            - 'balance': Tests related to balance.
            - 'coordination': Tests related to coordination.
        name (str): The name of the test (max length: 100 characters).
        category (str): The category of the test, chosen from `CATEGORIES`.
        description (str): A detailed description of the test.
        unit (str): The unit of measurement for the test result, chosen from `UNIT_CHOICES`.
        higher_is_better (bool): Indicates whether a higher value represents a better result.
            Defaults to True.
    Methods:
        __str__(): Returns the name of the test as its string representation.
    """

    UNIT_CHOICES = (
        ('seconds', 'Segundos'),
        ('minutes', 'Minutos'),
        ('meters', 'Metros'),
        ('centimeters', 'Centímetros'),
        ('kilograms', 'Kilogramos'),
        ('repetitions', 'Repeticiones'),
        ('score', 'Puntuación'),
    )

    CATEGORIES = (
        ('strength', 'Fuerza'),
        ('endurance', 'Resistencia'),
        ('speed', 'Velocidad'),
        ('flexibility', 'Flexibilidad'),
        ('agility', 'Agilidad'),
        ('balance', 'Equilibrio'),
        ('coordination', 'Coordinación'),
    )
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=CATEGORIES)
    description = models.TextField()
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES)
    higher_is_better = models.BooleanField(default=True, help_text="¿Un valor más alto representa un mejor resultado?")
    
    def __str__(self):
        return self.name

class EvaluationSession(models.Model):
    """
    EvaluationSession Model
    Represents a physical evaluation session conducted by an evaluator for a specific discipline.
    Attributes:
        date (DateField): The date when the evaluation session takes place.
        location (CharField): The location where the evaluation session is conducted. Maximum length is 100 characters.
        discipline (CharField): The discipline being evaluated. Choices are defined in `CustomUser.DISCIPLINE_CHOICES`.
        evaluator (ForeignKey): A reference to the user (of type `CustomUser`) who conducts the evaluation. 
            Limited to users with the role 'admin'. Deleting the evaluator will cascade and delete related sessions.
        notes (TextField): Optional field for additional notes or observations about the session.
    Methods:
        __str__(): Returns a string representation of the evaluation session in the format 
            "Evaluación <discipline> - <date>".
    """

    date = models.DateField()
    location = models.CharField(max_length=100)
    discipline = models.CharField(max_length=100, choices=CustomUser.DISCIPLINE_CHOICES)
    evaluator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='conducted_evaluations', 
                                 limit_choices_to={'role': 'admin'})
    notes = models.TextField(blank=True)
    #falta agregar el campo de tests
    
    def __str__(self):
        return f"Evaluación {self.discipline} - {self.date}"

class TestResult(models.Model):
    """
    TestResult model represents the outcome of a specific physical test conducted for an athlete.
    It links an athlete, a test, and an evaluation session, while storing the test result value,
    optional notes, and the date when the result was recorded.
    Attributes:
        athlete (ForeignKey): A reference to the athlete (CustomUser) who took the test.
            Limited to users with the role 'athlete'.
        test (ForeignKey): A reference to the specific test (Test) being recorded.
        session (ForeignKey): A reference to the evaluation session (EvaluationSession) 
            during which the test was conducted.
        numeric_value (DecimalField): The numeric result of the test, with up to 10 digits 
            and 2 decimal places.
        notes (TextField): Optional additional information or observations about the test result.
        date_recorded (DateTimeField): The timestamp when the test result was recorded, 
            automatically set to the current date and time.
    Meta:
        unique_together: Ensures that a combination of athlete, test, and session is unique, 
            preventing duplicate entries for the same test result.
    Methods:
        __str__: Returns a human-readable string representation of the test result, 
            including the athlete's name, test name, numeric value, and test unit.
    """

    athlete = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='test_results',
                               limit_choices_to={'role': 'athlete'})
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='results')
    session = models.ForeignKey(EvaluationSession, on_delete=models.CASCADE, related_name='results')
    numeric_value = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)
    date_recorded = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.athlete.name} - {self.test.name}: {self.numeric_value} {self.test.unit}"
    
    class Meta:
        unique_together = ('athlete', 'test', 'session')