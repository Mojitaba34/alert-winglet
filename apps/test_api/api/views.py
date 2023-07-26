from rest_framework.views import APIView

from apps.core.exceptions import CustomAPIException
from apps.test_api.api.serializers import TestPostSerializer


class TestView(APIView):
    serializer = TestPostSerializer

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        raise CustomAPIException(error_message="I'm just testing man")
