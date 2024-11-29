import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json
from dotenv import load_dotenv

load_dotenv()

# 초기 세션 상태 설정
if "conversation_log" not in st.session_state:
    st.session_state.conversation_log = []  # 대화 로그 저장
if "user_input" not in st.session_state:
    st.session_state.user_input = ""  # 사용자 입력 저장
if "mode" not in st.session_state:
    st.session_state.mode = "창의적 소설 모드"  # 기본 모드
if "background_image" not in st.session_state:
    st.session_state.background_image = None  # 배경 이미지

# OpenAI 모델 설정
llm = ChatOpenAI(
    temperature=0.7,  # 창의적 대답을 유도
    model="gpt-4o-mini"  # 적절한 모델 선택
)

# 사용자 질문 처리 함수
def process_user_input():
    user_input = st.session_state.user_input.strip()
    if user_input:
        # 사용자 질문 로그 추가
        st.session_state.conversation_log.append(("user", user_input))

        # AI 응답 생성
        generate_prompt = ChatPromptTemplate.from_messages([
            ("system", f"너는 {st.session_state.mode}에서 대화를 통해서 학생들이 창의적으로 소설을 작성할 수 있도록 도와주는 AI야. 학생들이 소설 쓰기에 대한 아이디어와 영감을 얻을 수 있도록 적극적으로 질문과 답을 해줘."),
            *st.session_state.conversation_log,
            ("human", "{input}")
        ])
        chain = (generate_prompt | llm | StrOutputParser())
        ai_response = chain.invoke({"input": user_input})

        # AI 응답 로그 추가
        st.session_state.conversation_log.append(("ai", ai_response))

        # 입력 창 초기화
        st.session_state.user_input = ""

# 스타일 설정
st.markdown("""
<style>
.chat-bubble {
    max-width: 70%;
    padding: 10px 15px;
    border-radius: 15px;
    margin-bottom: 10px;
    font-size: 16px;
    line-height: 1.5;
}
.user-bubble {
    background-color: #dcf8c6;
    align-self: flex-end;
    text-align: right;
}
.ai-bubble {
    background-color: #f1f0f0;
    align-self: flex-start;
    text-align: left;
}
.chat-container {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}
.chat-container-right {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
}
body {
    background-image: url('background_image_url');
    background-size: cover;
    background-attachment: fixed;
    background-position: center;
}
</style>
""", unsafe_allow_html=True)

# 배경 이미지 선택
backgrounds = {
    "기본": None,
    "판타지 소설": "https://example.com/fantasy.jpg",
    "SF 소설": "https://example.com/sf.jpg",
    "로맨스 소설": "https://example.com/romance.jpg",
}
selected_background = st.sidebar.selectbox("배경 이미지 선택", options=list(backgrounds.keys()))
st.session_state.background_image = backgrounds[selected_background]

if st.session_state.background_image:
    st.markdown(f"""
    <style>
    body {{
        background-image: url('{st.session_state.background_image}');
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }}
    </style>
    """, unsafe_allow_html=True)

# 모드 선택
modes = ["창의적 소설 모드", "단편 소설 모드", "서사적 소설 모드"]
st.session_state.mode = st.sidebar.radio("대화 모드 선택", options=modes)

# 제목 및 설명
st.title("소설 창작 아이디어 도우미")
st.markdown("""
이 도구는 AI와의 대화를 통해 소설 주제, 배경, 주인공 성격 등에 대한 영감을 얻을 수 있도록 도와줍니다.  
아래 대화창에서 자유롭게 질문하고, AI와 소설 아이디어를 만들어보세요!
""")

# 대화 로그 표시
st.subheader("대화 기록")
for sender, message in st.session_state.conversation_log:
    if sender == "user":
        st.markdown(f'<div class="chat-container chat-container-right"><div class="chat-bubble user-bubble">{message}</div></div>', unsafe_allow_html=True)
    elif sender == "ai":
        st.markdown(f'<div class="chat-container"><div class="chat-bubble ai-bubble">{message}</div></div>', unsafe_allow_html=True)

# 입력 칸 (하단)
st.text_input(
    "AI와 대화하기",
    value=st.session_state.user_input,
    placeholder="질문을 입력하세요...",
    on_change=process_user_input,
    key="user_input"
)

# 대화 로그 다운로드 버튼
if st.session_state.conversation_log:
    log_text = "\n".join([
        f"{'사용자' if sender == 'user' else 'AI'}: {message}"
        for sender, message in st.session_state.conversation_log
    ])
    st.download_button(
        label="대화 로그 다운로드",
        data=log_text,
        file_name="chat_log.txt",
        mime="text/plain"
    )

# 소설 초안 생성 버튼
if st.button("소설 초안 생성"):
    if st.session_state.conversation_log:
        summary_prompt = ChatPromptTemplate.from_messages([
            ("system", "너는 창의적인 소설 초안을 작성하는 AI야."),
            *st.session_state.conversation_log,
            ("human", "지금까지의 대화를 바탕으로 소설 초안을 작성해줘.")
        ])
        chain = (summary_prompt | llm | StrOutputParser())
        draft = chain.invoke({"input": ""})
        st.subheader("소설 초안")
        st.write(draft)
    else:
        st.warning("먼저 AI와 대화를 나누어주세요!")