import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai

# 1. SETUP
st.set_page_config(page_title="HR Intelligence Engine", layout="wide")

# Connect Gemini
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key in Streamlit Secrets!")

st.title("📊 Strategic People Intelligence")
st.markdown("---")

# 2. FEEDING THE DATA
# This looks for your file. If you haven't uploaded it to GitHub yet, it will use the "Upload" button.
uploaded_file = st.sidebar.file_uploader("Upload Excel Data", type=['xlsx', 'csv'])

# If no file is uploaded yet, we show a message
if uploaded_file is None:
    st.info("💡 Welcome! Please upload your HR Excel sheet in the sidebar to begin the analysis.")
else:
    # Read the data
    if uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_csv(uploaded_file)

    # --- 3. THE DASHBOARD (PART 1 OF YOUR PROJECT) ---
    st.header("📈 Organization Snapshot")
    
    # Create 3 columns for the 'Demographics'
    c1, c2, c3 = st.columns(3)

    with c1:
        st.subheader("Gender Distribution")
        # Automatically detects 'Gender' column
        if 'Gender' in df.columns:
            fig_gen = px.pie(df, names='Gender', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_gen, use_container_width=True)
        else:
            st.write("Column 'Gender' not found.")

    with c2:
        st.subheader("BUs & Functions")
        if 'BU' in df.columns:
            fig_bu = px.bar(df['BU'].value_counts(), orientation='h', color_discrete_sequence=['#636EFA'])
            st.plotly_chart(fig_bu, use_container_width=True)
        else:
            st.write("Column 'BU' not found.")

    with c3:
        st.subheader("Engagement by Level")
        if 'Level' in df.columns and 'Engagement' in df.columns:
            fig_lvl = px.box(df, x='Level', y='Engagement', color='Level')
            st.plotly_chart(fig_lvl, use_container_width=True)
        else:
            st.write("Columns 'Level' or 'Engagement' not found.")

    st.markdown("---")

    # --- 4. THE AI INTELLIGENCE (PART 2) ---
    st.header("🤖 AI Insights (Gemini)")
    query = st.chat_input("Ask a deep-dive question (e.g. 'Identify flight risks in Sales')")

    if query:
        # Convert the data to text for the AI to read
        raw_data_text = df.to_string()
        
        with st.spinner("Gemini is analyzing your data..."):
            model = genai.GenerativeModel('gemini-1.5-pro')
            prompt = f"""
            You are a Senior People Analytics Expert. 
            Below is the employee data:
            {raw_data_text}
            
            Question: {query}
            
            Instructions:
            1. Provide a professional, data-backed answer.
            2. If predicting risk, mention the specific reasons found in the data.
            3. Keep the tone executive and insightful.
            """
            
            response = model.generate_content(prompt)
            
            with st.chat_message("assistant"):
                st.write(response.text)
