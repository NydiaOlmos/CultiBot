import requests
import json

data = {
    "model": "google/gemma-4-e4b",
    "input": '''
        {"id":8,
        "planta":{
            "id":1,
            "nombre":"Tomata",
            "tipo":"Tomate Roma",
            "tipo_suelo":"otro"
        },
        "humedad_suelo":61.8,
        "temperatura_ambiente":23.5,
        "luminosidad":11500,
        "nutrientes":{
            "nitrogeno":2.1,
            "potasio":1.8,
            "fosforo":1.2
        },
        "fecha":"2026-05-21T18:00:00"}
    ''',
    "max_output_tokens": 3000,
    "reasoning": "on"
}

# data = {
#     "model": "google/gemma-4-e4b",
#     "input": "¿Cómo puedo hacer un frontEnd básico con html?cls",
#     "max_output_tokens": 3000,
#     "reasoning": "on"
# }

response = requests.post(
    "http://localhost:1234/api/v1/chat",
    json= data
)

content = response.json()['output'][1]['content']
print(content)

if "```json" in content:
    texto_limpio = content.split("```json")[1].split("```")[0].strip()
else:
    texto_limpio = content.strip()

datos_json = json.loads(texto_limpio)
print(datos_json)