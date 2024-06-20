import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import sys

API_KEY = 'Aquí colocas tu API KEY de la API de Google Generative AI Gemini'
genai.configure(api_key=API_KEY)

def translate_text(text):
  model = genai.GenerativeModel('gemini-1.5-flash')
  try:
    response = model.generate_content(
      f"Tu tarea es traducir un libro del inglés al español, este es público y fue hecho con LaTeX, así que debes mantener el formato de LaTeX en tu tradución. No agregues contenido nuevo, tu tarea es solo traducir. Como excepción, no debes traducir los textos que esten dentro de {{lstlisting}}. Tu respuesta debe ser directamente el texto traducido, no agregues ni comillas ni algún otro caracter extra en tu respuesta. Este es el texto:\n{text}",
      stream=False,
      safety_settings={
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE
      }
    )
    response.resolve()  # Completa la iteración de la respuesta
    # Ajusta esto según el formato de la respuesta de la API
    return f"{response.text}"
  except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

def translate_file(file_path):
  with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()
  
  paragraphs = content.split('\n\n')  # Dividimos el contenido en párrafos
  translated_content = ''
  current_chunk = ''

  for paragraph in paragraphs:
    if len(current_chunk) + len(paragraph) + 2 <= 5000:  # +2 para los \n\n
      current_chunk += paragraph + '\n\n'
    else:
      translated_chunk = translate_text(current_chunk)
      translated_content += translated_chunk
      current_chunk = paragraph + '\n\n'
  
  if current_chunk:  # Traducir el último chunk
    translated_chunk = translate_text(current_chunk)
    translated_content += translated_chunk
  
  # Guardar el contenido traducido en un nuevo archivo
  translated_file_path = file_path.replace('.tex', '_translated.tex')
  with open(translated_file_path, 'w', encoding='utf-8') as file:
    file.write(translated_content)
  
  print(f'Translation completed for {file_path}, saved to {translated_file_path}')

def main():
  if len(sys.argv) != 2:
    print("Usage: python main.py <chapter_file.tex>")
    sys.exit(1)
  
  file_path = sys.argv[1]
  if not os.path.exists(file_path):
    print(f"Error: File {file_path} does not exist.")
    sys.exit(1)
  
  translate_file(file_path)

if __name__ == '__main__':
  main()
