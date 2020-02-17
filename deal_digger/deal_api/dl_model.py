import warnings
warnings.simplefilter('ignore')


from deeppavlov import build_model, configs


class AnswerModel:
    def __init__(self):
        self._model = None

    @property
    def model(self):
        if self._model is None:
            self._model = build_model(configs.squad.squad_ru_rubert_infer)
        return self._model

    def answer(self, text, question):
        return self.model([text], [question])[0][0]
