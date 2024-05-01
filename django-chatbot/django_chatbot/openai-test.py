from openai import OpenAI

#openai1=OpenAI()
client = OpenAI(api_key='api key')


audio_path = 'dk.mp3'
audio_file = open(audio_path, "rb")
response = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
print(response.text)
