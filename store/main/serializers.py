from rest_framework import serializers 

class ReportSerializer(serializers.Serializer):
    report_id = serializers.IntegerField()