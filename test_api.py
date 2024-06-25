import requests

file_path = r'French Audio 2.wav'

url = "http://localhost:8000/recognize-and-translate/"
files = {'file': open(file_path, 'rb')}
language = {'language': 'French'}

response = requests.post(url, files=files, data=language)

response_json = response.json()

if response.status_code == 200:
    translated_text = response_json.get('translated_text')
    recognized_text = response_json.get('language_text')

    print("Translated Text:", translated_text)
    print("Recognized Text:", recognized_text)
else:
    print(f"Error: {response.status_code} - {response.json()['detail']}")
