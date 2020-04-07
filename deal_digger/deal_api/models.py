from django.db import models
from django.utils.translation import gettext_lazy as _

class Document(models.Model):
    class States(models.IntegerChoices):
        NOT_PROCESSED = 0
        PROCESSING = 1
        PROCESSED = 2

    pdf_file = models.FileField(upload_to='pdf')
    status = models.IntegerField(choices=States.choices, default=States.NOT_PROCESSED)
    name = models.CharField(max_length=255)
    text = models.TextField(null=True)


class DocumentAnswer(models.Model):
    class QuestionTypes(models.IntegerChoices):
        EXECUTOR = 0, _('Кто исполнительный орган')
        EXECUTOR_PERIOD = 1, _('Период действия исполнительного органа')

    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    question_type = models.IntegerField(choices=QuestionTypes.choices)
    answer = models.TextField()
    raw_answer = models.TextField(null=True)
