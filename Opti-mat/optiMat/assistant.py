import openai
import time
from dotenv import load_dotenv
import os

load_dotenv()

client  = openai.OpenAI()

Asst_name = 'Opti-Mat'
Asst_model = 'gpt-3.5-turbo'
Asst_id = os.environ.get("ASST_ID")

Asst_instructions= "You are an AI assistant specialized in material selection, you recommend the most suitable material for a particular application depending on the clients description. You.ve helped top researchers and engineers in selecting materials for their product design"


# === Create Assistant ===
class AssistantManager:
    thread_id = None 
    assistant_id = Asst_id 
    
    def __init__(self, model: str = Asst_model) -> None:
        self.client = openai.OpenAI()
        self.model = model
        self.assistant = None
        self.thread = None
        self.run = None
        self.summary = None
        
        # Retrieve existing assistant and thread if IDs are already available
        if AssistantManager.assistant_id:
            self.assistant = self.client.beta.assistants.retrieve(
                assistant_id = AssistantManager.assistant_id
            )
            
        if AssistantManager.thread_id:
            self.thread = self.client.beta.threads.retrieve(
                thread_id= AssistantManager.thread_id
            )
            
    
    def create_assistant(self, name = Asst_name, instructions = Asst_instructions):
        if not self.assistant:
            assistant_obj = self.client.beta.assistants.create(
                name = Asst_name,
                instructions= instructions,
                model= Asst_model,
                response_format={"type": "json_object"}
            )
            
            AssistantManager.assistant_id = assistant_obj.id
            self.assistant = assistant_obj
            print('Assistant created, id: ', self.assistant.id)
            return

        print('Connecting to Assistant, id:  ', self.assistant_id)
    
    def create_thread(self):
        if not self.thread:
            thread_obj = self.client.beta.threads.create()
            
            AssistantManager.thread_id = thread_obj.id
            self.thread = thread_obj
            print("Thread created, id: ", self.thread.id)
            return
        
        print('Connecting to thread, id: ', self.thread.id)
            
    def add_message_to_thread(self, role, content):
        if self.thread:
            self.client.beta.threads.messages.create(
                thread_id=self.thread.id,
                role=role,
                content=content
            )
        else:
            print('There is no thread')
    
    def run_assistant(self):
        if self.thread and self.assistant:
            self.run = self.client.beta.threads.runs.create(
                thread_id = self.thread.id,
                assistant_id = self.assistant.id,
                # instructions = instructions
            )
    
    def process_message(self):
        if self.thread:
            messages = self.client.beta.threads.messages.list(
                thread_id=self.thread.id
            )
            summary = []
            
            last_message = messages.data[0]
            role = last_message.role
            response = last_message.content[0].text.value
            summary.append(response)
            
            self.summary = "\n".join(summary)            
            return response
            
    def call_required_functions(self, required_actions):
        # if not self.run:
        #     return
        # tools_outputs = []
        pass
    
    def wait_for_completion(self):
        if self.thread and self.run:
            while True:
                time.sleep(5)
                run_status = self.client.beta.threads.runs.retrieve(
                    thread_id = self.thread.id,
                    run_id = self.run.id
                )
                print('run status: ', run_status.status)
                
                if run_status.status == 'completed':
                    response = self.process_message()
                    return response
                
                
# manager = AssistantManager()
# manager.create_assistant()
# manager.create_thread()
# manager.add_message_to_thread(role='user', content='artificial pyloric sphincter')
# manager.run_assistant()
# response = manager.wait_for_completion()


# print('----------------------------------------')
# print(response)