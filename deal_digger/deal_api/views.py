from rest_framework import views
from rest_framework.response import Response

from deal_api.dl_model import AnswerModel
model = AnswerModel()


class ExtractEntitiesApi(views.APIView):
    def post(self, request):
        text = request.data['text']
        gen_dir = model.predict_executor(text)
        gen_dir_age = model.predict_executor_period(text)
        return Response({
            'entities': {
                'executor': gen_dir,
                'executor_period': gen_dir_age,
            }
        })
