# frontend_streamlit/app.py
import streamlit as st
import pandas as pd
import requests
import json
import base64
from io import BytesIO
import os


# FastAPI Backend URL (adjust if running elsewhere)
FASTAPI_URL = "http://localhost:8000" 

# --- Custom Styling for OCP Branding ---
def apply_ocp_style():
    st.markdown(
        """
        <style>
        .main-header {
            color: #008000; /* OCP Green */
            font-size: 2.5em;
            font-weight: bold;
            text-align: center;
            padding-bottom: 20px;
        }
        .stButton button {
            background-color: #008000; /* OCP Green */
            color: white;
            border-radius: 5px;
            border: 1px solid #006400;
            padding: 10px 20px;
            font-size: 1.1em;
            cursor: pointer;
        }
        .stButton button:hover {
            background-color: #006400; /* Darker green on hover */
        }
        .stFileUploader > div > button {
            background-color: #008000;
            color: white;
        }
        .stFileUploader > div > button:hover {
            background-color: #006400;
        }
        .stChatInput > div > div > input {
            border: 2px solid #008000; /* Green border for chat input */
        }
        .stChatInput > div > div > button {
            background-color: #008000;
            color: white;
        }
        .stChatInput > div > div > button:hover {
            background-color: #006400;
        }
        .stAlert {
            background-color: #e6ffe6; /* Light green for success/info */
            color: #004d00;
        }
        /* Style for chat messages if desired */
        .st-chat-message-container.user {
            background-color: #f0fff0; /* Very light green for user messages */
        }
        .st-chat-message-container.assistant {
            background-color: #e6ffe6; /* Light green for assistant messages */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def main():
    st.set_page_config(
        page_title="OCP AI Contract Assistant",
        page_icon="🤖",
        layout="wide"
    )

    apply_ocp_style()

    # Load OCP Logo
    ocp_logo_path = "ocp_logo.png" # Make sure this file is in frontend_streamlit/
    if os.path.exists(ocp_logo_path):
        ocp_logo_base64 = get_image_base64(ocp_logo_path)
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center; align-items: center; gap: 20px; margin-bottom: 30px;">
                <img src="data:image/png;base64,{ocp_logo_base64}" width="100">
                <h1 class="main-header">OCP AI Contract Assistant</h1>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown('<h1 class="main-header">OCP AI Contract Assistant</h1>', unsafe_allow_html=True)

    # st.markdown("<p style='text-align: center; color: gray;'>Leveraging advanced AI models for smarter contract analysis.</p>", unsafe_allow_html=True)
    
    with st.sidebar:
        st.header("📋 Instructions")
        st.markdown("""
        ### Document Extraction
        1. Upload your PDF contract.
        2. Click 'Extract Information'.
        3. The AI model will analyze the document and provide key details.
        
        ### Contract Chatbot
        Once a PDF is uploaded and its information extracted, you can ask questions directly to the contract using the chatbot at the bottom of the page.
        
        <br>
        **Powered by OCP AI Initiative**
        """, unsafe_allow_html=True)
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload your PDF contract file here",
        type="pdf",
        help="Upload your contract in PDF format. The AI will try to extract key information and allow you to ask questions."
    )
    
    # Session state for extracted text and chatbot messages
    if "full_contract_text" not in st.session_state:
        st.session_state["full_contract_text"] = None
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    st.markdown("---")
    st.subheader("Contract Information Extraction")

    if uploaded_file is not None:
        st.success(f"File uploaded: {uploaded_file.name}")
        
        if st.button("Extract Contract Information", type="primary"):
            with st.spinner(" AI is processing your contract... This may take a moment."):
                try:
                    files = {"pdf_file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    response = requests.post(f"{FASTAPI_URL}/extract/", files=files)
                    response.raise_for_status() # Raise an exception for bad status codes
                    
                    data = response.json()
                    extracted_data = data["extracted_data"]
                    st.session_state["full_contract_text"] = data["full_text"]
                    
                    # Display results
                    st.success("Information extracted successfully!")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Contract Number:** {extracted_data['Contract Number'] or 'Not found'}")
                        st.write(f"**Client:** {extracted_data['Client'] or 'Not found'}")
                        st.write(f"**Supplier:** {extracted_data['Supplier'] or 'Not found'}")
                        st.write(f"**Object:** {extracted_data['Object'] or 'Not found'}")
                        # st.write(f"**Date:** {extracted_data['Date'] or 'Not found'}")
                    
                    with col2:
                        st.write(f"**Total Amount:** {extracted_data['Total Amount'] or 'Not found'}")
                        st.write(f"**Currency:** {extracted_data['Currency'] or 'Not found'}")
                        st.write(f"**Location:** {extracted_data['Location'] or 'Not found'}")
                    
                    st.subheader("📋 Complete Results Table")
                    df = pd.DataFrame([extracted_data])
                    st.dataframe(df, use_container_width=True)
                    
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Results as CSV",
                        data=csv,
                        file_name=f"contract_info_{uploaded_file.name}.csv",
                        mime="text/csv"
                    )
                    
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Error communicating with the AI backend: {e}. Please ensure the backend is running at {FASTAPI_URL}.")
                except Exception as e:
                    st.error(f"❌ An unexpected error occurred: {str(e)}")
        
    st.markdown("---")
    st.subheader("💬 Contract Chatbot")

    if st.session_state["full_contract_text"]:
        st.info("You can now ask questions about the uploaded contract!")
        for message in st.session_state["messages"]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Ask a question about the contract..."):
            st.session_state["messages"].append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("AI is thinking..."):
                    try:
                        # Call FastAPI /chat endpoint
                        chat_payload = {
                            "full_contract_text": st.session_state["full_contract_text"],
                            "question": prompt
                        }
                        response = requests.post(f"{FASTAPI_URL}/chat/", json=chat_payload)
                        response.raise_for_status()
                        
                        chat_data = response.json()
                        answer = chat_data["answer"]

                        if answer:
                            st.markdown(answer)
                            st.session_state["messages"].append({"role": "assistant", "content": answer})
                        else:
                            no_answer_message = "Sorry, I couldn't find a direct answer to that question in the document."
                            st.markdown(no_answer_message)
                            st.session_state["messages"].append({"role": "assistant", "content": no_answer_message})
                    except requests.exceptions.RequestException as e:
                        st.error(f"❌ Error communicating with the AI backend: {e}")
                        st.session_state["messages"].append({"role": "assistant", "content": f"Error: {e}"})
                    except Exception as e:
                        st.error(f"❌ An unexpected error occurred during chat: {str(e)}")
                        st.session_state["messages"].append({"role": "assistant", "content": f"Error: {e}"})
    else:
        st.warning("Please upload a PDF and click 'Extract Contract Information' first to enable the chatbot.")

    st.markdown("---")
    st.markdown("<p style='text-align: center; color: gray;'>Designed for OCP by AI Solutions Team</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()