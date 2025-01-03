import os
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration
from flask import Flask, request, jsonify, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

# Swagger UI
SWAGGER_URL = '/swagger'
API_URL = '../../static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "llm_query_gen"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
# End Swagger UI

huggingface_token = os.getenv("HUGGINGFACE_API_TOKEN")

def init_tokenizer(model_name: str = 't5-small') -> T5Tokenizer:
    return T5Tokenizer.from_pretrained(model_name, legacy=False, use_auth_token=huggingface_token)

def load_model(model_name='cssupport/t5-small-awesome-text-to-sql'):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = T5ForConditionalGeneration.from_pretrained(model_name, use_auth_token=huggingface_token)
    model = model.to(device)
    model.eval()
    return model, device

def gen_sql(model: T5ForConditionalGeneration, tokenizer: T5Tokenizer, device: torch.device, input_prompt: str) -> str:
    inputs = tokenizer(input_prompt, padding=True, truncation=True, return_tensors="pt").to(device)
    
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=512)
    query = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return query

tokenizer = init_tokenizer()
model, device = load_model()

@app.route('/gen_sql', methods=['POST'])
def gen_sql_endpoint():
    data = request.json
    schema = data.get('schema')
    query = data.get('query')
    input_prompt = f"tables:\n{schema}\nquery:\n{query}"
    
    query = gen_sql(model, tokenizer, device, input_prompt)
    return jsonify({"query": query})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)