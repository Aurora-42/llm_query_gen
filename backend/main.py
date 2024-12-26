import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration

def init_tokenizer(model_name: str = 't5-small') -> T5Tokenizer:
    return T5Tokenizer.from_pretrained(model_name, legacy=False)

def load_model(model_name='cssupport/t5-small-awesome-text-to-sql'):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    model = model.to(device)
    model.eval()
    return model, device

def generate_sql(model: T5ForConditionalGeneration, tokenizer: T5Tokenizer, device: torch.device, input_prompt: str) -> str:
    inputs = tokenizer(input_prompt, padding=True, truncation=True, return_tensors="pt").to(device)
    
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=512)
    generated_sql = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return generated_sql

def main():
    # Initialize tokenizer and model
    tokenizer = init_tokenizer()
    model, device = load_model()

    # Database schema and query
    schema = "CREATE TABLE student_course_attendance (student_id VARCHAR); CREATE TABLE students (student_id VARCHAR)"
    query = "count the number of students who attended the course"
    input_prompt = "tables:\n" + schema + "\nquery:\n" + query

    # Generate SQL
    generated_sql = generate_sql(model, tokenizer, device, input_prompt)
    print(f"The generated SQL query is: {generated_sql}")

if __name__ == "__main__":
    main()