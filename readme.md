# Gera querys apartir de linguagem natural
Um projeto de teste para praticar o uso de IA com Querys

# modelo usado
  cssupport t5-small-awesome-text-to-sql 

# Instalação
``` shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

# Modo de uso (temporario)
 O modelo recebe um input unico em forma de string no seguinte formato
 ```c
 "tables:\n" + schema + "\nquery:\n" + query
 ```
 A variavel "schema" é um snippet do "create" das tabelas, apenas para nivel de contexto
 - como por exemplo
 ```python
    schema = """
    CREATE TABLE employees (
        id INT PRIMARY KEY,
        name VARCHAR(100),
        salary DECIMAL(10, 2)
    );
    CREATE TABLE departments (
        id INT PRIMARY KEY,
        name VARCHAR(100)
    );
"""
 ```
 A variavel "Query" é simplismente o objetivo da query a ser produzida
 - Como por exemplo
 ```python
    query = "count the number of students who attended the course"
```
