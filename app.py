import streamlit as st

st.set_page_config(
page_title="Whole Seller Scheme ",  # Title on browser tab
page_icon="📊",
layout="centered",  # Optional: "centered" or "wide"
initial_sidebar_state="collapsed"  # Optional: "auto", "expanded", or "collapsed"
)
 

st.markdown(
    """
    <a href="https://subhash511.github.io/PriyaGold_QPS/" target="_blank">
        <button style="background-color:#4CAF50; color:white; padding:10px 20px; font-size:16px; border:none; border-radius:5px;">
            Go to PriyaGold QPS
        </button>
    </a>
    <br>
    """,
    unsafe_allow_html=True
)
st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
st.image("logo/QPSScheme.jpeg", use_container_width=True)

# """
# import pandas as pd
# import sqlite3
# import uuid
# from PIL import Image
# import os
# from main import main_ui
# from admin import admin_ui


# st.set_page_config(
#     page_title="Whole Seller Scheme ",  # Title on browser tab
#     page_icon="📊",
#     layout="centered",  # Optional: "centered" or "wide"
#     initial_sidebar_state="collapsed"  # Optional: "auto", "expanded", or "collapsed"
# )
# # ================================
# # 📌 DATABASE SETUP
# # ================================
# conn = sqlite3.connect("DATA/users.db", check_same_thread=False)
# c = conn.cursor()
# c.execute('''
#     CREATE TABLE IF NOT EXISTS sessions (
#         username TEXT,
#         token TEXT UNIQUE
#     )
# ''')
# conn.commit()

# if not os.path.exists("DATA"):
#         os.makedirs("DATA")
# # ================================
# # 📌 LOAD USERS FROM EXCEL
# # ================================
# @st.cache_data
# def load_users():
#     df = pd.read_excel("DATA/data.xlsx", sheet_name='DB')
#     #df = pd.read_parquet('https://files.dasboardai.com/DATA/data.parquet')
#     return df
   
# @st.cache_data
# def load_wholesaler():
#     df_wholesale = pd.read_excel("DATA/data.xlsx", sheet_name='data')
#     # df_wholesale = pd.read_parquet('https://files.dasboardai.com/DATA/DB.parquet')
#     return df_wholesale

# df1 = load_users()

# users = df1.set_index("Username")["Password"].to_dict()

# # ================================
# # 📌 SESSION STATE INIT
# # ================================
# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False
# if "Username" not in st.session_state:
#     st.session_state.Username = ""
# if "token" not in st.session_state:
#     st.session_state.token = ""

# # ================================
# # 🔄 CHECK IF USER ALREADY LOGGED IN FROM TOKEN IN URL
# # ================================
# query_params = st.query_params
# if not st.session_state.logged_in and "token" in query_params:
#     token = query_params["token"]
#     c.execute("SELECT username FROM sessions WHERE token = ?", (token,))
#     result = c.fetchone()
#     if result:
#         st.session_state.logged_in = True
#         st.session_state.Username = result[0]
#         st.session_state.token = token

# # ================================
# # 🔐 LOGIN FUNCTION
# # ================================
# def login(username, password):
#     if username in users and users[username] == password:
#         st.session_state.logged_in = True
#         st.session_state.Username = username

#         # Generate token and save in DB
#         token = str(uuid.uuid4())
#         st.session_state.token = token
#         c.execute("INSERT OR REPLACE INTO sessions (username, token) VALUES (?, ?)", (username, token))
#         conn.commit()

#         # Set query parameter
#         st.query_params["token"] = token
#         st.rerun()
#     else:
#         st.error("Invalid username or password.")

# # ================================
# # 🔓 LOGOUT FUNCTION
# # ================================
# def logout():
#     token = st.session_state.get("token", "")
#     if token:
#         c.execute("DELETE FROM sessions WHERE token = ?", (token,))
#         conn.commit()
#     st.session_state.logged_in = False
#     st.session_state.Username = ""
#     st.session_state.token = ""
#     st.query_params.clear()
#     st.rerun()

# # ================================
# # 🖥️ MAIN UI
# # ================================
# if st.session_state.logged_in:
#     # Sidebar with a logout button
#     username_to_search = st.session_state.Username
#     st.sidebar.success(f"Welcome back, **{username_to_search}**! 🎉") 
#     if st.sidebar.button("Logout"):
#         logout()
#     df_wholesale = load_wholesaler()    
#     if username_to_search == 'AdminSubhash':
#         st.write('Welcome to Admin Page')
#         admin_ui(df_wholesale=df_wholesale)
#     else:
#         result = df1[df1["Username"] == username_to_search]
#         if not result.empty:
#             db_id = result.iloc[0]["db_id"]
#             main_ui(db_id=db_id,df_wholesale=df_wholesale)



# else:
#     col1,col2 = st.columns(2)
#     with col1:   
#         image = Image.open('logo/logo.jpg')  # Replace with your image path
#         st.image(image,width=220)
#     with col2:
#         st.markdown("# QPS Wholeseller Scheme Tracker")    
#     st.title("🔐 Login")
#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")
#     if st.button("Login"):
#         login(username, password)
# """