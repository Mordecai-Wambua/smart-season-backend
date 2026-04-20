from django.contrib import admin
from .models import Field, FieldUpdate

class FieldUpdateInline(admin.TabularInline):
    model = FieldUpdate
    extra = 1

@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'crop_type', 'stage', 'status', 'agent', 'planting_date')
    list_filter = ('stage', 'crop_type')
    search_fields = ('name', 'crop_type')
    inlines = [FieldUpdateInline]

@admin.register(FieldUpdate)
class FieldUpdateAdmin(admin.ModelAdmin):
    list_display = ('field', 'agent', 'is_issue', 'created_at')
    list_filter = ('is_issue', 'created_at')