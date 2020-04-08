from django.db.models import Count

from django.shortcuts import render, redirect
from django import forms

import warnings
warnings.simplefilter('ignore')

from django.views.generic.list import ListView
from django.views.generic import DetailView
from deal_api.models import Document
from deal_api.tasks import extract_text, ask_questions


class DealFileForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['pdf_file']


def get_deal_form(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = DealFileForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            extract_text.delay(form.instance.id)
            return redirect('/')
    else:
        form = DealFileForm()
    return render(request, 'form.html', {'form': form})


class DocumentListView(ListView):
    model = Document
    paginate_by = None
    template_name = 'document_list.html'

    def get_queryset(self):
        q = super(DocumentListView, self).get_queryset()
        return q.annotate(num_answers=Count('documentanswer'))


class DocumentDetailView(DetailView):
    template_name = 'document_item.html'
    queryset = Document.objects.prefetch_related('documentanswer_set')


def ask_model(request, pk):
    ask_questions.delay(pk)
    return render(request, 'doc_submitted.html')


def ask_ocr(request, pk):
    extract_text.delay(pk)
    return render(request, 'doc_submitted.html')


def delete_document(request, pk):
    Document.objects.filter(id=pk).delete()
    return redirect('/')
