@echo off
title Motor de Busca Semantico - FGV IBRE
color 0F

echo ===================================================
echo     Iniciando o ambiente aguarde um instante...
echo ===================================================
echo.

if not exist ".venv\Scripts\activate" (
    echo [SETUP INICIAL] Ambiente virtual nao encontrado. Criando agora...
    python -m venv .venv
    echo [SETUP INICIAL] Instalando as dependencias do requirements.txt...
    call .venv\Scripts\activate
    pip install -r requirements.txt
    echo [SETUP INICIAL] Tudo pronto!
    echo.
)

REM Silencia Warnings e Mensagens de erro
set HF_HUB_DISABLE_SYMLINKS_WARNING=1
set HF_HUB_DISABLE_WARNINGS=1
set HF_HUB_DISABLE_PROGRESS_BARS=1
set TRANSFORMERS_VERBOSITY=error
set TF_CPP_MIN_LOG_LEVEL=3

REM Ativa o ambiente virtual
call .venv\Scripts\activate

REM Executa o arquivo principal
python main.py

REM Mantem a janela aberta se o programa for encerrado
pause