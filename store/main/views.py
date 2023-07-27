from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from .models import Store, StoreStatusLog
from .serializers import StoreSerializer
from requests import Response

def trigger_report(store):
    # store_id, 
    # uptime_last_hour(in minutes), 
    # uptime_last_day(in hours), 
    # update_last_week(in hours), 
    # downtime_last_hour(in minutes), 
    # downtime_last_day(in hours), 
    # downtime_last_week(in hours) 
    store_id = store.id 
    store_status_logs_utc = store.status_logs.all()
    



class StoreViewSet(ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

    @action(detail=True, methods=['GET'])
    def trigger_report(self, request):
        store = self.get_object()
        report_id = trigger_report(store)
        return Response.OK({"report_id": report_id})
