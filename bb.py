import requests

# Define as variáveis
server_url = 'https://nome_do_servidor:porta'
project_key = 'chave_do_projeto'
repository_slug = 'slug_do_repositorio'
username = 'seu_usuario'
password = 'sua_senha'

# Define o endpoint para obter informações sobre os pull requests
endpoint = f'/rest/api/1.0/projects/{project_key}/repos/{repository_slug}/pull-requests'

# Define os parâmetros da solicitação
params = {
    'state': 'OPEN'
}

# Faz a solicitação GET
response = requests.get(server_url + endpoint, auth=(username, password), params=params)

# Verifica se a solicitação foi bem sucedida
if response.status_code == 200:
    # Obtém os dados da resposta em JSON
    pr_data = response.json()['values']
    
    # Imprime informações sobre cada pull request
    for pr in pr_data:
        print(f'Pull request {pr["id"]}: {pr["title"]}')
else:
    print(f'Erro ao obter pull requests. Status de resposta: {response.status_code}')
