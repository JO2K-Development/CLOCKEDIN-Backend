from rest_framework import serializers

from CLOCKEDIN_Backend.models import WorkCycle


class WorkCycleSerializer(serializers.ModelSerializer):
    duration = serializers.DurationField(read_only=True)

    class Meta:
        model = WorkCycle
        fields = [
            "id",
            "start_time",
            "end_time",
            "duration",
            "status",
        ]
