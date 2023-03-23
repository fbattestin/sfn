import requests

class ControlMJobs:
    def __init__(self, url, user, password):
        self.url = url
        self.user = user
        self.password = password

    def get_failed_jobs(self, folders):
        # envia uma solicitação HTTP GET para o endpoint do Control-M
        response = requests.get(self.url, auth=(self.user, self.password))
        # verifica se a solicitação foi bem-sucedida
        if response.status_code == 200:
            # processa os dados JSON da resposta
            data = response.json()
            # filtra os jobs que falharam apenas nas pastas especificadas
            failed_jobs = [job for job in data['jobs'] if job['status'] == 'failed' and job['folder'] in folders]
            # retorna uma lista dos jobs que falharam
            return failed_jobs
        else:
            # retorna uma mensagem de erro se a solicitação não foi bem-sucedida
            return f"Erro {response.status_code}: Não foi possível acessar o endpoint {self.url}"

    def get_folders(self):
        # envia uma solicitação HTTP GET para o endpoint do Control-M que retorna informações sobre todas as pastas disponíveis
        response = requests.get(f"{self.url}/folders", auth=(self.user, self.password))
        # verifica se a solicitação foi bem-sucedida
        if response.status_code == 200:
            # processa os dados JSON da resposta
            data = response.json()
            # extrai os nomes das pastas
            folders = [folder['name'] for folder in data['folders']]
            # retorna a lista de nomes de pastas
            return folders
        else:
            # retorna uma mensagem de erro se a solicitação não foi bem-sucedida
            return f"Erro {response.status_code}: Não foi possível acessar o endpoint {self.url}/folders"


# cria uma instância da classe ControlMJobs
controlm = ControlMJobs('http://exemplo.com/api/jobs', 'user', 'password')

# chama a função get_folders para obter todos os nomes de pastas existentes
folders = controlm.get_folders()

# imprime a lista de pastas
print(folders)


# cria uma instância da classe ControlMJobs
controlm = ControlMJobs('http://exemplo.com/api/jobs', 'user', 'password')

# especifica as pastas que deseja filtrar
folders = ['Folder1', 'Folder2', 'Folder3', 'Folder4']

# chama o método get_failed_jobs para obter os jobs que falharam nessas pastas
failed_jobs = controlm.get_failed_jobs(folders)

# imprime os jobs que falharam
for job in failed_jobs:
    print(job['name'], job['start_time'], job['end_time'], job['error_message'])
