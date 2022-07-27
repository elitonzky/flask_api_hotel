<h1> Configurar Ambiente </h1>

python3 -m venv env

source env/bin/activate

pip install --upgrade pip 

pip install --upgrade pip setuptools

pip install -r requiriments.txt

<h1> Iniciar projeto </h1>

python app.py


# flask_api_hotel
API que disponibiliza hoteis em catálogo.

ENDPOINTS:

  GET
  http://127.0.0.1:5000/sites
  * Lista todos hoteis disponiveis

  GET
  http://127.0.0.1:5000/sites/{url}
  * Lista dados de um site com base na URL

  POST
  http://127.0.0.1:5000/sites/{url}
  * Cria site com base em sua URL

  DEL
  http://127.0.0.1:5000/sites/{url}
  * Deleta sites utilizando URL

HOTEIS:

  GET
  http://127.0.0.1:5000/hoteis/all
  * Lista todos hoteis cadastrados
  
  GET
  http://127.0.0.1:5000/hoteis/1
  * Busca Hotel pelo ID
  
  POST
  http://127.0.0.1:5000/hoteis/1
  * Cadastra Hotel pelo ID
  
  PUT
  http://127.0.0.1:5000/hoteis/1
  * Edita Hotel Pelo ID
  
  
  DEL
  http://127.0.0.1:5000/hoteis/1
  * Deleta Hotel pelo ID
  
 Usuários:
 
  GET
  http://127.0.0.1:5000/usuarios/{user_id}
  * Busca usuário pelo ID
  
  DEL
  /usuarios/{user_id}
  * Deleta Usuario pelo ID
  
  POST
  http://127.0.0.1:5000/cadastro
  * Cadastra usuário
  
Autenticação:

  POST
  http://127.0.0.1:5000/login
  * Loga usuário e retorna Token de acesso
  
  
  POST
  http://127.0.0.1:5000/logout
  * Logout usuário
  
  GET
  http://127.0.0.1:5000/confirmacao/1
  * Ativação de usuário via email
