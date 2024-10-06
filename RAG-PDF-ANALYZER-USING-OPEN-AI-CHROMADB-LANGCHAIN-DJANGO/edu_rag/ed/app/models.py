from django.db import models

class PDFDocument(models.Model):
    title = models.CharField(max_length=200)
    pdf_file = models.FileField(upload_to='pdfs/')
    audio_file = models.FileField(upload_to='audio/', blank=True, null=True)  # Add this line
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
