import speech_recognition as sr
import pyttsx3
#import request

reconhecedor = sr.Recognizer()
microfone = sr.Microphone()
query = ""

escuta = pyttsx3.init()

def ouvir():
    try:
        with sr.Microphone(device_index=1) as source:
            print('Ouvindo...')
            voice = reconhecedor.listen(source)
            command = reconhecedor.recognize_google(voice, language='pt-br')
            print(command)
            return command

    except:
        return 'Não escutei nada :/'

with microfone as mic:
    reconhecedor.adjust_for_ambient_noise(mic)
    print("Fale suas preferências!")
    audio = reconhecedor.listen(mic)
    msg = reconhecedor.recognize_google(audio, language='pt')

query = msg
print(query)

json = ["id_conversa" ,"561",
        "resposta" , "Esta configuração deve ser ideal para este tipo de uso:"
        "Processador: Intel Core i7 8700K ou AMD Ryzen 7 2700X , Placa de vídeo: NVIDIA GTX 1080 8GB ou AMD RX Vega 64 8GB , "
        "Memória RAM: 16GB , Espaço em disco: 100 GB de espaço livre no HD , Sistema operacional: Windows 10 64 Bit. " ]

resposta = json[3]

escuta.say(resposta)
escuta.runAndWait()
