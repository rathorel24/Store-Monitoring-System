from django.db import models

class Store(models.Model):
    store_id = models.CharField(max_length=50, primary_key=True)
    timezone_str = models.CharField(max_length=50,null=True,blank=True)

    def __str__(self):
        return self.store_id

class Day(models.IntegerChoices):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

class StoreTiming(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="timings")
    day = models.IntegerField(choices=Day.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.store.store_id} - {self.day} - {self.start_time} - {self.end_time}"
    
class StoreStatus(models.IntegerChoices):
    INACTIVE = 0
    ACTIVE = 1


class StoreStatusLog(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="status_logs")
    status = models.IntegerField(choices=StoreStatus.choices)
    timestamp = models.DateTimeField(verbose_name="Time Stamp in UTC",null=True,blank=True)

    def get_local_timestamp(self):
        return self.timestamp.astimezone(self.store.timezone_str)
    
    def __str__(self):
        return f"{self.store.store_id} - {self.status} - {self.timestamp}"


class ReportStatus(models.IntegerChoices):
    PENDING = 0
    COMPLETED = 1

class StoreReport(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="reports",null=True,blank=True)
    status = models.IntegerField(choices=ReportStatus.choices)
    report_url = models.FileField(upload_to="reports",null=True,blank=True)