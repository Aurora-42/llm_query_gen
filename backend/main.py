import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration
from flask import Flask, request, jsonify

app = Flask(__name__)

def init_tokenizer(model_name: str = 't5-small') -> T5Tokenizer:
    return T5Tokenizer.from_pretrained(model_name, legacy=False)

def load_model(model_name='cssupport/t5-small-awesome-text-to-sql'):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    model = model.to(device)
    model.eval()
    return model, device

def gen_sql(model: T5ForConditionalGeneration, tokenizer: T5Tokenizer, device: torch.device, input_prompt: str) -> str:
    inputs = tokenizer(input_prompt, padding=True, truncation=True, return_tensors="pt").to(device)
    
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=512)
    generated_sql = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return generated_sql

tokenizer = init_tokenizer()
model, device = load_model()

@app.route('/gen_sql', methods=['POST'])
def gen_sql_endpoint():
    data = request.json
    schema = data.get('schema')
    query = data.get('query')
    input_prompt = f"tables:\n{schema}\nquery:\n{query}"
    
    generated_sql = gen_sql(model, tokenizer, device, input_prompt)
    return jsonify({"generated_sql": generated_sql})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)