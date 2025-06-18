from gigachat import GigaChat
import datetime
import os

api_key = ''

model = GigaChat(
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
    max_tokens=36000,
)
req_sent = str(datetime.datetime.now())
# print(model.tokens_count(input_=["Я"], model="GigaChat-Pro"))
# file = model.upload_file(open("C:\\Users\\tomilov\\Downloads\\cat.jpg", "rb"))

inp_answer = 'Поставь глагол в скобках в правильную форму. We ___ football yesterday. (play)'

response = model.chat({
        "messages": [
            {
                "role": "user",
                "content": f"Твоя цель: из запроса определить начальную форму глагола и время, "
                           f"в котором он должен быть использован."
                           f"Шаги: "
                           f"1. Определи инфинитив."
                           f"2. По заданию и контексту примера определи форму глагола, "
                           f"которую нужно использовать в ответе."
                           f"Формат вывода:"
                           f"***INFINITIVE***: подставь сюда инфинитив ***"
                           f"***TENSE***: подставь сюда номер формы глагола (только 2 или 3) ***"
                           f"Пример: "
                           f"1."
                           f"Поставь глагол в скобках в правильную форму."
                           f"I ___ up at 5 a.m. (wake)"
                           f"Ответ:"
                           f"***INFINITIVE***: wake ***"
                           f"***TENSE***: 2 ***"
                           f"2."
                           f"Выбери нужную форму глагола из тех, что выделены курсивом."
                           f"He has *it\(broke/broken) his arm."
                           f"***INFINITIVE***: break ***"
                           f"***TENSE***: 3 ***"
                           "***"
                           "Задание: "
                           f"{inp_answer}"
                           "***"

                # "attachments": [file.id_],
            }
        ],
        # "temperature": 0.0
    })
resp_arr = str(datetime.datetime.now())

with open('usage_tom.txt', 'a') as f:
    f.write(f'req sent at {req_sent} | answer arrived at {resp_arr} | model {response.model} | usage {str(response.usage)}\n')
answer = response.choices[0].message.content
from grammar_graph_TIR.tools import Inf2Irregular
i2ir = Inf2Irregular('C:\\Users\\tomilov\\LightRAG\\grammar_graph_TIR\\irregular-verbs-de.csv')



inf, form = (answer.split('\n')[0].split('***INFINITIVE***:')[1].strip(),
             int(answer.split('\n')[1].split('******TENSE***:')[1].strip()))

print(f'Using the Inf2Irr Tool with args {inf, form}')
if i2ir.is_irregular(inf):
    part_of_prompt = f'{inf} has proper form to use in the case - {i2ir.do_map(inf, form)}'
else:
    part_of_prompt = f'{inf} is regular'

print(f'Inf2Irr Tool with args {inf, form} results in: {part_of_prompt}')
req_sent = str(datetime.datetime.now())
response = model.chat({
        "messages": [
            {
                "role": "user",
                "content": f"Твоя цель: на основе формулировки задания и результата поиска по таблице неправильных "
                           f"глаголов, выполнить задание. "
                           f"Формат вывода:"
                           f"***ANSWER***: подставь сюда ответ ***"
                           f"Пример: "
                           f"1."
                           f"Поставь глагол в скобках в правильную форму."
                           f"I ___ up at 5 a.m. (wake)"
                           f"Результат поиска:"
                           f"'wake has proper form to use in the case - woke'"
                           f"Ответ:"
                           f"***ANSWER***: I woke up at 5 a.m."
                           f"2."
                           f"Выбери нужную форму глагола из тех, что выделены курсивом."
                           f"He has *it\(broke/broken) his arm."
                           f"Результат поиска:"
                           f"'break has proper form to use in the case - broken'"
                           f"Ответ:"
                           f"***ANSWER***: He has broken his arm."
                           "***"
                           "Задание: "
                           f"{inp_answer}"
                           "***"
                           f"Результат поиска:"
                           f"{part_of_prompt}"
            }
        ],
    })
resp_arr = str(datetime.datetime.now())

with open('usage_tom.txt', 'a') as f:
    f.write(f'req sent at {req_sent} | answer arrived at {resp_arr} | model {response.model} | usage {str(response.usage)}\n')
final_answer = response.choices[0].message.content

print(final_answer)