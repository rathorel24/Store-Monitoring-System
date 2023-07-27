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
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    day = models.IntegerField(choices=Day.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.store.store_id} - {self.day} - {self.start_time} - {self.end_time}"
    
class StoreStatus(models.IntegerChoices):
    INACTIVE = 0
    ACTIVE = 1


class StoreStatusLog(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    status = models.IntegerField(choices=StoreStatus.choices)
    timestamp = models.DateTimeField(verbose_name="Time Stamp in UTC",null=True,blank=True)

    def __str__(self):
        return f"{self.store.store_id} - {self.status} - {self.timestamp}"