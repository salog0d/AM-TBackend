from django.db import models
from custom_auth.models import CustomUser

class TestCategory(models.Model):
    """Categoría de test físico (ej: resistencia, fuerza, velocidad)"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Test Categories"

class PhysicalTest(models.Model):
    """Definición de un tipo de test físico"""
    UNIT_CHOICES = (
        ('seconds', 'Segundos'),
        ('minutes', 'Minutos'),
        ('meters', 'Metros'),
        ('centimeters', 'Centímetros'),
        ('kilograms', 'Kilogramos'),
        ('repetitions', 'Repeticiones'),
        ('score', 'Puntuación'),
    )
    
    name = models.CharField(max_length=100)
    category = models.ForeignKey(TestCategory, on_delete=models.CASCADE, related_name='tests')
    description = models.TextField()
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES)
    higher_is_better = models.BooleanField(default=True, help_text="¿Un valor más alto representa un mejor resultado?")
    
    def __str__(self):
        return self.name

class EvaluationSession(models.Model):
    """Sesión de evaluación física"""
    date = models.DateField()
    location = models.CharField(max_length=100)
    discipline = models.CharField(max_length=100, choices=CustomUser.DISCIPLINE_CHOICES)
    evaluator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='conducted_evaluations', 
                                 limit_choices_to={'role': 'coach'})
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Evaluación {self.discipline} - {self.date}"

class TestResult(models.Model):
    """Resultado de un test físico específico para un atleta"""
    athlete = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='test_results',
                               limit_choices_to={'role': 'athlete'})
    test = models.ForeignKey(PhysicalTest, on_delete=models.CASCADE, related_name='results')
    session = models.ForeignKey(EvaluationSession, on_delete=models.CASCADE, related_name='results')
    numeric_value = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)
    date_recorded = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.athlete.name} - {self.test.name}: {self.numeric_value} {self.test.unit}"
    
    class Meta:
        unique_together = ('athlete', 'test', 'session')