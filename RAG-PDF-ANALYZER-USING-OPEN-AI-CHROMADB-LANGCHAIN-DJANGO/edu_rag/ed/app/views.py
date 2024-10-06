import os
from django.shortcuts import render, redirect
from .models import PDFDocument
from .forms import PDFUploadForm
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from gtts import gTTS
from django.conf import settings
import os
from gtts import gTTS
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from .models import PDFDocument  # Assuming you have a model named PDF for uploaded PDFs
from PyPDF2 import PdfReader  # Assuming you're using PyPDF2 for PDF reading
from django.core.files.storage import FileSystemStorage
# Ensure your OpenAI API key is set
os.environ["OPENAI_API_KEY"] = "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"
def home(request):
    return render(request,'intro.html')
def upload_pdf(request):
    if request.method == "POST":
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('pdf_list')
    else:
        form = PDFUploadForm()
    return render(request, 'upload_pdf.html', {'form': form})

def pdf_list(request):
    pdfs = PDFDocument.objects.all()
    return render(request, 'pdf_list.html', {'pdfs': pdfs})

from django.core.files.storage import FileSystemStorage

def convert_pdf_to_speech(request, pdf_id):
    # Get the PDF object
    pdf = get_object_or_404(PDFDocument, id=pdf_id)
    
    # Extract the PDF text
    pdf_path = pdf.file.path  # Assuming your PDF model has a file field
    title = pdf.title
    
    # Convert the PDF content to speech and save the audio file
    audio_file_name = convert_pdf_to_speech_function(pdf_path, title)

    # Return the audio file name and make it available in the context
    return redirect('ask_question', pdf_id=pdf_id)

def convert_pdf_to_speech_function(pdf_path, title):
    """
    Convert the entire PDF text to speech and return the audio file path.
    """
    # Load and read PDF using PyPDFLoader or PyPDF2 (assumed PyPDFLoader or similar is used here)
    loader = PdfReader(pdf_path)
    full_text = ""
    for page in loader.pages:
        full_text += page.extract_text()

    # Convert text to speech using gTTS
    tts = gTTS(text=full_text, lang='en')
    
    # Create the file path
    audio_file_name = f"{title.replace(' ', '_')}.mp3"
    audio_file_path = os.path.join(settings.MEDIA_ROOT, 'audio', audio_file_name)
    
    # Ensure the 'audio' folder exists in the media directory
    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, 'audio')):
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'audio'))

    # Save the audio file
    tts.save(audio_file_path)

    # Return just the file name (relative to MEDIA_URL) for HTML usage
    return audio_file_name

def ask_question(request, pdf_id):
    pdf = PDFDocument.objects.get(id=pdf_id)
    pdf_path = pdf.pdf_file.path
    audio_file = pdf.audio_file.name if pdf.audio_file else None  # Use the stored audio file name

    if request.method == "POST":
        query = request.POST.get('query')

        # Create the RAG application
        rag_app = create_rag_app(pdf_path)

        # Get the answer to the user's query
        try:
            result = rag_app.run(query)
        except Exception as e:
            return render(request, 'ask_question.html', {
                'pdf': pdf,
                'error': f"Error retrieving answer: {str(e)}"
            })

        # Text-to-speech conversion
        if 'convert_to_speech' in request.POST:
            try:
                audio_file_name = convert_pdf_to_speech(pdf_path, pdf.title)  # Call your TTS function
                pdf.audio_file = f'audio/{audio_file_name}'  # Save the audio file path in the model
                pdf.save()  # Save the PDFDocument instance to update the audio file path
                audio_file = pdf.audio_file.name  # Update audio_file variable
            except Exception as e:
                return render(request, 'ask_question.html', {
                    'pdf': pdf,
                    'result': result,
                    'query': query,
                    'error': f"Error converting PDF to speech: {str(e)}"
                })

        return render(request, 'ask_question.html', {
            'pdf': pdf,
            'result': result,
            'query': query,
            'audio_file': audio_file  # Pass audio file path to the template
        })

    return render(request, 'ask_question.html', {'pdf': pdf, 'audio_file': audio_file})

def create_rag_app(pdf_path):
    """
    Creates a RAG application using LangChain, OpenAI, and ChromaDB.
    """
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()

    db = Chroma.from_documents(texts, embeddings)

    retriever = db.as_retriever()
    qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=retriever)

    return qa

# views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import PDFDocument
from gtts import gTTS
import os
from django.conf import settings

from django.shortcuts import render, get_object_or_404
from .models import PDFDocument  # Assuming your PDFDocument model is imported

def text_to_speech_view(request, pdf_id):
    pdf = get_object_or_404(PDFDocument, id=pdf_id)

    audio_file = pdf.audio_file.name if pdf.audio_file else None  # Use the stored audio file name

    if request.method == "POST":
        # Call your conversion function here
        audio_file_name = convert_pdf_to_speech_function(pdf.pdf_file.path, pdf.title)  # Convert to speech
        pdf.audio_file = f'audio/{audio_file_name}'  # Save the audio file path in the model
        pdf.save()  # Save the PDFDocument instance to update the audio file path
        audio_file = pdf.audio_file.name  # Update audio_file variable

    # Fetch all PDF documents for listing
    all_pdfs = PDFDocument.objects.all()

    return render(request, 'text_to_speech.html', {
        'pdf': pdf,
        'audio_file': audio_file,
        'pdfs': all_pdfs  # Pass all PDFs to the template
    })


def convert_pdf_to_speech_function(pdf_path, title):
    """
    Convert the entire PDF text to speech and return the audio file path.
    """
    # Load and read PDF using PyPDF2 or similar
    loader = PdfReader(pdf_path)
    full_text = ""
    for page in loader.pages:
        full_text += page.extract_text()

    # Convert text to speech using gTTS
    tts = gTTS(text=full_text, lang='en')
    
    # Create the file path
    audio_file_name = f"{title.replace(' ', '_')}.mp3"
    audio_file_path = os.path.join(settings.MEDIA_ROOT, 'audio', audio_file_name)
    
    # Ensure the 'audio' folder exists in the media directory
    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, 'audio')):
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'audio'))

    # Save the audio file
    tts.save(audio_file_path)

    return audio_file_name


