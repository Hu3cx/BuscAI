import google.generativeai as genai
import re
from datetime import datetime
from app import db

class genAIException(Exception):
    """GENAI classe base"""

class Buscas(db.Model):
    __tablename__ = 'Buscas'
    id_busca = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.id'))  
    consulta = db.Column(db.String(255))
    resultado = db.Column(db.Text)
    data_hora_busca = db.Column(db.DateTime, default=datetime.now)

class ChatBot:
    CHATBOT_NAME = 'Buscai'

    def __init__(self, api_key, db):
        self.genai = genai
        self.genai.configure(api_key=api_key)
        self.model = self.genai.GenerativeModel('gemini-pro')
        self.conversation = None
        self._conversation_history = []
        self.db = db

        self.preload_conversation()
        self.start_conversation()  # Inicia a conversa durante a inicialização

    def clear_conversation(self):
        self.conversation = self.model.start_chat(history=[])

    def start_conversation(self):
        self.conversation = self.model.start_chat(history=self._conversation_history)

    def _construct_message(self, text, role='user'):
        return {
            'role': role,
            'parts': text
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
                self._construct_message('Forneça SEMPRE muito bem detalhado o tópico solicitado, e NUNCA esquecer de incluir citações de fontes confiáveis e links que funcionam relacionado ao tópico do YouTube.'),
            ]

    def salvar_busca(self, termo, resultado, usuario_id):
        try:
            # Criando uma nova busca associada ao usuário
            busca = Buscas(id_usuario=usuario_id, consulta=termo, resultado=resultado)
            self.db.session.add(busca)
            self.db.session.commit()
        except Exception as e:
            self.db.session.rollback()
            raise genAIException(f'Erro ao salvar a busca: {str(e)}')


    def send_prompt(self, prompt, user, temperature=1):
     if temperature < 0 or temperature > 1:
         raise genAIException('A temperatura deve estar entre 0 e 1')
     if not prompt:
         raise genAIException('O prompt não pode estar vazio')
     try:
         response = self.conversation.send_message(
             content=prompt,
             generation_config=self._generation_config(temperature),
         )
         response.resolve()
         formatted_response = self.format_response(response.text)
         usuario_id = user.id
         self.salvar_busca(termo=prompt, resultado=formatted_response, usuario_id=usuario_id)
         return formatted_response
     except Exception as e:
         raise genAIException(str(e))
     
    def format_response(self, response_text):
      # Remover os asteriscos e formatar negrito com tags <strong>
      response_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', response_text)

      paragraphs = response_text.split('\n')
      formatted_response = ''
      for paragraph in paragraphs:
          # Identificar e formatar citações
          if paragraph.startswith('>'):
              formatted_response += f'<blockquote>{paragraph[1:].strip()}</blockquote>'
          # Identificar e formatar listas
          elif paragraph.startswith('*'):
              formatted_response += f'<ul><li>{paragraph[1:].strip()}</li></ul>'
          # Identificar e formatar links
          elif 'http://' in paragraph or 'https://' in paragraph:
              words = paragraph.split()
              formatted_paragraph = ' '.join(
                  f'<a href="{word}" target="_blank">{word}</a>' if word.startswith('http') else word
                  for word in words
              )
              formatted_response += f'<p>{formatted_paragraph}</p>'
          else:
              formatted_response += f'<p>{paragraph}</p>'

      # Consolidar listas em uma única <ul>
      formatted_response = re.sub(r'</ul>\s*<ul>', '', formatted_response)

      return formatted_response

    @property
    def history(self):
        conversation_history = [
            {'role': message.role, 'text': message.parts[0].text} for message in self.model.history
        ]
        return conversation_history 
