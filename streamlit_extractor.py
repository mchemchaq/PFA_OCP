# import streamlit as st
# import pandas as pd
# from free_contract_extractor import FreeContractExtractor
# import tempfile
# import os

# def main():
#     st.set_page_config(
#         page_title="Free Contract Extractor",
#         page_icon="📄",
#         layout="wide"
#     )
    
#     st.title("📄 Free Contract Information Extractor")
#     st.markdown("**100% Free** - No API keys required! Extract contract information using pattern matching.")
    
#     # Sidebar with instructions
#     with st.sidebar:
#         st.header("📋 Instructions")
#         st.markdown("""
#         1. Upload your PDF contract
#         2. Click 'Extract Information'
#         3. View the extracted data
#         4. Download results as CSV
        
#         **Supported Languages:**
#         - French ✅
#         - English ✅
        
#         **Extracted Information:**
#         - Contract Number
#         - Supplier/Provider
#         - Client
#         - Contract Object
#         - Total Amount
#         - Currency
#         - Date
#         - Location
#         """)
    
#     # File upload
#     uploaded_file = st.file_uploader(
#         "Choose a PDF contract file",
#         type="pdf",
#         help="Upload your contract in PDF format"
#     )
    
#     if uploaded_file is not None:
#         # Save uploaded file temporarily
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
#             tmp_file.write(uploaded_file.getvalue())
#             tmp_file_path = tmp_file.name
        
#         # Display file info
#         st.success(f"✅ File uploaded: {uploaded_file.name}")
        
#         # Extract button
#         if st.button("🔍 Extract Contract Information", type="primary"):
#             with st.spinner("Extracting information from contract..."):
#                 try:
#                     extractor = FreeContractExtractor()
#                     result = extractor.extract_to_dict(tmp_file_path)
                    
#                     # Display results
#                     st.header("📊 Extracted Information")
                    
#                     # Create two columns
#                     col1, col2 = st.columns(2)
                    
#                     with col1:
#                         st.subheader("Contract Details")
#                         st.write(f"**Contract Number:** {result['Contract Number'] or 'Not found'}")
#                         st.write(f"**Client:** {result['Client'] or 'Not found'}")
#                         st.write(f"**Supplier:** {result['Supplier'] or 'Not found'}")
#                         st.write(f"**Date:** {result['Date'] or 'Not found'}")
                    
#                     with col2:
#                         st.subheader("Financial & Location")
#                         st.write(f"**Total Amount:** {result['Total Amount'] or 'Not found'}")
#                         st.write(f"**Currency:** {result['Currency'] or 'Not found'}")
#                         st.write(f"**Location:** {result['Location'] or 'Not found'}")
                    
#                     # Contract object (full width)
#                     st.subheader("Contract Object")
#                     st.write(result['Object'] or 'Not found')
                    
#                     # Results table
#                     st.subheader("📋 Complete Results Table")
#                     df = pd.DataFrame([result])
#                     st.dataframe(df, use_container_width=True)
                    
#                     # Download button
#                     csv = df.to_csv(index=False)
#                     st.download_button(
#                         label="📥 Download Results as CSV",
#                         data=csv,
#                         file_name=f"contract_info_{uploaded_file.name}.csv",
#                         mime="text/csv"
#                     )
                    
#                 except Exception as e:
#                     st.error(f"❌ Error processing file: {str(e)}")
        
#         # Clean up temporary file
#         try:
#             os.unlink(tmp_file_path)
#         except:
#             pass
    
#     # Footer
#     st.markdown("---")
#     st.markdown("🆓 **Completely Free** - No API costs, no subscriptions!")

# if __name__ == "__main__":
#     main()
import streamlit as st
import pandas as pd
from contract_extractor import FreeContractExtractor
import tempfile
import os

def main():
    st.set_page_config(
        page_title="Free AI Contract Extractor",
        page_icon="🤖",
        layout="wide"
    )

    st.title("🤖  AI Contract Information Extractor")
    st.markdown("**100%  & AI-Powered** - Leveraging Hugging Face models for smarter extraction!")
    st.markdown("This tool uses advanced Question Answering models to understand your contract documents without any API keys.")
    
    # Sidebar with instructions
    with st.sidebar:
        st.header("📋 Instructions")
        st.markdown("""
        1. Upload your PDF contract.
        2. Click 'Extract Information'.
        3. The AI model will analyze the document.
        4. View the extracted data.
        5. Download results as CSV.
        
        **How it works (AI-Powered):**
        - Extracts text from your PDF.
        - Uses a pre-trained **Hugging Face Question Answering model** to find answers to specific questions within the contract text (e.g., "Who is the client?", "What is the total amount?").
        - No internet connection needed for the extraction once the model is downloaded (first run).
        
        **Extracted Information:**
        - Contract Number
        - Supplier/Provider
        - Client
        - Contract Object
        - Total Amount
        - Currency
        - Date
        - Location
        
        *Note: AI extraction quality depends on the document clarity and model's understanding. It's not 100% accurate for all documents.*
        """)
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose a PDF contract file",
        type="pdf",
        help="Upload your contract in PDF format. The AI will try to extract key information."
    )
    
    if uploaded_file is not None:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        
        # Display file info
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        
        # Extract button
        if st.button("🔍 Extract Contract Information (AI)", type="primary"):
            st.info("💡 First run might take longer as the AI model is downloaded.")
            with st.spinner("🚀 AI is extracting information from your contract... This may take a moment."):
                try:
                    extractor = FreeContractExtractor()
                    result = extractor.extract_to_dict(tmp_file_path)
                    
                    # Display results
                    st.header("📊 Extracted Information (AI-Powered)")
                    
                    # Create two columns
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("Contract Details")
                        st.write(f"**Contract Number:** {result['Contract Number'] or 'Not found'}")
                        st.write(f"**Client:** {result['Client'] or 'Not found'}")
                        st.write(f"**Supplier:** {result['Supplier'] or 'Not found'}")
                        st.write(f"**Object:** {result['Object'] or 'Not found'}")
                        st.write(f"**Date:** {result['Date'] or 'Not found'}")
                    
                    with col2:
                        st.subheader("Financial & Location")
                        st.write(f"**Total Amount:** {result['Total Amount'] or 'Not found'}")
                        st.write(f"**Currency:** {result['Currency'] or 'Not found'}")
                        st.write(f"**Location:** {result['Location'] or 'Not found'}")
                    
                    # Contract object (full width)
                    st.subheader("Contract Object")
                    st.write(result['Object'] or 'Not found')
                    
                    # Results table
                    st.subheader("📋 Complete Results Table")
                    df = pd.DataFrame([result])
                    st.dataframe(df, use_container_width=True)
                    
                    # Download button
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Results as CSV",
                        data=csv,
                        file_name=f"ai_contract_info_{uploaded_file.name}.csv",
                        mime="text/csv"
                    )
                    
                except Exception as e:
                    st.error(f"❌ Error processing file with AI: {str(e)}. Please try another file or check logs for details.")
        
        # Clean up temporary file
        try:
            os.unlink(tmp_file_path)
        except Exception as e:
            st.warning(f"Could not clean up temporary file: {e}")
    
    # Footer
    st.markdown("---")
    st.markdown("🆓 **Completely Free & Open Source** - Powered by Hugging Face models!")

if __name__ == "__main__":
    main()