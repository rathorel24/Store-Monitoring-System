from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from .models import Store, StoreStatusLog, StoreStatus, StoreReport, ReportStatus
from .serializers import StoreSerializer
from rest_framework.response import Response
from main.helper import generate_report

class StoreViewSet(ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

    @action(detail=True, methods=['GET'])
    def trigger_report(self, request):
        store = self.get_object()
        report = StoreReport.objects.create(store=store, status=ReportStatus.PENDING)
        generate_report(store,report)
        return Response.OK({"report_id": report.pk})

    @action(detail=False, methods=['GET'])
    def get_report(self, request):
        store = self.get_object()
        report = store.reports.last()
        if report:
            return Response.OK({"report_url": report.report_url.url})
        return Response.OK({"report_url": "No report found"})    