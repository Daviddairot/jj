from django.contrib import admin
from .models import CalculationAttempt

@admin.register(CalculationAttempt)
class CalculationAttemptAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'p', 'h')
    list_filter = ('timestamp',)
