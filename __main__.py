import PyPDF2
from gtts import gTTS
import os
import time
import pyttsx3
from playsound import playsound

# Função para extrair texto do PDF
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
        return text

# Função para ler o índice da última frase lida
def read_last_index():
    if os.path.exists('last_index.txt'):
        with open('last_index.txt', 'r') as f:
            return int(f.read().strip())
    return 0

# Função para salvar o índice da última frase lida
def save_last_index(index):
    with open('last_index.txt', 'w') as f:
        f.write(str(index))

# Função para dividir o texto e reproduzir em partes
def stream_text_to_audio(text):
    sentences = text.split('. ')  # Divida o texto em frases
    last_index = read_last_index()  # Leia o último índice salvo

    for i in range(last_index, len(sentences)):
        sentence = sentences[i]
        print(sentence)
        if sentence.strip():  # Verifique se a frase não está vazia
            audio_path = 'temp_audio.mp3'  # Caminho temporário para o áudio
            tts = gTTS(text=sentence, lang='pt', timeout=10, slow=False)
            tts.save(audio_path)
            playsound(audio_path)  # Reproduzir o áudio
            time.sleep(0.5)  # Pausa entre as frases
            os.remove(audio_path)  # Remover o arquivo de áudio temporário
            
            # Salvar o índice atual
            save_last_index(i)

def main():
    # Caminho do arquivo PDF
    filename = 'relatorio'
    pdf_path = f'pdf/{filename}.pdf'

    # Extrair texto do PDF
    pdf_text = extract_text_from_pdf(pdf_path)

    # Converter texto em áudio e fazer streaming
    stream_text_to_audio(pdf_text)

if __name__ == '__main__':
    main()
