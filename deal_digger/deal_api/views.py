from rest_framework import views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from deal_api.dl_model import AnswerModel
model = AnswerModel()


class ExtractEntitiesApi(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        text = request.data['text']
        category = request.data['category']

        return Response({'entities': []})
