#from tracemalloc import start
import speech_recognition as sr
from moviepy.editor import *
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence


def convert():
    cont = 0
    #lê e cria a variavel
    mp4_file = "video.mp4"
    wav_file = "audio.wav"
    
    #converte
    videoClip = VideoFileClip(mp4_file)
    audioclip = videoClip.audio
    audioclip.write_audiofile(wav_file)

    audioclip.close()
    videoClip.close()

    filename = "audio.wav"
    arquivo = open("legenda-pt.srt", "w", encoding="utf-8")
    
    r = sr.Recognizer()
    sound = AudioSegment.from_wav(filename)  
    chunks = split_on_silence(sound, min_silence_len = 2000, silence_thresh = sound.dBFS-16, keep_silence = 1000)
    folder_name = "audio-chunks"
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    for i, audio_chunk in enumerate(chunks, start=1):
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        with sr.AudioFile(chunk_filename) as source:
            audio = r.record(source)
        try:
            text = r.recognize_google(audio, language = "pt-BR")
        except sr.UnknownValueError as e:
            print("Erro", str(e))
            #arquivo.write("\n Erro \n\n")
        else:
            text = f"{text.capitalize()}. "
            print(chunk_filename, ":", text)
            whole_text += text
            arquivo.write("\n" + text + "\n\n")
            cont += 1
    # return the text for all chunks detected
    arquivo.write("\n" + cont + "\n\n")
    return whole_text

convert()
