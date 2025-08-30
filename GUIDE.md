

### 1. Install Dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 2. Choose Your Method

#### 🌟 Web Interface (Recommended)
\`\`\`bash
streamlit run streamlitextractor.py
\`\`\`
- Upload PDF contracts
- Extract information instantly
- Download results as CSV

#### ⚡ Single File Extraction
\`\`\`bash
python contract_extractor.py your_contract.pdf
\`\`\`

#### 📁 Batch Processing (Multiple Files)
\`\`\`bash
python batch_extractor.py ./contracts_folder/ results.csv
\`\`\`

## 📋 What Gets Extracted

- **Contract Number**: CONTRAT N° 48041K24
- **Supplier**: MB SETRAV
- **Client**: OCP SA
- **Object**: Contract purpose/description
- **Total Amount**: 1 545 600,00 Dirhams
- **Currency**: Dirhams, EUR, USD, etc.
- **Date**: Contract date
- **Location**: Contract location

## 🎯 Supported Languages

- ✅ **French** (Optimized)
- ✅ **English**
- ✅ **Mixed French/English**

## 🔧 How It Works

1. **PDF Text Extraction**: Uses `pdfplumber` to extract text
2. **Pattern Matching**: Uses regex patterns to find information
3. **Data Cleaning**: Cleans and normalizes extracted data
4. **Multiple Patterns**: Uses multiple patterns per field for better accuracy

## 💡 Advantages

- ✅ **No Internet Required** (after installation)
- ✅ **Fast Processing**
- ✅ **Batch Processing**
- ✅ **Privacy Friendly** (no data sent to external services)
- ✅ **Customizable Patterns**

## 🛠️ Customization

You can easily add new patterns in `free_contract_extractor.py`:

\`\`\`python
self.patterns = {
    'contract_number': [
        r'CONTRAT\s+N[°º]\s*([A-Z0-9/\-]+)',
        # Add your custom pattern here
        r'Your\s+Custom\s+Pattern\s*([A-Z0-9]+)',
    ],
    # Add new fields
    'new_field': [
        r'Your\s+Pattern\s*([^\\n]+)',
    ]
}
\`\`\`

## 📊 Example Output

\`\`\`
Contract Number: 48041K24
Supplier: MB SETRAV
Client: OCP SA
Object: Fourniture et installation de panneaux de signalisation...
Total Amount: 1 545 600,00 Dirhams
Currency: Dirhams
Date: 01/02/2024
Location: Khouribga
\`\`\`

## 🎯 Perfect For

- Small businesses
- Freelancers
- Students
- Anyone who needs basic contract extraction
- Batch processing multiple contracts
- Privacy-sensitive environments


pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

✅ Solutions
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
## OCR meaning 
OCR PDF" refers to a PDF file that has undergone Optical Character Recognition, a technology that converts scanned images or text-based PDFs into machine-readable, editable, and searchable text. This process allows you to select, copy, edit, and search for text within documents that were previously just static images, transforming them into fully interactive documents. 



jss script 
uvicorn main:app --reload --port 8000
python -m http.server 8080









            // <div><strong>Date:</strong> ${data["Date"] || 'Not found'}</div>










pip install "fastapi[all]" uvicorn pydantic python-multipart python-dotenv PyMuPDF transformers torch





pip install streamlit pandas requests


uvicorn main:app --reload --host 0.0.0.0 --port 8000