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

def get_model_response(question):
    my_model = 'MeghanaArakkal/TuringChat'

    model_id="NousResearch/Llama-2-7b-chat-hf"
    model = AutoModelForCausalLM.from_pretrained(my_model,load_in_8bit=True,device_map="auto")
    tokenizer = AutoTokenizer.from_pretrained(model_id)

    model.eval()

    eval_prompt = f"""
    Reply to the following messages as the user Meghana. Provide just one reply, do not continue the conversation
    User (John): {question}
    Meghana:
    """
    prompt = eval_prompt.format(question=question)
    model_input = tokenizer(prompt, return_tensors="pt").to("cuda")

    with torch.no_grad():
        answer = tokenizer.decode(model.generate(**model_input, max_new_tokens=250,do_sample=True)[0], skip_special_tokens=True)
    
    return answer

