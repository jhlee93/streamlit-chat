import streamlit as st
from st_pages import add_page_title

add_page_title(layout='wide')

ss = st.session_state
st.warning('대화 내역은 __20개__ 까지만 저장됩니다.')

if 'chat_history' in ss:
    chat_history = ss.chat_history
    if not chat_history:
        st.write('### 텅...🫥')
else:
    st.write('### 텅...🫥')
    st.stop()

markdown_preview = st.toggle('Markdown Preview')
for c in ss.chat_history:
    user_message, assi_message = c['User'], c['Assistant']
    with st.chat_message('human'):
        st.code(user_message, language='markdown')

    with st.chat_message('assistant'):
        if markdown_preview:
            st.write(assi_message)
        else:
            st.code(assi_message, language='markdown')