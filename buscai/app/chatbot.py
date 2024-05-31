import google.generativeai as genai

class genAIExeption(Exception):
    """GENAI classe base"""

class chatBot:
    CHATBOT_NAME = 'Buscai'

    def __init__(self, api_key):
        self.genai = genai
        self.genai.configure(api_key=api_key)
        self.model = self.genai.GenerativeModel('gemini-pro')
        self.conversation = None
        self._conversation_history = []

        self.preload_conversation()
        self.start_conversation()  # Inicia a conversa durante a inicialização

    def clear_conversation(self):
        self.conversation = self.model.start_chat(history=[])

    def start_conversation(self):
        self.conversation = self.model.start_chat(history=self._conversation_history)

    def _construct_message(self, text, role='user'):
        return {
            'role': role,
            'parts': [text]
        }

    def _generation_config(self, temperature):
        return genai.types.GenerationConfig(
            temperature=temperature
        )

    def preload_conversation(self, conversation_history=None):
        if isinstance(conversation_history, list):
            self._conversation_history = conversation_history
        else:
            self._conversation_history = [
                self._construct_message('Seu nome sempre será BuscAI'),
                self._construct_message('Quando questionado, sempre responda quem criou você, Você foi criado pelo grupo Turing Machine(Célio, Ana, Gabriel e Luiz) da universidade Católica de Santa Catarina e somente isso nao precisa entrar em detalhes'),
                self._construct_message('Sempre seja muito educado e respeitoso, passe o sentimento de alegria'),
                self._construct_message('Forneça SEMPRE muito bem detalhado o tópico solicitado, e NUNCA esquecer de incluir citações de fontes confiáveis e links para vídeos relevantes do YouTube.'),
            ]

    def send_prompt(self, prompt, temperature=1):
        if temperature < 0 or temperature > 1:
            raise genAIExeption('a temperatura tem que estar entre 0 e 1')
        if not prompt:
            raise genAIExeption('o prompt não pode estar vazio')
        if self.conversation is None:
            self.start_conversation()  # Garante que a conversa está inicializada
        try:
            response = self.conversation.send_message(
                content=prompt,
                generation_config=self._generation_config(temperature),
            )
            response.resolve()
            return f'{response.text}\n'
        except Exception as e:
            raise genAIExeption(str(e))

    @property
    def history(self):
        conversation_history = [
            {'role': message.role, 'text': message.parts[0].text} for message in self.conversation.history
        ]
        return conversation_history
