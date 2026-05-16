from bs4 import BeautifulSoup
import re
import config as cfg
PADRAO_INICIO = re.compile(r"(?:Publicado em:\s*)?\d{2}/\d{2}/\d{4}(?:\s*(?:às\s*\d{2}h\d{2}|-\s*\d{2}h\d{2}\s*\|\s*Mercados|—\s*Nota à Imprensa|—\s*FGV IBRE))?\s*")
PADRAO_FIM = re.compile(r"(?i)(?:Leia o comunicado|Dados completos|Acesse a PNAD|Veja a cotação|Fonte:|Para acessar o relatório).*$")

def remover_metadados(texto: str,padrao_inicio=PADRAO_INICIO,padrao_fim=PADRAO_FIM) -> str:
    """Recebe um texto e o retorna sem metadados"""
    
    if not isinstance(texto, str):
        return ""
    
    #Remove metadados no inicio do texto.
    inicio_limpo = padrao_inicio.sub("", texto)
    
    #Remove metadados no final do texto.
    texto_limpo = padrao_fim.sub("", inicio_limpo)
    
    return texto_limpo

def limpar_texto(texto: str, min_palavras: int = cfg.MIN_PALAVRAS) -> str: 
    """
    Processa o texto bruto: remove HTML, metadados, espaços extras e 
    descarta textos com conteúdo insuficiente.
    """
    # Verifica se o texto é string ou é uma string vazia.
    if not isinstance(texto, str) or not texto.strip():
        return None
    
    # Remove Tags e resolve Entidades HTML.
    soup = BeautifulSoup(texto, "html.parser")
    texto_sem_html = soup.get_text(separator=" ")
    
    # Chama a função para remover os metadados
    texto_sem_meta = remover_metadados(texto_sem_html)
    
    # Garante que não sobrou nenhum espaço duplo após remover os metadados
    texto_limpo = re.sub(r'\s+', ' ', texto_sem_meta).strip()
    
    # Junta um ponto final que tenha ficado solto.
    texto_limpo = re.sub(r'\s+\.?$', '.', texto_limpo)
    
    # Retorna None caso o texto não tenha uma quantidade mínima de palavras. 
    if len(texto_limpo.split()) < min_palavras:
        return None
        
    return texto_limpo
