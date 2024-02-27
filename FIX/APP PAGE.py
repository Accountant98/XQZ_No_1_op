
import sys
# sys.path.append(r"C:QZ_No_1_code")
import streamlit as st
from user_read_only import user_read_only
from admin import admin
st.set_page_config(
    page_title="My Streamlit App",
    page_icon=":smiley:",
    layout="wide"  
)
try :
    if st.session_state.position=="admin": #st.session_state.mail:
    #------------MAIN APP-----------x
        try:
            admin()
        except Exception as e:
            st.error(f"Error: {e}")
    elif st.session_state.position=="staff" : 
        try:
            user_read_only()
        except Exception as e:
            st.error(f"Error: {e}")
except:
    st.warning("Please login before running app!!!")

