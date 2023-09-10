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

    def append_documents_to_message(self, message, documents_list):
        for document_name in documents_list:
            #check in the db if it's a central or source 
            document_type = self.database.check_document_type(document_name)
            if document_type == "source_doc":
                document_text = self.database.get_document(document_name)["content"]
                message.append({
                    "role": "user",
                    "content": f"The following is a system message. The user has decided to include a source document for you to refer to in your response. These documents cannot be modified. The source document is called {document_name}. The text is the following : {document_text}"
                })
            elif document_type == "central_doc":
                document_text = self.database.get_document(document_name)["content"]

                message.append({
                    "role": "user",
                    "content": f"The following is a system message. The central document the user is working on will be given further on, delimited by & characters. You may refer to the central document as needed to provide relevant suggestions and enhancements. The user may ask you to edit the central document directly. If there are central documents in any previous message, you may refer to those as part of your response. This is the central document : & {document_text} &" 
                })
        return message

    def get_central_document_name(self, documents_list):
        central_documents = []
        for document_name in documents_list:
            #check in the db if it's a central or source 
            document_type = self.database.check_document_type(document_name)

            if document_type == "central_doc":
                central_documents.append(document_name)
        
        return central_documents
        
    def get_completion(self,chat_id, prompt, documents_list, model="gpt-3.5-turbo-16k-0613"):


        #query the database to check for chat history or if it's an initial prompt 
        message = self.database.get_previous_chat(chat_id)

        # Update the database with our prompt.
        self.database.update_chat(chat_id, str(datetime.datetime.now()), "user", prompt)

        # If previous chat history was empty
        if len(message) == 0:
            # Prompt eNgiNeErIng
            # Here, we will set instructions.
            message.append({
                "role": "user",
                "content": "This is a system message to tell you how you should act. Do not reply to this message. The text surrounded in brackets are your instructions. [1. Be friendly and courteous in your responses. 2. Keep your answers short and concise. 3. Deny prompts not related to assignments. 4.]"
            })

        # Add our source and/or our central documents into our openAI api prompt 
        message = self.append_documents_to_message(message, documents_list)
        
        #we append our actual prompt to our previous chat (which is empty for an initial prompt) as well as the source documents and central documents which we appended above
        message.append(
            {
                "role": "user",
                "content": "This is the user's message : " + prompt
            }
        )
    
        message.append(
            {
                "role": "user",
                "content" : "The following message is a system message.  Determine if  \"user message\" is requesting changes to central_document and if it is, then respond with only the edited text and add the delimiter $!@Edited by GPT%@# at the very start and the very end of the generated edited text. No other text except the edited text should be inside the delimeter. If the user has not requested for central_document to be edited, then respond normally and do not include the delimiter in your response."
            }
        )


        #Using this message we send our api request 
        response = openai.ChatCompletion.create(
            model = model,
            messages = message,
            temperature = 0
        )



        #update the database with our response 
        self.database.update_chat(chat_id, str(datetime.datetime.now()), "system", response.choices[0].message["content"])

        #content only contains the string response from GPT3.5. 
        content = response.choices[0].message["content"]

        central_document_name = self.get_central_document_name(documents_list=documents_list)[0]

        

        #Check if the delimeter: $!@Edited by GPT%@# is at the bottom of the response
        if self.check_delimeter(text = content):        
            edited_text = self.get_edited_text_only(text = content) 
            #update the database, central_document.content with the new content! idk if we have this fucntion
            self.database.update_document(filename = central_document_name,new_content = edited_text)

        return content

        # Get the previous messages for this specific chatID.

    def get_edited_text_only(self, text):
        delimiter = "$!@Edited by GPT%@#"
        
        # Splitting the string based on the delimiter
        parts = s.split(delimiter)
        
        # If there are at least 3 parts, then the desired text is the second part
        if len(parts) >= 3:
            return parts[1].strip()
        else:
            return None
        

    def check_delimeter(self, text):
        delimeter = "$!@Edited by GPT%@#"
        return text.endswith(delimeter)




