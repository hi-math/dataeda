import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import time
from streamlit_extras.switch_page_button import switch_page 
from gspread.exceptions import APIError

st.image("images/bg.png")
st.header('	:seedling:서울특별시 :blue[환경 데이터] 플랫폼', divider="rainbow")

st.divider()

if 'name' not in st.session_state:
    st.session_state['name'] = 'noname'
    
    
if 'pw' not in st.session_state:
    st.session_state['pw'] = ''


with st.form("로그인"):
    col1, col2 = st.columns(2)
    with col1 : 
        st.session_state['name'] = st.text_input("이름", key="a")
    with col2 : 
        st.session_state['pw'] = st.text_input("비밀번호", key="b", type="password")
    submitted = st.form_submit_button("로그인")

login = {"박시현":1113,
         "성지은":1408,
         "유지우":1412,
         "이유진":1414,
         "조수아":1416,
         "조현서":2111,
         "김서진":2203,
         "김나경":2304,
         "이정민":2315,
         "유준서":2410,
         "정희선":2413,
         "김진영":3204,
         "이서연":3210,
         "안영석":1000}


if submitted:
    with st.spinner('로그인중입니다...'):
        time.sleep(2)
    
    if st.session_state['name'] in login.keys():
        
        if st.session_state['pw'] == str(login[st.session_state['name']]):
        
            st.caption(f"{st.session_state['name']}님 로그인 되었습니다.")
            conn = st.connection("gsheets", type=GSheetsConnection)
            df = conn.read(
            worksheet="Sheet1",
            ttl="10m",
            usecols=[0, 1],
            nrows=100
        )
            df = df.dropna(axis=0)
            df1 = pd.DataFrame({"name":st.session_state['name'],
                    "loc":"",
                    "reason":""}, index=[0])
        
        
            try:
              conn.create(worksheet=st.session_state['name'], data=df1)
            except APIError as e:
              if e.response.status_code == 400 and 'already exists' in str(e):
                pass
              else:
                raise  # 다른 APIError의 경우, 예외를 다시 발생시킴
                        

            my_bar = st.progress(0, text='잠시후 페이지를 이동합니다.')

            for percent_complete in range(100):
              time.sleep(0.01)
              my_bar.progress(percent_complete + 1, text='잠시후 페이지를 이동합니다.')
        
            switch_page("데이터 살펴보기")
        
        else:
          st.write("로그인 정보가 잘못되었습니다.")
        
    else:
          st.write("로그인 정보가 잘못되었습니다.")
          
              

# if st.button("new sheet"):
#     df1 = pd.DataFrame({"A":[1,2,3],
#                    "B":[3,4,5],
#                    "C":[7,8,9]})
#     conn.create(worksheet="abcd", data=df1)
#     st.success("Done")
    
# if st.button("Calculate Total Orders Sum"):
#     sql = 'SELECT SUM("age") as "ass" FROM "Sheet1";'
#     total_orders = conn.query(sql=sql)
#     st.write(total_orders)
        
# name = st.text_input("name", "name")
# pet = st.text_input("pet","pet")
# age = st.slider("age",min_value=0, step=1)
        
# if st.button("insert"):
#     df_copy = df.copy()
#     df_new = pd.DataFrame([{"name": name,
#                            "pet": pet,
#                            "age": age}])
#     df_new
#     df_result = pd.concat([df_copy,df_new], ignore_index=True)
#     conn.update(worksheet="Sheet1", data=df_result)
#     st.success("Worksheet Updated 🤓")
