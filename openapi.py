import openai   
from dotenv import load_dotenv
import openai
import os


load_dotenv()
secret_key = os.getenv("OPENAI_API_KEY")
openai.api_key = secret_key
def get_completion(prompt, model = "gpt-3.5-turbo-16k-0613"):
    message = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model = model,
        messages = message,
        temperature = 0
    )
    return response
