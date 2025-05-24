# para formatar o texto português
# -*- coding: utf-8 -*-
import chromadb
import leitor
import time
from datetime import datetime
from chromadb.utils import embedding_functions
import os


def exibir_menu():
    """Exibe um menu de opções e retorna a escolha do usuário"""
    print('\n===== MENU DE OPÇÕES =====')
    print('1. Lista de modelos de embedding disponíveis')
    print('2. Ler arquivos PDF')
    print('3. Ler arquivos TXT')
    print('4. Ler arquivos DOCX')
    print('5. Ler todos os tipos de arquivos')
    print('6. Pesquisar')
    print('7. Eliminar Ficheiro')
    print('0. Sair')
    print('============================================')

    flag = True
    while flag:
        try:
            escolha = int(input("Digite sua opção: "))
            if 0 <= escolha <= 7:
                flag = False
            else:
                print("Opção inválida! Por favor, escolha um número entre 0 e 7.")
        except ValueError:
            print("Por favor, digite apenas números.")
    return escolha


def escolher_modelo(lista_de_modelos):
    """Permite ao usuário escolher um modelo de embedding da lista disponível"""
    print("\n===== MODELOS DE EMBEDDING DISPONÍVEIS =====")
    for i, modelo in enumerate(lista_de_modelos, start=1):
        print(f"{i}. {modelo}")
    print("============================================")
    
    while True:
        try:
            escolha = int(input("\nEscolha o número do modelo desejado: "))
            if 1 <= escolha <= len(lista_de_modelos):
                modelo_escolhido = lista_de_modelos[escolha]
                print(f"\nModelo escolhido: {modelo_escolhido}")
                return modelo_escolhido
            else:
                print(f"Opção inválida! Por favor, escolha um número entre 1 e {len(lista_de_modelos)}.")
        except ValueError:
            print("Por favor, digite apenas números.")


def adiciona_dados(collection, dados):
        # Adicionar ficheiros à coleção
        collection.add(
            documents=list(dados.values()),  # lista de ficheiros
            ids=[k for k in dados.keys()]    # ids dos ficheiros
        )
        print(f"Foram adicionados {len(dados)} ficheiros.")
        # Limpar o dicionário para evitar adicionar os mesmos ficheiros novamente
        dados.clear()


def pesquisar(collection):
    prompt = input("Digite o termo que deseja pesquisar: ")
    while True:
        try:
            n_resultados = int(input("Quantos resultados deseja obter:  "))
            if n_resultados <= 0:
                print("O número de resultados deve ser maior que zero.")
            else:
                break
        except ValueError:
            print("Por favor, escreva apenas números.")
            
    print("============================================\nA pesquisar...")

    # Iniciar cronómetro para medir o tempo de pesquisa
    start_time = time.perf_counter()
    # Realizar a pesquisa
    results = collection.query(
        query_texts=[prompt],    # o que o utilizador quer pesquisar                  
        n_results=n_resultados   # Número de resultados a serem retornados
    )
    # Parar o cronómetro
    end_time = time.perf_counter()
    query_time = end_time - start_time
    print(f"Modelo de Embedding: all-MiniLM-L6-v2\nTempo de pesquisa: {query_time:.4f} segundos")

    if results and results.get('documents') and len(results['documents'][0]) > 0:
        num_results = len(results['documents'][0])
        doc_text = []
        titles = []
        distance = []
        for i in range(num_results):
            doc_text.append(results['documents'][0][i])
            distance.append(results['distances'][0][i])
            doc_id_path = results['ids'][0][i]
            titles.append(os.path.basename(doc_id_path))
        
        leave = False
        while not leave:
            print(f"\n--- Pesquisas encontradas ---\n")   
            j = 0 
            for title in titles:
                print(f"--- Resultado {j+1} ---")
                print(f"Ficheiro: {title}")
                print(f"Distância de Similaridade: {distance[j]:.4f}\n")
                j += 1
                
            print("Escolha um resultado para ver o conteúdo ou escreva 0 para sair.")
            choice = input("Digite o número do resultado desejado: ")
            if choice == '0':
                leave = True
            else:
                try:
                    choice = int(choice) - 1  # Ajustar para índice 0
                    if 0 <= choice < num_results:
                        print("============================================\n")
                        print(f"Conteúdo do Resultado {choice + 1}:")
                        print(f"Ficheiro: {titles[choice]}")
                        print(f"{doc_text[choice]}\n\n")
                        
                    else:
                        print("Opção inválida!")
                except ValueError:
                    print("Por favor, escreva apenas números.")
    else:
        print("Nenhum resultado encontrado.")


def eliminar_dados(collection):
    ids = collection.get(include=[])
    for id in ids['ids']:
        print(id)
    id = input("Digite o ID do ficheiro que deseja eliminar: ")
    if id in ids['ids']:
        collection.delete(ids=[id])
        print(f"Ficheiro {id} eliminado com sucesso.")
    else:
        print(f"Ficheiro {id} não encontrado.")


def main():

    lista_de_modelos_de_embedding = ["all-MiniLM-L6-v2",
                                    "all-mpnet-base-v2",
                                    "multi-qa-mpnet-base-dot-v1",
                                    "multi-qa-MiniLM-L6-cos-v1",
                                    "paraphrase-multilingual-mpnet-base-v2",
                                    "paraphrase-albert-small-v2",
                                    "paraphrase-multilingual-MiniLM-L12-v2",
                                    "paraphrase-MiniLM-L3-v2",
                                    "distiluse-base-multilingual-cased-v1",
                                    "distiluse-base-multilingual-cased-v2"]

    # Conectar ao ChromaDB no container
    chroma_client = chromadb.Client(
        chromadb.config.Settings(chroma_server_host="chroma", chroma_server_http_port="8000")
    )
    
    # ERRO por alguma razão se usarmos isto não escreve a opção 2 no print do menu
    
    embedder = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
    )

    # cria a coleção "my_collection" 
    collection = chroma_client.get_or_create_collection(
        name="my_collection",
        embedding_function=embedder, # modelo de embedding
    )
     
    dados = {}  # Dicionário para armazenar os ficheiros lidos temporariamente

    escolha = None

    while escolha != 0:

        escolha = exibir_menu()
        
        match escolha:
            case 0:
                print("A sair do programa. Até logo!")
                break # sair do loop

            case 1:
                modelo_escolhido = escolher_modelo(lista_de_modelos_de_embedding)
                print(f"Modelo escolhido: {modelo_escolhido}")
            
            case 2:
                print("A ler ficheiros PDF...")
                leitor.extract_text(r"data\pdf", dados)
                adiciona_dados(collection, dados)
                
            case 3:
                print("A ler ficheiros TXT...")
                leitor.extract_text(r"data\txt", dados)
                adiciona_dados(collection, dados)
                
            case 4:
                print("A ler ficheiros DOCX...")
                leitor.extract_text(r"data\docx", dados)
                adiciona_dados(collection, dados)
                
            case 5:
                print("A ler todos os tipos de ficheiros...")
                leitor.extract_text(r"data\pdf", dados)
                leitor.extract_text(r"data\txt", dados)
                leitor.extract_text(r"data\docx", dados)
                adiciona_dados(collection, dados)
        
            case 6:
                pesquisar(collection)
                
            case 7:
                eliminar_dados(collection)
        

main()