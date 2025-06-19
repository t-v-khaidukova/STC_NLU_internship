# Запустить команду:
#   streamlit run app.py

import streamlit as st
from tools import Inf2Irregular, GrammarHelper

# Настройка страницы
st.set_page_config(page_title="GigaChat Tool Interface")

# Заголовок и описание
st.title("🛠️ GigaChat Tool Interface")
st.write("Введите вопрос, и система подберёт нужный инструмент и покажет вызов функции и результат.")

# Ввод вопроса
question = st.text_input("Ваш вопрос:")

# Кнопка выполнения
if st.button("Отправить"):
    if not question:
        st.error("Пожалуйста, введите вопрос.")
    else:
        # Выбор инструмента
        if "irregular" in question.lower():
            infinitive = question.strip().split()[-1]
            func_name = "Inf2Irregular.do_map"
            args = {"infinitive": infinitive, "form": 2}
            result = Inf2Irregular().do_map(infinitive, 2)
        else:
            noun = question.strip().rstrip('?')
            func_name = "GrammarHelper.explain_noun"
            args = {"noun": noun}
            result = GrammarHelper().explain_noun(noun)

        # Вывод вызова функции и результата
        st.subheader("Function Call")
        st.json({"name": func_name, "arguments": args})
        st.subheader("Response")
        st.write(result)