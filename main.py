from gigachat import GigaChat
from tools import Inf2Irregular, GrammarHelper, all_actual_tools
"""
Перечень функций:
 - неправильные глаголы (50%)
 - проверка согласованности употребления формы
 - гугл поиск (?)
 - яндекс поиск (?)
 -


LLM (Запрос + prompt + context)

prompt - тебе нужно решить задачку, вот тебе список доступных функций, если нужно

context :
inf2irregular - позволяет осуществить проверку регуляности глагола
inf2irregular(infinitive) - > bool, str

"""

class LLM_FC:
    def __init__(self, api_key='', max_tokens=4096):
        self.context = []
        self.model = GigaChat(
            base_url='https://gigachat.devices.sberbank.ru/api/v1',
            auth_url='https://ngw.devices.sberbank.ru:9443/api/v2/oauth',
            credentials=api_key,
            scope='GIGACHAT_API_CORP',
            model='GigaChat-Max',
            timeout=60.0,
            verbose=True,
            verify_ssl_certs=False,
            temperature=1e-8,
            profanity=False,
            max_tokens=max_tokens,
        )
        self.functions = []
        self.get_all_functions()

    def get_all_functions(self):
        self.functions.append(Inf2Irregular().description())
        self.functions.append(GrammarHelper().description())

    def has_fc(self, message):
        return 'function_call' in message[-1]["choices"][-1]['finish_reason']

    def fc_prerun_desc(self, message):
        func_to_be_called = message[-1]["choices"][-1]['message']['function_call']['name']
        its_args = message[-1]["choices"][-1]['message']['function_call']['arguments']
        return func_to_be_called, its_args

    def fc(self, msg):
        name = msg[-1]["choices"][-1]['message']['function_call']['name']
        # TODO continue

    def run(self, request: str):
        response = self.model.chat({
            "messages": [
                {
                    "role": "user",
                    "content": request  }
    ],
  "functions": self.functions})

if __name__ == '__main__':
    print('Hello!')