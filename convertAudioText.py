# Importa as bibliotecas necessárias
import speech_recognition as sr  # Biblioteca para reconhecimento de fala
from moviepy.editor import *     # Biblioteca para manipulação de vídeos
import os                        # Biblioteca para operações de sistema
from pydub import AudioSegment   # Biblioteca para manipulação de áudio
from pydub.silence import split_on_silence  # Função para dividir áudio com base no silêncio

# Função para converter um vídeo em áudio e transcrever a fala em texto
def convert():
    cont = 0  # Variável para contar as partes do áudio transcritas
    
    # Define os nomes dos arquivos de entrada (vídeo) e saída (áudio)
    mp4_file = "video.mp4"
    wav_file = "audio.wav"
    
    # Converte o vídeo para áudio
    videoClip = VideoFileClip(mp4_file)  # Carrega o vídeo
    audioclip = videoClip.audio         # Obtém o áudio do vídeo
    audioclip.write_audiofile(wav_file)  # Salva o áudio em um arquivo WAV
    
    audioclip.close()    # Fecha o arquivo de áudio
    videoClip.close()    # Fecha o arquivo de vídeo

    # Define o nome do arquivo de áudio
    filename = "audio.wav"
    # Cria um arquivo para salvar a transcrição em formato de legenda (SRT)
    arquivo = open("legenda-pt.srt", "w", encoding="utf-8")
    
    r = sr.Recognizer()  # Cria um objeto Recognizer para reconhecimento de fala
    sound = AudioSegment.from_wav(filename)  # Carrega o arquivo de áudio
    # Divide o áudio em partes com base no silêncio
    chunks = split_on_silence(sound, min_silence_len=2000, silence_thresh=sound.dBFS-16, keep_silence=1000)
    
    folder_name = "audio-chunks"  # Pasta para armazenar os trechos de áudio
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)  # Cria a pasta se não existir
    
    whole_text = ""  # Variável para armazenar o texto completo da transcrição
    
    # Itera sobre os trechos de áudio
    for i, audio_chunk in enumerate(chunks, start=1):
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")  # Nome do arquivo de trecho de áudio
        audio_chunk.export(chunk_filename, format="wav")  # Exporta o trecho de áudio para um arquivo WAV
        
        with sr.AudioFile(chunk_filename) as source:
            audio = r.record(source)  # Lê o trecho de áudio com o Recognizer
        try:
            text = r.recognize_google(audio, language="pt-BR")  # Realiza o reconhecimento de fala
        except sr.UnknownValueError as e:
            print("Erro", str(e))
            #arquivo.write("\n Erro \n\n")
        else:
            text = f"{text.capitalize()}. "  # Capitaliza o texto transcrit
            print(chunk_filename, ":", text)  # Exibe o trecho de áudio e o texto transcrit
            whole_text += text  # Adiciona o texto à transcrição completa
            arquivo.write("\n" + text + "\n\n")  # Escreve o texto no arquivo de legenda
            cont += 1
    
    arquivo.write("\n" + str(cont) + "\n\n")  # Escreve o número de partes transcritas no arquivo de legenda
    return whole_text  # Retorna o texto completo da transcrição

# Chama a função de conversão e transcrição
convert()
