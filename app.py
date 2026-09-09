"""배포 실습용 미니 여행 도우미.

    streamlit run app.py

키는 코드에 적지 않는다.
- 내 컴퓨터: .env 파일          → load_dotenv() 가 읽어 os.environ 에 올린다
- 배포본:    Cloud 의 Secrets 칸 → Streamlit 이 시작할 때 os.environ 에 올린다
그래서 양쪽 모두 os.getenv() 한 줄로 읽힌다.
"""
import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # 내 컴퓨터에서 실행할 때는 .env 파일에서 키를 읽는다

st.set_page_config(page_title="미니 여행 도우미", page_icon="🧳")
st.title("🧳 미니 여행 도우미")

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("OPENAI_API_KEY 를 찾을 수 없습니다. 내 컴퓨터에서는 .env, 배포본에서는 Secrets 에 넣어야 합니다.")
    st.stop()

client = OpenAI(api_key=api_key)

if "chat" not in st.session_state:
    st.session_state.chat = []

for message in st.session_state.chat:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if question := st.chat_input("여행에 대해 물어보세요"):
    st.session_state.chat.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("생각 중…"):
            response = client.chat.completions.create(
                model="gpt-5.4-nano",
                messages=[{"role": "system", "content": "너는 여행 도우미다. 한국어로 짧게 답한다."}]
                + st.session_state.chat,
            )
            answer = response.choices[0].message.content
        st.markdown(answer)

    st.session_state.chat.append({"role": "assistant", "content": answer})
