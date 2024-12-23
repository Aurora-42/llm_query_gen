from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import time

model_name = "gpt2"

pipe = pipeline("text-generation", model=model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

tokenizer.pad_token = tokenizer.eos_token

def generate_query(prompt, max_length=100):
    inputs = tokenizer(prompt, return_tensors="pt", padding=True)
    attention_mask = inputs['attention_mask']
    
    outputs = model.generate(
        inputs["input_ids"],
        attention_mask=attention_mask,
        max_length=max_length,
        num_return_sequences=1,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        pad_token_id=tokenizer.eos_token_id
    )
    query = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return query

# Exemplo de uso
prompt = ("Write a SQL query to find all users who signed up in the last week. The table is named 'users' and has columns 'id', 'name', 'email', and 'signup_date'. The query should select 'id', 'name', and 'email' of the users who signed up in the last week.")
query = generate_query(prompt)

print(query)