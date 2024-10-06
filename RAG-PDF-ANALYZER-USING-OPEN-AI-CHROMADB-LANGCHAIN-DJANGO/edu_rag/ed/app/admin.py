from django.contrib import admin
from .models import PDFDocument

class PDFDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')

admin.site.register(PDFDocument, PDFDocumentAdmin)
