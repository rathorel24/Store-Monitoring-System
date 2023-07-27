from django.contrib import admin
from .models import Store, StoreStatusLog, StoreTiming, StoreReport

# Register your models here.
@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('store_id', 'timezone_str')
    list_filter = ('timezone_str',)
    search_fields = ('store_id',)

@admin.register(StoreTiming)
class StoreTimingAdmin(admin.ModelAdmin):
    list_display = ('store', 'day', 'start_time', 'end_time')
    raw_id_fields = ('store',)
    list_filter = ('day',)
    search_fields = ('store_id',)

@admin.register(StoreStatusLog)
class StoreStatusLogAdmin(admin.ModelAdmin):
    list_display = ('store', 'status', 'timestamp')
    raw_id_fields = ('store',)
    list_filter = ('status',)
    search_fields = ('store_id',)

@admin.register(StoreReport)
class StoreReportAdmin(admin.ModelAdmin):
    list_display = ('store', 'status', 'report_url')
    raw_id_fields = ('store',)
    list_filter = ('status',)
    search_fields = ('store_id',)