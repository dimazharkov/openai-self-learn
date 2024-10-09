from dotenv import load_dotenv
from openai import AzureOpenAI
import os

load_dotenv()

def get_azure_openai_client() -> AzureOpenAI:
   azure_api_key = os.getenv("OPENAI_API_KEY")
   azure_endpoint = "https://openai-east-prod.openai.azure.com"
   azure_api_version = "2023-03-15-preview"

   client = AzureOpenAI(
      azure_endpoint=azure_endpoint,
      api_key=azure_api_key,
      api_version=azure_api_version
   )

   return client

def use_azure_openai_client(prompt: str, text: str, model: str = "alec-gpt-4o-test", temperature: float = 0, max_tokens: int = 200) -> str:
   client = get_azure_openai_client()
   response = client.chat.completions.create(
      model=model,
      temperature=temperature,
      max_tokens=max_tokens,
      messages=[
         {"role": "system", "content": prompt},
         {"role": "user", "content": text}
      ]
   )

   return response.choices[0].message.content