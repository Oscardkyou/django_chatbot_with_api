from django.shortcuts import render, redirect
from django.http import JsonResponse
from openai import OpenAI

openai_api_key = 'my api key'

client = OpenAI(api_key=openai_api_key)

from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat
from django.utils import timezone
from .tasks import recognize_and_save_history
import whisper



def ask_openai(message):
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are an helpful assistant."},
        {"role": "user", "content": message},
    ]
    )

    answer = response.choices[0].message.content.strip()
    return answer

# Create your views here.
def chatbot(request):
    chats = Chat.objects.filter(user=request.user)

    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)

        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html', {'chats': chats})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('chatbot')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect('chatbot')
            except:
                error_message = 'Error creating account'
                return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = 'Password dont match'
            return render(request, 'register.html', {'error_message': error_message})
    return render(request, 'register.html')


def logout(request):
    auth.logout(request)
    return redirect('login')


def whisper(request):
    if request.method == 'POST' and request.FILES.get('audio_file'):
        audio_file = request.FILES['audio_file']
        # Инициализация клиента OpenAI
        client = OpenAI(api_key=openai_api_key)
        try:
            # Создание транскрипции аудиофайла
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file.read(),
                #response_format="text",  # Чтение содержимого аудиофайла
                #content_type='audio/mpeg'  # Указание типа содержимого
            )

            # Получение текста транскрипции
            transcribed_text = transcription.text

            # Возврат результата транскрипции в шаблон whisper.html
            return render(request, 'whisper.html', {'transcribed_text': transcribed_text})
        except Exception as e:
            error_message = f"Ошибка при обращении к OpenAI API: {str(e)}"
            return render(request, 'whisper.html', {'error_message': error_message})

    # Если запрос не POST или файл не был отправлен, просто отображаем шаблон whisper.html
    return render(request, 'whisper.html')


def recognize_text(request):
    # Получить текст для распознавания из запроса
    text = request.POST.get('text')
    # Вызвать Celery-задачу для выполнения распознавания и сохранения истории
    recognize_and_save_history(text)
    # Вернуть ответ пользователю, например, HTTP-ответ или шаблон страницы
    #Чтоб откладывалась история распознования
    #(В идале запросы делать при помощи Celery)


def result_page(request):
    return render(request, 'results.html')
