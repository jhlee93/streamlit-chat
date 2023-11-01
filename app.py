import streamlit as st
from st_pages import show_pages, Page, add_page_title

from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.callbacks.streamlit import StreamlitCallbackHandler

import re
import clipboard
import prompts


add_page_title(layout='wide')
show_pages(
    [
        Page('app.py', 'Prompt Test', '💬'),
        Page('pages/chat_history.py', 'Chat History', '📝')
    ]
)

ss = st.session_state

# ----- Openai API Key
if 'openai_api_key' in st.secrets:
    ss.openai_api_key = st.secrets.openai_api_key
else:
    ss.openai_api_key = st.sidebar.text_input(
    'OpenAI API Key', type="password", placeholder='sk-***')

# ----- LLM Select
ss.model_name = st.sidebar.selectbox(
    'Model', ('gpt-3.5-turbo', 'gpt-3.5-turbo-16k', 'gpt-4'))

# ----- Temperature
ss.temperature = st.sidebar.slider(
    'Temperature', value=1.0, min_value=0.0, max_value=2.0, step=0.1)

# ----- Chat History
if 'chat_history' not in ss:
    ss.chat_history = []
else:
    if len(ss.chat_history) > 20:
        ss.chat_history = ss.chat_history[-20:]

# ----- Select Prompt
prompt_dict = {
    'Custom': prompts.custom,
    'Report-Writer': prompts.report,
    'Proposal-Writer': prompts.propsal,
    'Python-Assistant': prompts.python_assistant,
    'Prompt-Generator': prompts.prompt_generator,
}
selected_prompt_key = st.selectbox('프롬프트 선택', prompt_dict.keys(), index=0)
selected_prompt = prompt_dict[selected_prompt_key]

with st.expander("프롬프트", expanded=True):
    prompt_template = st.text_area(
        " ", value=selected_prompt,
        height=int(len(selected_prompt.split('\n')) * 30)
        )

def on_copy_click(text):
    clipboard.copy(text)

def get_prompt_inputs(prompt_text):
    return re.findall(r'\{(\w+)\}', prompt_text)

def run_chain(data, container):
    chain = LLMChain(
        llm=ChatOpenAI(
            model_name=ss.model_name, temperature=ss.temperature,
            streaming=True, openai_api_key=ss.openai_api_key),
        prompt=PromptTemplate.from_template(prompt_template),
        verbose=False
    )
    manager = StreamlitCallbackHandler(container)
    response = chain.run(data, callbacks=[manager])
    manager._current_thought.complete('Finished...')

    return response

with st.form('my_form', clear_on_submit=True):
    # Break: OpenAI API Key Error
    if not ss.openai_api_key or not ss.openai_api_key.startswith('sk-'):
        if not ss.openai_api_key:
            warning_message = 'OpenAI API Key 를 입력해주세요 🥲'

        elif not ss.openai_api_key.startswith('sk-'):
            warning_message = 'OpenAI API Key 형식이 올바르지 않습니다 🥲'
        
        st.warning(warning_message, icon='🚨')
        _ = st.form_submit_button('Send Message')
        st.stop()


    # ----- Human Container
    human_container = st.chat_message("human")
    input_keys = get_prompt_inputs(prompt_template)
    # user input variables
    input_dict = {}
    for k in input_keys:
        input_dict[k] = human_container.text_area(f"___{k}___", '')

    with human_container.expander("__Your Message__", expanded=True):
        user_message = prompt_template.format(**input_dict)
        st.write(f"""```\n{user_message}\n```""")

    submitted = human_container.form_submit_button('Send Message', use_container_width=True)
    if not submitted:
        st.stop()

    # ----- AI Container
    ai_container = st.chat_message("assistant")
    response = run_chain(input_dict, ai_container)

    ss.chat_history.append({'User':user_message,'Assistant':response})
    ai_container.write(response) # write response

    ai_container.form_submit_button( # copy
        "copy & clear", on_click=on_copy_click, args=(response,), type='primary')

    del ss.openai_api_key