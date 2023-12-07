import torch
# import os

# from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    # BitsAndBytesConfig,
    # TrainingArguments,
    # pipeline,
    # logging,
)
# from peft import LoraConfig
# from trl import SFTTrainer
from peft import PeftModel

def check_answer(text):
    if '/' in text:
        return True
    if '\\' in text:
        return True
    return not any(char.isalpha() for char in text)

def get_model_response(question, person):

    #my_model = 'MeghanaArakkal/TuringChat'

    model_id="NousResearch/Llama-2-7b-chat-hf"
    model = AutoModelForCausalLM.from_pretrained(model_id,load_in_8bit=True,device_map="auto")
    model = PeftModel.from_pretrained(model, person.endpoint, device_map="auto")
    tokenizer = AutoTokenizer.from_pretrained(model_id)

    model.eval()

    eval_prompt = """
    Reply to the following messages as the user {NAME}. Provide just one reply, do not continue the conversation
    User (John): {QUESTION}[/]
    {NAME}:
    """
    prompt = eval_prompt.format(NAME=person.user,QUESTION=question)
    model_input = tokenizer(prompt, return_tensors="pt").to("cuda")

    retry = True
    count=0
    while retry and count<3:
        with torch.no_grad():
            answer = tokenizer.decode(model.generate(**model_input, max_new_tokens=50,do_sample=True)[0], skip_special_tokens=True)
        print("COUNT")
        print(count)
        print("ANSWER")
        print(answer)
        answer=answer[len(prompt):]
        retry = check_answer(answer)
        count+=1
    
    return answer

