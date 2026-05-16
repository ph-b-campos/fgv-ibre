# Desafio Técnico — Estágio em Ciência de Dados
**FGV IBRE — Instituto Brasileiro de Economia**

---

## Instruções de uso da Aplicação:
- Execute o arquivo 'executar.bat'.
- Espere alguns instantes.
- Busque por noticias utilizando palavras chave ou eventos. ex: inflação, desemprego, taxa de juros, aumento ipca.
- Evite buscar por siglas de índices como ICC, IPA.
- Para encerrar o programa digite sair e feche a aba.

--- 
## Raciocínio no desenvolvimento do projeto:
---
### Etapa 1 - Limpeza e Tratamento de Texto
- Utilizei a biblioteca BeautifulSoup para estruturar o texto e remover Tags e Entidades HTML, por conta do seu 'html.parser'.
- Utilizei Regex para remover metadados (datas, links, nomes de revistas).
- Retirei espaços repetitivos.
- Deletei textos que tinham menos que 15 palavras.
- Salvei os dados na mesma pasta '\dados' como 'noticias_limpas.json'.

### Etapa 2 - Geração de Embeddings
- Escolhi o modelo 'paraphrase-multilingual-MiniLM-L12-v2' da biblioteca Sentence Transformers por estar em portugês e por ser um modelo leve.

### Etapa 3 - Motor de Busca Semântico
- Fiz uma interface em que o usuário deve interagir e realizar buscas sem precisar abrir um terminal iniciar um ambiente virtual e rodar o código manualmente.
- Para realizar a busca semântica, a frase do usuário é mapeada em um embeding e utilizei a função semantic search tambem da biblioteca sentence_transformers para obter a semelhança entre a frase buscada e os textos das noticias.
- Optei por utilizar um limiar que da um limite mínimo de semelhança para o funcionamento da busca, com objetivo de melhorar a experiência do usuário que pode pesquisar sobre um assunto que não é abrangido pelo corpus e receber textos que não tem relação semântica com a busca.
- Caso nenhum texto presente tenha essa semelhança mínima o programa avisa ao usuário.
- Optei tambem por não apresentar mais de 5  textos, evitando uma poluição visual.


## Avaliação qualitativa
--- 
O projeto tem documentação para todas as funções e comentários explicando o que acontece em cada parte do código. Apliquei o princípio da responsabilidade única isolando as regras do projeto: criei um arquivo config.py para armazenar variáveis de controle (como mínimo de palavras e semelhança mínima).Além disso, separei as funções de tratamento em um módulo próprio (data_cleaning.py), deixando o código mais conciso e legível. Por fim, para usar a aplicação não é necessário que o usuário saiba ativar um ambiente virtual e rodar o código, o script executar.bat permite que usuários não tecnicos consigam acessar a aplicação apenas seguindo as simples instruções de uso. Apesar de algumas limitações, o resultado final me agradou ficou simplês eficiente e respeitou as boas práticas de programação.
### Limitações da Aplicação
- Meu programa não retorna resultados caso você busque por algum índice específico ex:(ICC,IPA), mesmo que o índice esteja presente no texto, isso é uma consequência do limiar que eu apliquei, eu optei por manter o limiar conscientemente dessa limitação, pois eu prefiro ter essa limitação do que devolver uma busca não precisa e que não tem relação com o tema pesquisado.

- Caso o usuário quisesse ver mais de 5 textos relacionados com a busca e eles cumprissem os requisitos o usuário não consegue acessar, isso foi uma consequência da escolha de apresentar apenas 5 para o usuário evitando a poluição visual.
