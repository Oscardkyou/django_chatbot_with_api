from celery import shared_task
from .models import RecognitionHistory

@shared_task
def recognize_and_save_history(text):
    # Выполнить распознавание текста
    # Например, если у вас есть функция для распознавания:
    # recognized_text = perform_recognition(text)
    recognized_text = text  # Здесь нужно выполнить распознавание

    # Сохранить результат в базе данных
    RecognitionHistory.objects.create(text=recognized_text)