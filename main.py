import streamlit as st
import pandas as pd

user_df = pd.read_csv("users.csv")
user_dict = {}
for i in range(len(user_df)) :
    user_dict[user_df.iloc[i,1]] = user_df.iloc[i,1]


# 초기 세션 상태 설정
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# 로그인 함수
def login(username, password):
    # 사용자 인증 로직
    if password == user_dict[username]:  # 예시로 고정된 계정
        st.session_state.logged_in = True
        st.success("로그인 성공!")
    else:
        st.error("아이디 또는 비밀번호가 잘못되었습니다.")

# 로그아웃 함수
def logout():
    st.session_state.logged_in = False

# 로그인 페이지
def login_page():
    st.title("로그인 페이지")
    username = st.text_input("아이디")
    password = st.text_input("비밀번호", type="password")
    if st.button("로그인"):
        login(username, password)

# 메인 페이지
def main_page():
    st.title("메인 페이지")
    pages = {
        "글쓰기 도우미": [
            st.Page("DAS.py", title="소설창작도우미"),
            st.Page("WAS.py", title="글쓰기도우미"),
        ]
    }
    pg = st.navigation(pages)
    pg.run()

    # 로그아웃 버튼
    if st.button("로그아웃"):
        logout()

# 메인 로직
if st.session_state.logged_in:
    main_page()
else:
    login_page()
