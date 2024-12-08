import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

# 초기 세션 상태 설정
if "text" not in st.session_state:
    st.session_state.text = []  # 현재 텍스트 상태
if "prev_text" not in st.session_state:
    st.session_state.prev_text = []  # 이전 텍스트 상태 (되돌리기용)

# 제목 및 설명
st.title("글쓰기 도우미")
st.markdown("""
이 도구는 글쓰기 도우미입니다. 나만의 소설을 작성하는 과정에서 막히는 부분이 생겼을 때 AI가 소설의 뒷내용을 자연스럽게 작성해줍니다.  
AI가 작성해준 뒷내용 중에 마음에 들지 않는 내용은 삭제 및 수정을 하면서 나만의 소설을 완성해 봅시다.
""")

print(st.session_state.text)
print(st.session_state.prev_text)
if not st.session_state.text :
    first_value = ""
else :
    first_value = st.session_state.text[-1]
# 텍스트 입력/결과 창 (하나의 창에서 입력과 결과를 관리)
new_text = st.text_area(
    "여기에 텍스트를 입력하세요",
    value= first_value,
    height=200
)
    

# "문장 이어서 쓰기" 버튼 동작
if st.button("문장 이어서 쓰기"):
    # 현재 텍스트 상태를 이전 상태로 저장 (되돌리기용)
    st.session_state.prev_text.append(new_text)
    

    generate_prompt = ChatPromptTemplate.from_messages([
        ("system", """
         지금까지 작성된 글을 읽고, 글의 내용을 자연스럽게 이어서 한 문장을 작성해봐. 필요에 따라 대화하는 표현은 큰따옴표, 생각하는 표현은 작은따옴표로 나타내줘. 
         지금까지 작성한 내용은 지우지 말고 계속 써줘.
         """),
        ("human", "{input}")
    ])

    llm = ChatOpenAI(
        temperature=0.5,
        model='gpt-4o-mini'
    )

    chain = (generate_prompt | llm | StrOutputParser())

    # 현재 텍스트를 입력으로 사용해 이어쓰기 처리
    result = chain.invoke({
        "input": new_text
    })

    # 기존 텍스트에 이어서 추가
    st.session_state.text.append( f" {result}")
    st.rerun()  # UI를 즉시 업데이트

if len(st.session_state.text) > 0:
    if st.button("직전 문장으로 돌아가기"):
        if len(st.session_state.prev_text) > 0:
            # text를 이전 상태로 복원
            st.session_state.text = st.session_state.prev_text[-1]
            # prev_text에서 마지막 복원 상태 제거
            st.session_state.prev_text = st.session_state.prev_text[:-1]
            st.rerun()
        else:
            st.warning("복구할 이전 상태가 없습니다!")

# 텍스트 출력
if len(st.session_state.text) > 0:
    # 두 리스트의 최소 길이
    min_length = min(len(st.session_state.text), len(st.session_state.prev_text))
    
    # prev_text와 text 모두 있는 인덱스에 대해 출력
    for i in range(min_length):
        col1, col2 = st.columns(2)
        with col1:
            st.write("내가 작성한 내용")
            st.write(st.session_state.prev_text[i])
        with col2:
            st.write("AI가 수정해준 내용")
            st.write(st.session_state.text[i])
    
    # 만약 text가 prev_text보다 길어서 나머지가 있다면
    if len(st.session_state.text) > min_length:
        for i in range(min_length, len(st.session_state.text)):
            col1, col2 = st.columns(2)
            with col1:
                st.write("내가 작성한 내용")
                st.write("이전 상태 없음")  # 이전 상태가 없는 경우
            with col2:
                st.write("AI가 수정해준 내용")
                st.write(st.session_state.text[i])


# "복사하기" 버튼 동작
if st.button("복사하기"):
    # 복사할 텍스트를 표시 (Streamlit에서는 클립보드 접근이 제한됨)
    st.text_area("복사할 텍스트", value=st.session_state.text, height=200)
    st.success("완성된 텍스트가 복사 영역에 표시되었습니다. 복사하려면 Ctrl+C를 사용하세요.")

# "글쓰기 모음집" 버튼 동작
if st.button("글쓰기 모음집"):
    padlet_url = "https://padlet.com/sres5002/8-23-dp6gx9cp2tuln5tn"
    st.markdown(f"""
    <script>
    window.open("{padlet_url}", "_blank");
    </script>
    """, unsafe_allow_html=True)
    st.success("Padlet 사이트로 이동합니다!")