import django_filters
from CLOCKEDIN_Backend.models import WorkCycle

class WorkCycleFilter(django_filters.FilterSet):
    start_time__gte = django_filters.DateTimeFilter(field_name='start_time', lookup_expr='gte')
    start_time__lte = django_filters.DateTimeFilter(field_name='start_time', lookup_expr='lte')

    class Meta:
        model = WorkCycle
        fields = ['start_time__gte', 'start_time__lte', 'is_confirmed_stationary', 'start_method', 'end_method']