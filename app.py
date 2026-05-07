import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai

# 1. SETUP
st.set_page_config(page_title="People Intelligence Engine", layout="wide")

# 2. API KEY SETUP
# We will set this up in the hosting step later
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key! Please set it in Streamlit Secrets.")

st.title("🛡️ People Intelligence One-Stop Shop")
st.markdown("### Powered by Gemini AI")

# 3. SIDEBAR - FILTERS (Demographics)
st.sidebar.header("Filter Insights")
gender = st.sidebar.multiselect("Gender", ["Female", "Male", "Other"], default=["Female", "Male", "Other"])
bu = st.sidebar.multiselect("Business Unit", ["Sales", "Tech", "HR", "Marketing"], default=["Sales", "Tech", "HR", "Marketing"])

# 4. DASHBOARD AREA (Charts)
col1, col2 = st.columns(2)

with col1:
    st.subheader("Engagement by Business Unit")
    # Mock data - in a real app, this pulls from your uploaded CSV
    df_bu = pd.DataFrame({"BU": ["Sales", "Tech", "HR", "Marketing"], "Engagement": [3.2, 4.5, 4.1, 3.8]})
    fig1 = px.bar(df_bu, x="BU", y="Engagement", color="BU")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Retention Risk by Level")
    df_lvl = pd.DataFrame({"Level": ["L1", "L2", "L3", "L4"], "Risk": [10, 25, 15, 5]})
    fig2 = px.line(df_lvl, x="Level", y="Risk")
    st.plotly_chart(fig2, use_container_width=True)

# 5. THE DATA ABSORBER (RAG)
uploaded_file = st.file_uploader("Upload your Survey/FGD Data (CSV or Text)")

if uploaded_file:
    # Read the data
    if uploaded_file.name.endswith('.csv'):
        data_text = pd.read_csv(uploaded_file).to_string()
    else:
        data_text = uploaded_file.read().decode("utf-8")
    
    st.success("Data absorbed successfully!")

    # THE CHAT BOX
    query = st.chat_input("Ask a question (e.g., 'What are the chances of Akshay leaving?')")

    if query:
        with st.chat_message("user"):
            st.write(query)
            
        # Ask Gemini
        model = genai.GenerativeModel('gemini-1.5-pro')
        prompt = f"You are an HR Director. Use this data: {data_text}. Question: {query}"
        
        response = model.generate_content(prompt)
        
        with st.chat_message("assistant"):
            st.write(response.text)
