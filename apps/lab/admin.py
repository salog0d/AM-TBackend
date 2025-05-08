from django.contrib import admin
from apps.lab.models import Test, EvaluationSession, TestResult

# Register your models here.
admin.site.register(Test)
admin.site.register(EvaluationSession)
admin.site.register(TestResult) 