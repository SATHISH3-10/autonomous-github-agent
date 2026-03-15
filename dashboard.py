import streamlit as st
import json
from agent import run_agent

st.title("Autonomous GitHub Issue Fixer")

if st.button("Run Agent"):
    
    logs = run_agent()
    
    st.success("Agent executed successfully")

    for log in logs:
        st.write(log)