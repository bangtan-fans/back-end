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

    def append_source_docs_to_message(self, message, source_docs):
        for document_name in source_docs:
            document_text = self.database.get_source_document(document_name)
            message.append({
                "role": "user",
                "content": f"The following is a system message. The user has decided to include a source document for you to refer to in your response. The source document is called {document_name}. The text is the following : {document_text}"
            })
        return message

    def append_content_doc_to_message(self, message, content_docs):
        for document_name in content_docs:
            document_text = self.database.get_source_document(document_name)
            
            message.append({
                "role": "user",
                "content": f"The following is a system message. The content document the user is working on will be given further on, delimited by & characters. You may refer to the content document as needed to provide relevant suggestions and enhancements. If there are source documents in any previous message, you may refer to those as part of your response. This is the content document : & {document_text} &" 
            })
        return message


    def get_completion(self,chat_id, prompt, source_docs, model="gpt-3.5-turbo-16k-0613"):


        #query the database to check for chat history or if it's an initial prompt 
        message = self.database.get_previous_chat(chat_id)

        # Update the database with our prompt.
        self.database.update_chat(chat_id, str(datetime.datetime.now()), "user", prompt)

        if len(message) == 0:
            # Prompt eNgiNeErIng
            # Here, we will set instructions.
            message.append({
                "role": "user",
                "content": "This is a system message to tell you how you should act. Do not reply to this message. The text surrounded in brackets are your instructions. [1. Be friendly and courteous in your responses. 2. Keep your answers short and concise. 3. Deny prompts not related to assignments. 4.]"
            })

        self.append_source_docs_to_message(message, source_docs)
        

        #we append our prompt to our previous chat (which is empty for an initial prompt)
        message.append(
            {
                "role": "user",
                "content": "This is the user's message : " + prompt
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







