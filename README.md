Passo a passo para iniciar o ambiente de desenvolvimento da sua máquina.
1-verificar se você ja tem o git e o python instalado na sua máquina(caso não tenha, sera nessecário instalar).
2-Realizar o clone do repósitório em sua máquina utilizando o git clone https://github.com/Hu3cx/BuscAI.git.
3-Após ter o ambiente clonado em sua máquina, execute o o terminal do seu compilador(de preferencia do vscode) ou terminal do windows.
4-com o terminal do vscode aberto, caso as bibliotecas não estejam identificadas, executar o comando "pip install flask" e "pip install google-generativeai"
5-No terminal acesse a pasta "scripts" que esta dentro de buscai>venv>scripts e executar o ambiente virtual com o comando .\activate


6-Em seguida, após todos os complementos estaremm configurados e intalados, sera necessário abrir o arquivo app.py e alterar a linha 3 para "from chatbot import chatBot" 
motivo: o ambiente esta configurado para nossa produção/hospedagem *ESTE PASSO É MUITO IMPORTANTE*;(caso tenha algum arquivo referenciando o caminho completo como por exemplo "from buscai.app.app" sera necessário alterar para somente "from app" para ajustar o caminho correto)

7- execute com a tecla F5 com o arquivo app.py aberto no compilardor
8 - o terminal deve dar uma mensagem assim: * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 907-350-181
9- execute o endereço de ip(localhost) em seu navegador de preferencia para execuatar a aplicação em ambiente.
