
##
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
pip install streamlit pandas requests
Running uvicorn 0.35.0 with CPython 3.9.5 on Darwin
pip install "fastapi[all]" uvicorn pydantic python-multipart python-dotenv PyMuPDF transformers torch




jss script ///////

cd backend
    uvicorn main:app --reload --port 8000
cd frontend_web
    python -m http.server 8080



// with streamlit 


cd backend 
uvicorn main:app --reload --host 0.0.0.0 --port 8000

cd frontend_streamlit
    streamlit run app.py







