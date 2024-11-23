from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from CLOCKEDIN_Backend.models import WorkCycle
from CLOCKEDIN_Backend.permissions import IsEmployee
from CLOCKEDIN_Backend.serializers.work_cycle_serializer import WorkCycleSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class WorkCyclesViewSet(ReadOnlyModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsEmployee]
    serializer_class = WorkCycleSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['start_time', 'end_time', 'is_confirmed_stationary', 'start_method', 'end_method']

    def get_queryset(self):
        return WorkCycle.objects.filter(employee=self.request.user).order_by('-start_time')