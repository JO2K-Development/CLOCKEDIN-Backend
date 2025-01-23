from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from CLOCKEDIN_Backend.models import WorkCycle
from CLOCKEDIN_Backend.permissions import IsManager
from CLOCKEDIN_Backend.serializers.work_cycle_serializer import WorkCycleSerializer


class WorkCyclesViewSet(ModelViewSet):
    queryset = WorkCycle.objects.all()
    serializer_class = WorkCycleSerializer
    permission_classes = [IsManager]

    def perform_create(self, serializer):
        start_time = serializer.validated_data.get("start_time")
        end_time = serializer.validated_data.get("end_time")
        if start_time >= end_time:
            raise serializers.ValidationError("Start time must be before end time.")
        serializer.save()

    def perform_update(self, serializer):
        start_time = serializer.validated_data.get("start_time")
        end_time = serializer.validated_data.get("end_time")
        if start_time >= end_time:
            raise serializers.ValidationError("Start time must be before end time.")
        serializer.save()

    @action(detail=True, methods=["delete"], url_path="delete-cycle")
    def delete_cycle(self, request, pk=None):
        work_cycle = self.get_object()
        work_cycle.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
