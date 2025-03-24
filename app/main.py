import os
import chromadb
import extractors
from sentence_transformers import SentenceTransformer

def main():
    print("Inicializando o projeto de análise de padrões de texto...")
    # Inicializar ChromaDB
    client = chromadb.PersistentClient("./chroma_db")
    
    try:
        # Tentar obter uma coleção existente
        collection = client.get_collection("documentos")
        print("Coleção existente encontrada.")
    except:
        # Criar uma nova coleção se não existir
        print("Criando nova coleção...")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Função para criar embeddings
        def embedding_function(texts):
            embeddings = model.encode(texts)
            return embeddings.tolist()
        
        collection = client.create_collection(
            name="documentos",
            embedding_function=embedding_function
        )
    
    print("Sistema inicializado com sucesso!")
    print(f"A coleção contém {collection.count()} documentos.")

if __name__ == "__main__":
    main()