import sys
from configparser import ConfigParser
from chatbot import chatBot

def main():
    config = ConfigParser()
    config.read('credentials.ini')
    api_key=config['gemini_ai'] ['API_KEY']

    chatbot = chatBot(api_key=api_key)
    chatbot.start_conversation()
    #chatbot.clear_conversation()

    print("Bem vindo ao BuscAI, seu buscador com base em IA para auxiliar em seu material de estudos")

    #print('{0}: {1}'.format(chatbot.CHATBOT_NAME, chatbot.history[-1]['text']))

    while True:
        user_input = input("Você:")
        if user_input.lower() =='sair':
            sys.exit("saindo...")
            break
        try:
            response = chatbot.send_prompt(user_input)
            print(f"{chatbot.CHATBOT_NAME}: {response}")
        except Exception as e:
            print(f"Error: {e}")
main()