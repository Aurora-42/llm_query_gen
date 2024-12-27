# Gera querys a partir de linguagem natural
Um projeto de teste para praticar o uso de IA com Querys

# Modelo usado
  [T5-satts](https://huggingface.co/cssupport/t5-small-awesome-text-to-sql)

# Instalação
``` shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

# Como executar o projeto
``` shell
sh run.sh
```
Na primeira execução ele faz o download no modelo
e armazena em cache

# Modo de uso (temporario)
 Faça uma requisição post com o seguinte body (usando postman ou insomnia)
 no Endpoint /gen_sql
```
    "schema": "CREATE TABLE student_course_attendance (student_id VARCHAR); CREATE TABLE students (student_id VARCHAR);",
    "query": "count the number of students who attended the course"
```
 O modelo recebe um input unico em forma de string no seguinte formato
 ```c
 "tables:\n" + schema + "\nquery:\n" + query
 ```
 A variavel "schema" é um snippet do "create" das tabelas, apenas para nivel de contexto
 - como por exemplo
 ```python
{
     "schema" = "CREATE TABLE student_course_attendance (student_id VARCHAR);\
                  CREATE TABLE students (student_id VARCHAR);"
} 
 ```
 A variavel "Query" é simplismente o objetivo da query a ser produzida
 - Como por exemplo
 ```python
{
    "query" = "count the number of students who attended the course"
}

```
O Resultado deve ser:
``` shell
    SELECT COUNT(*) FROM students AS T1 JOIN student_course_attendance AS T2 ON T1.student_id = T2.student_id GROUP BY T1.student_id
```
