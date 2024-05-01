from openai import OpenAI
api_key = "my key"
client = OpenAI(api_key=api_key)
audio_file = open("/Users/apple/LessonITC/start_project/django-chatbot/django_chatbot/audio/dk.mp3", "rb")
transcript = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file
)
