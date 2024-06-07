from django.contrib import admin
from .models import ScrapeJob

class ScrapeJobAdmin(admin.ModelAdmin):
    list_display = ('job_id', 'status', 'created_at', 'updated_at')
    readonly_fields = ('job_id', 'created_at', 'updated_at')
    search_fields = ('job_id', 'status')

admin.site.register(ScrapeJob, ScrapeJobAdmin)
