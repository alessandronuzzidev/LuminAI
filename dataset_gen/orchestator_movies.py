import os
import base64
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
      
endpoint = os.getenv("ENDPOINT_URL", "https://aless-mdr63rxd-eastus2.openai.azure.com/")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4o")
      
# Initialize Azure OpenAI client with Entra ID authentication
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
    azure_endpoint=endpoint,
    azure_ad_token_provider=token_provider,
    api_version="2025-01-01-preview",
)

system_prompt = "Eres un asistente de inteligencia artificial que resume películas en español. " \
            + "No uses emoticonos y genera solamente el resumen de la película. " \
            + "Puedes incluir nombres de personajes, actores o directores. " \
            + "Puedes incluir el nombre de la película. " \
            + "Deben ser resúmenes extensos, que puedan ocupar varias págians de documentos word o pdf. " \
            + "No incluyas caracteres para markdown, es para word o pdf, tampoco bullet points. Debe estar redactado al 100%."

for movie in ["Avatar", "Titanic", "The Godfather", "Inception", "The Dark Knight"]:
    # Encode the movie name to handle special characters
    movie_encoded = base64.b64encode(movie.encode()).decode()

    prompt = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": system_prompt
                }
            ]
        },
        {
            "role": "user", 
            "content": [
                {
                    "type": "text",
                    "text": f"Resume la película {movie}."
                }
            ]
        }
    ]
    response = client.chat.completions.create(
        model=deployment,
        messages=prompt,
        max_tokens=4000 
    )
    resume = response.choices[0].message.content
    with open(f"files_generated/{movie.lower()}.txt", "w") as f:
        f.write(resume)