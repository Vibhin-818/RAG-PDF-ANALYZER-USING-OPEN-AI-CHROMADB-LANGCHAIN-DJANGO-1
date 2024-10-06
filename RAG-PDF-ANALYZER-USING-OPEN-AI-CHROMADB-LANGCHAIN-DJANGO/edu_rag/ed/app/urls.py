# urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (
    upload_pdf,
    pdf_list,
    ask_question,
    convert_pdf_to_speech,
    text_to_speech_view,
    home,
   # voice_assistant_view,  # Import the new view
)

urlpatterns = [
    path('upload/', upload_pdf, name='upload_pdf'),
    path('pdfs/', pdf_list, name='pdf_list'),
    path('ask/<int:pdf_id>/', ask_question, name='ask_question'),
    path('convert_pdf_to_speech/<int:pdf_id>/', convert_pdf_to_speech, name='convert_pdf_to_speech'),
    path('text_to_speech/<int:pdf_id>/', text_to_speech_view, name='text_to_speech'),
    #path('voice_assistant/', voice_assistant_view, name='voice_assistant'),  # Add this line
    path('', home, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
