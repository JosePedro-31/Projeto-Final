import os
import sys
import chromadb
import leitor
from datetime import datetime
from chromadb.utils import embedding_functions


def exibir_menu():
    """Exibe um menu de opções e retorna a escolha do usuário"""
    print('\n===== MENU DE OPÇÕES =====')
    print('1. Lista de modelos de embedding disponíveis')
    print('2. Ler arquivos PDF')
    print('3. Ler arquivos TXT')
    print('4. Ler arquivos DOCX')
    print('5. Ler todos os tipos de arquivos')
    print('0. Sair')
    print('=========================')

    flag = True
    while flag:
        try:
            escolha = int(input("Digite sua opção: "))
            if 0 <= escolha <= 5:
                flag = False
            else:
                print("Opção inválida! Por favor, escolha um número entre 0 e 5.")
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

    # cria o cliente ChromaDB
    chroma_client = chromadb.Client()
    
    # ERRO por alguma razão se usarmos isto não escreve a opção 2 no print do menu
    '''
    embedder = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2",
    )
    '''

    # cria a coleção "my_collection" 
    collection = chroma_client.get_or_create_collection(
        name="my_collection",
        metadata={
        "description": "my first Chroma collection",
        "created": str(datetime.now())
        } 
    )
     
    dic = {}

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
                leitor.extract_text(r"data\pdf", dic)
                print(f"Foram adicionados {len(dic)} ficheiros.")
                                
            case 3:
                print("A ler ficheiros TXT...")
                leitor.extract_text(r"data\txt", dic)
                print(f"Foram adicionados {len(dic)} ficheiros.")
                
            case 4:
                print("A ler ficheiros DOCX...")
                leitor.extract_text(r"data\docx", dic)
                print(f"Foram adicionados {len(dic)} ficheiros.")
                
            case 5:
                print("A ler todos os tipos de ficheiros...")
                leitor.extract_text(r"data\pdf", dic)
                leitor.extract_text(r"data\txt", dic)
                leitor.extract_text(r"data\docx", dic)
                print(f"Foram adicionados {len(dic)} ficheiros.")

        
        
        # Adicionar ficheiros à coleção
        collection.add(
            documents=list(dic.values()),  # lista de ficheiros
            ids=[k for k in dic.keys()]    # ids dos ficheiros
        )

        prompt = input("Digite o termo que deseja pesquisar: ")
        n_resultados = int(input("Quantos resultados deseja obter:  "))

        # Realizar a pesquisa
        results = collection.query(
            query_texts=[prompt],    # o que o utilizador quer pesquisar                  
            n_results=n_resultados   # Número de resultados a serem retornados
        )
        
        # Exibir resultados
        print("\nResultados da pesquisa:")
        print(results)


main()