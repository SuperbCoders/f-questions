import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

import warnings
import pickle

warnings.simplefilter('ignore')

from deeppavlov import build_model, configs


class AnswerModel:
    def __init__(self):
        print('Loading model')
        self._model = build_model(configs.squad.squad_ru_rubert_infer)
        print('Model loaded')
        models_dir = os.path.join(os.path.dirname(__file__), 'models')

        with open(os.path.join(models_dir, 'trigram_encoder.pkl'), 'rb') as f:
            self.trigram_encoder = pickle.load(f)

        with open(os.path.join(models_dir, 'regressor.pkl'), 'rb') as f:
            self.regressor = pickle.load(f)

    @property
    def model(self):
        if self._model is None:
            self._model = build_model(configs.squad.squad_ru_rubert_infer)
        return self._model

    def answer(self, text, question):
        return self.model([text], [question])[0][0]

    def predict_executor(self, text):
        answers = [
            self.answer(text, q)
            for q in [
                'кто исполнительный орган',
                'кто является исполнительным орган',
                'единоличный исполнительный орган',
            ]
        ]
        enc_answers = self.trigram_encoder.transform(answers).toarray()
        predicts = self.regressor.predict(enc_answers)
        if any(predicts):
            return 'генеральный директор'
        return None

    def predict_executor_period(self, text):
        for q in ['избирается сроком на', 'какой срок полномочий генерального директора']:
            ans = self.answer(text, q)
            if 4 < len(ans) < 25:
                return ans.lower()
        return None

model = AnswerModel()
