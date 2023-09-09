import openai   
from dotenv import load_dotenv
import openai
import os
from database import Database
import datetime



# def get_completion(prompt, model = "gpt-3.5-turbo-16k-0613"):
#     message = [
#         {"role": "user", "content": "Give me five random words."},
#         {"role": "system", "content": "Elephant, sunshine, guitar, pineapple, laughter"},
#         {"role": "user", "content": prompt}]
#     response = openai.ChatCompletion.create(
#         model = model,
#         messages = message,
#         temperature = 0
#     )
#     return 


class OpenAIAPI():
    def __init__(self, database):
        load_dotenv()
        secret_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = secret_key
        self.database = database

    def get_completion(self,chat_id, prompt, model="gpt-3.5-turbo-16k-0613"):


        #query the database to check for chat history or if it's an initial prompt 
        message = self.database.get_previous_chat(chat_id)

        # Update the database with our prompt.
        self.database.update_chat(chat_id, str(datetime.datetime.now()), "user", prompt)


        if len(message) == 0:
            # Prompt eNgiNeErIng
            # Here, we will set instructions.
            message.append({
                "role": "user",
                "content": "This is a system message to tell you how you should act. Do not reply to this message. The text surrounded in brackets are your instructions. [1. Always start your response with a \"yes sir\"] The next message is from the user themself."
            })
        #we append our prompt to our previous chat (which is empty for an initial prompt)
        message.append(
            {
                "role": "user",
                "content": prompt
            }
        )
    
        #Using this message we send our api request 
        response = openai.ChatCompletion.create(
            model = model,
            messages = message,
            temperature = 0
        )


        #update the databse with our response
        self.database.update_chat(chat_id, str(datetime.datetime.now()), "system", response.choices[0].message["content"])

        return response.choices[0].message["content"]

        # Get the previous messages for this specific chatID.







