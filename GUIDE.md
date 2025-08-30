

#### Web Interface 
streamlit run streamlitextractor.py
- Upload PDF contracts
- Extract information instantly
- Download results as CSV


#### 📁 Batch Processing (Multiple Files)
\`\`\`bash
python batch_extractor.py ./contracts_folder/ results.csv
\`\`\`


## How It Works

1. **PDF Text Extraction**: Uses `pdfplumber` to extract text
2. **Pattern Matching**: Uses regex patterns to find information
3. **Data Cleaning**: Cleans and normalizes extracted data
4. **Multiple Patterns**: Uses multiple patterns per field for better accuracy


pip install --upgrade pip setuptools wheel

Option 1: Install a prebuilt wheel (recommended)

On macOS, recent Python versions can use prebuilt pyarrow wheels. Try upgrading pip and installing pyarrow first:

pip install --upgrade pip setuptools wheel
pip install pyarrow==11.0.0


If that succeeds, then install Streamlit:

pip install streamlit==1.28.0
 pip install torch torchvision torchaudio  

// pdf scaned 
brew install tesseract  # macOS
pip install pytesseract

