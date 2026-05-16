import pandas as pd
from data_cleaning import limpar_texto
from sentence_transformers import SentenceTransformer,util
import config as cfg
import os
import warnings
import logging
# Silencia avisos do Python e do Hugging Face
warnings.filterwarnings("ignore")
logging.getLogger("huggingface_hub").setLevel(logging.ERROR)
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

def busca_semantica(query,modelo,embedding_corpus,semelhanca_min = cfg.THRESHOLD_BUSCA,max_artigos = cfg.MAX_ARTIGOS):
    """ 
    Realiza uma busca no embedding dos textos com base na semelhança semântica 
    com um limiar de semelhança mínimo e retorna uma quantidade máxima de textos
    que tem relação semântica com a busca, caso nenhum texto tenha a semelhança 
    mínima retorna uma lista vazia.
    """

    # Faz o embedding da frase de busca
    query_embedding = modelo.encode(query, convert_to_tensor=True)

    # Projeta a busca no nosso embedding do corpus e filtra um numero máximo
    hits = util.semantic_search(query_embedding, embedding_corpus, top_k=max_artigos)[0]

    # Realiza um filtro de semelhança mínima
    resultados_filtrados = [hit for hit in hits if hit['score'] >= semelhanca_min]

    # Caso nenhum texto passe no filtro retorna uma lista vazia
    if len(resultados_filtrados) == 0:
        return []

    return resultados_filtrados

def main():
    # Carrega os dados em um DataFrame do pandas.
    noticias_brutas = pd.read_json('dados/noticias_brutas.json')

    # Etapa 1: Realiza a limpeza de dados transformando o texto bruto em texto estruturado.
    noticias_brutas['texto'] = noticias_brutas['texto'].apply(limpar_texto)

    # Remove as linhas que não tiveram o mínimo de palavras desejado.
    noticias_brutas.dropna(subset=['texto'], inplace=True)

    # Salva os dados limpos em um json.
    noticias_brutas.to_json(cfg.CLEAN_DATA_PATH, orient='records', force_ascii=False, indent=4)

    # Etapa 2: Geração do embedding do corpus.

    # Instancia o modelo escolhido
    model = SentenceTransformer(cfg.MODELO)

    # Extrai a coluna texto do dataframe e salva em uma lista
    textos = noticias_brutas['texto'].tolist()

    # Cria um embedding a partir dessa lista
    embeddings = model.encode(textos)
    
    # Etapa 3: Busca semântica.
    query = ''
    print("Iniciando busca semantica...\n")
    
    while True:
        print("Digite 'sair' para encerrar.\n")
        query = input('Tema desejado : ')
        if query.lower() == 'sair':
            print("Encerrando o sistema. Até logo!")
            break

        # Realiza a busca semantica
        resultados_filtrados = busca_semantica(query, model,embeddings)

        print('Resultados : \n')

        # Caso não ache nenhuma noticia relevante avisa ao usuário
        if len(resultados_filtrados) == 0:
            print("Nenhuma notícia relevante encontrada para esta busca.\n")
            continue

        # Printa e retorna as noticias para o usuário
        for i, hit in enumerate(resultados_filtrados):
            idx = int(hit['corpus_id'])
            texto_recuperado = textos[idx]
            print(texto_recuperado,'\n')
        



if __name__ == "__main__":
    main()