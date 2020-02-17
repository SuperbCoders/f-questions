from django.db import models
from regex_field.fields import RegexField


class DocumentCategory(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=250, null=False, blank=False)


class DocumentRegex(models.Model):
    category = models.ForeignKey(DocumentCategory, on_delete=models.CASCADE)
    search_pattern = RegexField(max_length=500, null=False, blank=False)
