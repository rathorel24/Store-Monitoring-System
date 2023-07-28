from rest_framework.viewsets import GenericViewSet ,ModelViewSet
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action
from .models import Store, StoreStatusLog, StoreStatus, StoreReport, ReportStatus
from .serializers import ReportSerializer
from rest_framework.response import Response
from main.helper import generate_report_data , generate_csv_file, trigger_report_combined
from django.conf import settings

class StoreViewSet(ModelViewSet):
    queryset = Store.objects.all()

    @action(detail=True, methods=['GET'],)
    def trigger_report(self, request,pk):
        store = self.get_object()
        report = StoreReport.objects.create(store=store, status=ReportStatus.PENDING)
        csv_data = []
        data = generate_report_data(store)
        csv_data.append(data)
        generate_csv_file(report, csv_data)
        return Response(status=200, data={"report_id": report.id})

    @action(detail=False, methods=['POST'])
    def get_report(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        report_id = serializer.validated_data.get("report_id")
        report = get_object_or_404(StoreReport, id=report_id)
        if report.status == ReportStatus.COMPLETED:
            report_url = settings.MEDIA_ROOT + "/" + report.report_url.name
            return Response(status=200,data={"report_url": report_url,"status": "Complete"})
        else:
            return Response(status=200, data={"status": "Running"})   
    
    def get_serializer_class(self):
        if self.action == 'get_report':
            return ReportSerializer
        return self.serializer_class