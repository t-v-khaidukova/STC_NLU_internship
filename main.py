from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole, Function
import json
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
        print('Creating tools')
        self.functions.append(Inf2Irregular().description())
        self.functions.append(GrammarHelper().description())

    def has_fc(self, message):
        return 'function_call' in message[-1]["choices"][-1]['finish_reason']

    def fc_prerun_desc(self, message):
        func_to_be_called = message[-1]["choices"][-1]['message']['function_call']['name']
        its_args = message[-1]["choices"][-1]['message']['function_call']['arguments']
        return func_to_be_called, its_args

    def fc(self, message):
        # name = message[-1]["choices"][-1]['message']['function_call']['name']
        # TODO continue
        # 1. Получить имя и аргументы функции
        func_name, func_args = self.fc_prerun_desc(message)
        # 2. Найти соответствующий callable в all_actual_tools
        tools_map = all_actual_tools()
        if func_name not in tools_map:
            # Если функция неизвестна — кидаем ошибку или возвращаем сообщение
            message.append({
                'role': 'system',
                'content': f"Ошибка: неизвестная функция '{func_name}'"
            })
            return message
        # 3. Вызываем функцию
        try:
            result = tools_map[func_name](**func_args)
        except Exception as e:
            # Обработка ошибок в вызове функции
            message.append({
                'role': 'system',
                'content': f"Ошибка при выполнении функции '{func_name}': {str(e)}"
            })
            return message
        # 4. Добавляем сообщение от роли 'function' с результатом
        message.append({
            'role': 'function',
            'name': func_name,
            'content': str(result)
        })
        return message

    def run(self, request: str):
        from gigachat.models import Chat, Messages, MessagesRole, Function, FunctionParameters
        search = Function(
            name="duckduckgo_search",
            description="""Поиск в DuckDuckGo.
        Полезен, когда нужно ответить на вопросы о текущих событиях.
        Входными данными должен быть поисковый запрос.""",
            parameters=FunctionParameters(
                type="object",
                properties={"query": {"type": "string", "description": "Поисковый запрос"}},
                required=["query"],
            ),
        )
        payload = Chat(
            messages=[Messages(role=MessagesRole.USER, content=request)],
            functions=self.functions,
            function_call='auto',
        )
        response = self.model.chat(payload)

if __name__ == '__main__':
    print('Hello!')