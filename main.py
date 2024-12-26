import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Init Tokenizer from Hugging Face Transformers library
tokenizer = T5Tokenizer.from_pretrained('t5-small', legacy=False)

# load model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = T5ForConditionalGeneration.from_pretrained('cssupport/t5-small-awesome-text-to-sql')
model = model.to(device)
model.eval()

def generate_sql(input_prompt):
    inputs = tokenizer(input_prompt, padding=True, truncation=True, return_tensors="pt").to(device)
    
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=512)
    generated_sql = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return generated_sql

# database schema
schema = "CREATE TABLE student_course_attendance (student_id VARCHAR); CREATE TABLE students (student_id VARCHAR)"
# query to generate SQL
query = "count the number of students who attended the course"

input_prompt = "tables:\n" + schema + "\nquery:\n" + query

generated_sql = generate_sql(input_prompt)

print(f"The generated SQL query is: {generated_sql}")