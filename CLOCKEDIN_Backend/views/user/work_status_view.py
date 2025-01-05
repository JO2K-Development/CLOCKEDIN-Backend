from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from CLOCKEDIN_Backend.models import CurrentWorkCycle, WorkCycle
from CLOCKEDIN_Backend.models.work_cycle import WorkCycleActionType
from CLOCKEDIN_Backend.permissions import IsEmployee


class WorkStatusViewSet(ViewSet):
    permission_classes = [IsEmployee]

    @action(detail=False, methods=["post"])
    @transaction.atomic
    def toggle(self, request):
        user = request.user
        current_cycle = CurrentWorkCycle.objects.filter(employee=user).first()

        if current_cycle:
            self._end_work_session(user, current_cycle)
            return Response({"message": "Work session ended and saved."}, status=status.HTTP_200_OK)
        else:
            self._start_work_session(user)
            return Response({"message": "Work session started."}, status=status.HTTP_201_CREATED)

    def _start_work_session(self, user):
        CurrentWorkCycle.objects.create(
            employee=user,
            company=user.company,
            start_time=timezone.now(),
            start_method=WorkCycleActionType.APP,
        )

    def _end_work_session(self, user, current_cycle):
        WorkCycle.objects.create(
            employee=user,
            company=current_cycle.company,
            start_time=current_cycle.start_time,
            end_time=timezone.now(),
            start_method=current_cycle.start_method,
            end_method=WorkCycleActionType.APP,
        )
        current_cycle.delete()
