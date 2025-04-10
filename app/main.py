import os
import chromadb
import leitor
from sentence_transformers import SentenceTransformer
from datetime import datetime
from chromadb.utils import embedding_functions

"""
TO-DO:
    - corrigir o erro de nuemro de embendings disponíveis ( começa em 2 enves de 1 )
    - corrigir o erro de escolher o embedding ( não está retornando o modelo escolhido )
    - corrigir o erro no menu de opções ( só a opção 4 funciona )

"""

def exibir_menu():
    """Exibe um menu de opções e retorna a escolha do usuário"""
    print("\n===== MENU DE OPÇÕES =====")
    print("1. Lista de modelos de embedding disponíveis")
    print("2. Ler arquivos PDF")
    print("3. Ler arquivos TXT")
    print("4. Ler arquivos DOCX")
    print("5. Ler todos os tipos de arquivos")
    print("0. Sair")
    print("=========================")
    
    while True:
        try:
            escolha = int(input("Digite sua opção: "))
            if 0 <= escolha <= 5:
                return escolha
            else:
                print("Opção inválida! Por favor, escolha um número entre 0 e 5.")
        except ValueError:
            print("Por favor, digite apenas números.")

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
     
    dic = {}

    escolha = None

    while escolha != 0:

        escolha = exibir_menu()
        
        if escolha == 0:
            print("Saindo do programa. Até logo!")
            break

        elif escolha == 1:
            modelo_escolhido = escolher_modelo(lista_de_modelos_de_embedding)
            print(f"Modelo escolhido: {modelo_escolhido}")
            continue
        
        elif escolha == 2:
            print("Lendo arquivos PDF...")
            leitor.extract_text(r"data\pdf", dic)
            print(f"Foram adicionados {len(dic)} documentos.")
            continue
            
        elif escolha == 3:
            print("Lendo arquivos TXT...")
            leitor.extract_text(r"data\txt", dic)
            print(f"Foram adicionados {len(dic)} documentos.")
            continue
            
        elif escolha == 4:
            print("Lendo arquivos DOCX...")
            leitor.extract_text(r"data\docx", dic)
            print(f"Foram adicionados {len(dic)} documentos.")
            continue
            
        elif escolha == 5:
            print("Lendo todos os tipos de arquivos...")
            leitor.extract_text(r"data\pdf", dic)
            leitor.extract_text(r"data\txt", dic)
            leitor.extract_text(r"data\docx", dic)
            print(f"Foram adicionados {len(dic)} documentos.")

        

            # cria o cliente ChromaDB
            chroma_client = chromadb.Client()

            sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="multi-qa-mpnet-base-dot-v1",
            )

            # cria a coleção "my_collection" 
            collection = chroma_client.get_or_create_collection(
                name="my_collection",
                embedding_function=sentence_transformer_ef,
                metadata={
                "description": "my first Chroma collection",
                "created": str(datetime.now())
                } 
            )
            
            # Adicionar documentos à coleção
            collection.add(
                documents=list(dic.values()),  # lista de documentos
                ids=[k for k in dic.keys()]    # ids dos documentos
            )

            termo_pesquisa = input("Digite o termo que deseja pesquisar: ")
            n_resultados = int(input("Quantos resultados deseja obter:  "))

            # Realizar a pesquisa
            results = collection.query(
                query_texts=[termo_pesquisa],  # o que o usuário quer pesquisar                  
                n_results=n_resultados         # Número de resultados a serem retornados
            )
            
            # Exibir resultados
            print("\nResultados da pesquisa:")
            print(results)


main()