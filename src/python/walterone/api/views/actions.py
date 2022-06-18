from rest_framework import views, status
from rest_framework.response import Response

from api.serializers.actions import ActionSerializer
from api.tasks.attack import attack_task

class ActionView(views.APIView):
    def post(self, request):
        serializer = ActionSerializer(data=request.data)
        if serializer.is_valid():
            attack_task.delay(request.data)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
