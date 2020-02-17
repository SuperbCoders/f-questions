from collections import OrderedDict

from django.shortcuts import render
from django import forms

import warnings
warnings.simplefilter('ignore')

from deal_api.dl_model import AnswerModel
model = AnswerModel()


class DealForm(forms.Form):
    deal = forms.CharField(widget=forms.Textarea, label='Договор', required=True)
    q1 = forms.CharField(widget=forms.TextInput, label='Вопрос 1', required=True)
    q2 = forms.CharField(widget=forms.TextInput, label='Вопрос 2', required=False)
    q3 = forms.CharField(widget=forms.TextInput, label='Вопрос 3', required=False)


def get_deal_form(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = DealForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            questions = OrderedDict()
            q_list = [form.cleaned_data['q1'], form.cleaned_data['q2'], form.cleaned_data['q3']]
            for q in q_list:
                questions[q] = model.answer(form.cleaned_data['deal'], q)

            return render(
                request, 'response.html', {
                    'deal': form.cleaned_data['deal'],
                    'questions': questions
                }
            )

    # if a GET (or any other method) we'll create a blank form
    else:
        form = DealForm()

    return render(request, 'form.html', {'form': form})
