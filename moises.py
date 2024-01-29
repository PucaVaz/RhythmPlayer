import requests
import json
import time
import os
import wget

# CLASSE CRIADA PARA ORGANIZAR OS REQUESTS PARA A API DA MUSIC.AI DE FORMA MAIS SIMPLES E CONCENTRADA

class Moises:

    def __init__(self, api_key):
        self.api_key = api_key

    def limpar_tela(self):
        sistema_operacional = os.name

        if sistema_operacional == 'nt':  # Windows
            os.system('cls')
        else:  # Linux e macOS
            os.system('clear')

    def get_file_urls(self):  # obter um link que possa subir a musica e baixar
        headers = {
            'Authorization': self.api_key,
        }
        response = requests.get(
            "https://api.music.ai/api/upload", headers=headers) # request para o serviço de upload de arquivos da music.ai
        json_data = response.json()

        upload_url = json_data['uploadUrl']
        download_url = json_data['downloadUrl']
        return upload_url, download_url

    def upload(self, arquivo):  # subir a musica para o link obtido na funçao get_file_urls

        upload_url, download_url = self.get_file_urls()

        headers = {
            'Content-Type': 'audio/mpeg',
        }

        response = requests.put(
            upload_url, headers=headers, data=open(arquivo, 'rb')) # upa a musica para que o serviço da music.ai possa processar

        #print("FUNCAO UPLOAD")
        #print(response.status_code)

        return download_url # retorna o link para baixar o arquivo

    def download_arquivo(self, url, pasta, nome_arq): # funçao para baixar o vocal e o instrumental da musica depois de ter sido processado
        if not (os.path.exists(pasta)):
            os.mkdir(pasta)

        download = pasta + "\\" + nome_arq

        response = wget.download(url, download)

        #print("FUNCAO DOWNLOAD")
        #print(response)

        return response

    def separa_vocal(self, arquivo): # funçao principal para separar o vocal e o instrumental da musica

        self.limpar_tela()

        download_url = self.upload(arquivo) # upa a musica e retorna o link para baixar o arquivo
        # print("parametro arquivo (separa): ", arquivo) 
        nome_arq = os.path.basename(arquivo)

        headers = {
            'Authorization': self.api_key,
            'Content-Type': 'application/json'
        }
        
        job_name = "separa_vocal_" + nome_arq

        data = {
            "name": job_name,
            "workflow": "separa_vocal",
            "params": {
                "inputUrl": download_url
            }
        }

        response = requests.post(
            "https://api.music.ai/api/job", headers=headers, json=data) # request para o serviço de separar vocal da music.ai

        #print("FUNCAO SEPARA VOCAL")
        #print(response.status_code)
        #print(response.json())
        print("PREPARANDO SUA(S) MUSICA(S)...")

        while (1):

            job_url = "https://api.music.ai/api/job/" + response.json()['id'] 
            headers = {
                'Authorization': self.api_key,
            }
            response = requests.get(job_url, headers=headers) # request para checar se o job foi concluido
            if response.json()['status'] == 'SUCCEEDED':
                # baixa o arquivo
                #print(response.json())

                vocais = response.json()['result']['vocal'] # link para baixar o vocal
                resto = response.json()['result']['resto'] # link para baixar o instrumental

                path = os.getcwd() + "\\out\\" + nome_arq # path para salvar os arquivos baixados

                voc_path = self.download_arquivo(vocais, path, "vocal.wav") # baixa o vocal
                instr_path = self.download_arquivo(resto, path, "instr.wav") # baixa o instrumental

                if (os.path.exists(voc_path) and os.path.exists(instr_path)): # se os arquivos foram baixados com sucesso, retorna o path para os arquivos
                    #print("Arquivos baixados com sucesso")
                    paths = [voc_path, instr_path]
                    #print("paths: ", paths) 
                    self.limpar_tela()
                    print("A MUSICA FOI PROCESSADA")
                    time.sleep(0.5)
                    return paths 
                else:
                    print("Erro ao baixar arquivos")
                    return None

            elif response.json()['status'] == 'FAILED':

                print("JOB FAILED")
                break

            time.sleep(3) # espera 3 segundos para checar se o job foi concluido

    def ler_pasta(self, pasta): # funçao para ler uma pasta e separar o vocal e o instrumental de todas as musicas da pasta
        arquivos = os.listdir(pasta)

        arquivos_mp3 = [os.path.join(
            pasta, arquivo) for arquivo in arquivos if arquivo.lower().endswith('.mp3')]

        paths = {}

        for arquivo in arquivos_mp3:
            path = self.separa_vocal(arquivo)
            if path is None:
                print(
                    f"Erro ao separar vocal do arquivo {os.path.basename(arquivo)}")
            else:
                paths[os.path.basename(arquivo)] = path

        #print("paths: ", paths)
                
        self.limpar_tela()

        print("AS MUSICAS FORAM PROCESSADAS")

        return paths
