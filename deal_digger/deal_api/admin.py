from django.contrib import admin
from .models import DocumentCategory, DocumentRegex

admin.site.register(DocumentCategory)
admin.site.register(DocumentRegex)