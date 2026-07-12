# Consulta de Óbitos Receita Federal

Sistema básico em python para automatizar consulta de óbito através de CPF e data de nascimento no site da Receita Federal.

## Instalação das dependências

Acesse o site oficial do Python e faça a sua instalação: [https://www.python.org/downloads/](https://www.python.org/downloads/)

Após a instalação do python, baixe esse repositório em sua maquina, extraia os arquivos e abra o Prompt de Comandos na pasta onde se encontra o arquivo `main`.
No Prompt de Comandos, execute o seguinte comando para instalação das dependência necessárias: `pip install undetected-chromedriver pyautogui`.

## Configurações

Após isso, abra o arquivo data.csv e insira os dados dos que devem ter seus dados da seguinte forma:

```
CPF, DATA_NASC
12345678900,11012011
```

sendo o CPF e Data de Nascimento dos mesmos.

imagem demonstrativa: <br>
<img width="291" height="120" alt="image" src="https://github.com/user-attachments/assets/dc3c1040-c2d9-48f4-ad1e-e8708d098aeb" />

## Execução

No prompt de comandos, execute o seguinte comando: `py main.py`, e espere o código ser executado.

O código vai consular um por um e trazer os dados dentro um outro arquivo .csv: `resultados_consulta_obito.csv`, dentro desse arquivo vai estar contido todos os dados dos consultados, inclusive a data de óbito.

<img width="524" height="95" alt="image" src="https://github.com/user-attachments/assets/71768cde-596f-4269-ac12-4916b326d02c" />
<br>
<img width="958" height="137" alt="image" src="https://github.com/user-attachments/assets/6b61e003-c466-461b-ae44-7bfe9682fe22" />

## Observações

Burlar captchas de segurança, principalmente em sites governamentais como o da Receita Federal é um crime que infringe a Lei Geral de Proteção de Dados, de 2018 (LGPD). Portanto, use com total responsábilidade.

Eu não sou responsável por como e porque você utilizará desse sistema e nem pelos dados obtidos através do mesmo!

O sistema possuí um delay entre as consultas para evitar qualquer bloqueio.
