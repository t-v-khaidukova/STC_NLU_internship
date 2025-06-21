# Запустить команду:
#   streamlit run app.py

import streamlit as st
from tools import Inf2Irregular, GrammarHelper
from main import LLM_FC

api_key = st.text_input("🔐 Введите API API-ключ", type="password")
# Настройка страницы
st.set_page_config(page_title="GigaChat Tool Interface")

# Заголовок и описание
st.title("🛠️ GigaChat Tool Interface")
st.write("Введите вопрос, и система подберёт нужный инструмент и покажет вызов функции и результат.")

# Ввод вопроса
question = st.text_input("Ваш вопрос:")


max_num_fc = 5
# Кнопка выполнения
if st.button("Отправить"):
    if not question or not api_key:
        st.error("❗ Введите тему и API-ключ.")
    else:
        main_llm = LLM_FC(api_key=api_key)
        with st.spinner("🧠 Работа GrammarTool..."):
            result = question
            for _ in range(max_num_fc):
                result = main_llm.run(result)
                if main_llm.has_fc(result):
                    func_name, args = main_llm.fc_prerun_desc(result)
                    result = main_llm.fc(result)
                    st.subheader("Function Call")
                    st.json({"name": func_name, "arguments": args})
                    st.subheader("Response")
                    st.write(result)
                else:
                    break
        # Вывод вызова функции и результата
        st.subheader("Response")
        st.write(result)

        # # Выбор инструмента
        # if "irregular" in question.lower():
        #     infinitive = question.strip().split()[-1]
        #     func_name = "Inf2Irregular.do_map"
        #     args = {"infinitive": infinitive, "form": 2}
        #     result = Inf2Irregular().do_map(infinitive, 2)
        # else:
        #     noun = question.strip().rstrip('?')
        #     func_name = "GrammarHelper.explain_noun"
        #     args = {"noun": noun}
        #     result = GrammarHelper().explain_noun(noun)


