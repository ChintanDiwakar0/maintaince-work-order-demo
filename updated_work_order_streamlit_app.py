
import streamlit as st
import pandas as pd
import openai
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Work Order Processor", layout="wide")
st.title("🛠️ Maintenance Work Order Assistant")

# File upload
uploaded_file = st.file_uploader("📄 Upload Maintenance Work Order Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success("✅ File Uploaded Successfully")
    st.dataframe(df)

    work_order_options = df["Work Order Number"].unique().tolist()
    selected_wo = st.selectbox("🔎 Select a Work Order", work_order_options)

    if selected_wo:
        selected_data = df[df["Work Order Number"] == selected_wo].to_dict(orient="records")[0]

        # Show extracted fields
        st.subheader("📋 Extracted Information for Google Form Submission")
        st.code(json.dumps(selected_data, indent=2), language="json")

        # Create a chat assistant
        st.subheader("🤖 Ask about this Work Order")

        # Store chat history in session
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "system", "content": "You are a helpful assistant helping users understand maintenance work order details."},
                {"role": "user", "content": f"Here are the work order details: {json.dumps(selected_data, indent=2)}"}
            ]

        user_input = st.text_input("Ask a question about the selected work order")

        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.spinner("Thinking..."):
                response = client.chat.completions.create(
                    model="gpt-4-1106-preview",
                    messages=st.session_state.messages
                )
                reply = response.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.success("💬 Response:")
                st.markdown(reply)

# Instructions
st.markdown("---")
st.markdown("After selecting a work order, all extracted details are shown above in JSON format You can copy these to pre-fill a Google Form or submit them via API.")
