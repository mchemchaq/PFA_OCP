# backend/contract_extractor.py
import fitz
import re
from transformers import pipeline

class FreeContractExtractor:
    _instance = None # Singleton pattern
    _qa_pipeline = None # Store the pipeline directly

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(FreeContractExtractor, cls).__new__(cls)
            cls._qa_pipeline = pipeline(
                "question-answering",
                model="mrm8488/bert-multi-cased-finetuned-xquadv1"
            )
            print("Initialized multilingual QA model (mrm8488/bert-multi-cased-finetuned-xquadv1).")
        return cls._instance

    def _extract_text_from_pdf(self, pdf_path):
        text = ""
        try:
            document = fitz.open(pdf_path)
            for page_num in range(len(document)):
                page = document.load_page(page_num)
                text += page.get_text("text")
            document.close()
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            raise
        return text
    
    def _chunk_text(self, text, max_words=400):
        words = text.split()
        for i in range(0, len(words), max_words):
            yield " ".join(words[i:i+max_words])

    def ask_question_from_text(self, context, question):
        if not context.strip():
            return None
        try:
            best_answer, best_score = None, 0
            for chunk in self._chunk_text(context):
                result = self._qa_pipeline(question=question, context=chunk)
                if result and result['score'] > best_score:
                    best_answer, best_score = result['answer'].strip(), result['score']
            return best_answer
        except Exception as e:
            print(f"Error asking question '{question}': {e}")
            return None

    def _regex_extract(self, text, pattern):
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return None

    def _extract_parties_from_domicile(self, text):
        client = self._regex_extract(
            text,
            r"Pour le CLIENT\s*:\s*([\s\S]+?)(?=Pour le PRESTATAIRE)"
        )
        supplier = self._regex_extract(
            text,
            r"Pour le PRESTATAIRE\s*:\s*([\s\S]+?)(?=ARTICLE|\Z)"
        )
        return client, supplier

    def _extract_object_first_page(self, pdf_path):
        text = ""
        try:
            document = fitz.open(pdf_path)
            first_page = document.load_page(0)
            text = first_page.get_text("text")
            document.close()
        except Exception as e:
            print(f"Error reading first page: {e}")
            return None

        match = re.search(
            r"POUR\s+([\s\S]{20,300})",
            text,
            re.IGNORECASE
        )
        if match:
            obj = match.group(1).strip()
            obj = re.split(r"\n\d{4}|\nARTICLE", obj)[0].strip()
            return obj
        return None

    def extract_to_dict(self, pdf_path):
        extracted_data = {
            "Contract Number": None,
            "Supplier": None,
            "Client": None,
            "Object": None,
            "Total Amount": None,
            "Currency": None,
            "Date": None,
            "Location": None,
        }

        full_text = self._extract_text_from_pdf(pdf_path)
        if not full_text:
            raise ValueError("Could not extract any text from the PDF.")

        extracted_data["Contract Number"] = self._regex_extract(full_text, r"CONTRAT\s*(?:N°|No)\s*([A-Z0-9/.-]+)")
        extracted_data["Total Amount"] = self._regex_extract(full_text, r"Montant\s+(?:HT|total)[^\d]*([\d\s.,]+)")
        extracted_data["Currency"] = self._regex_extract(full_text, r"\b(MAD|Dirhams?|DH|EUR|USD)\b")

        answer = self.ask_question_from_text(full_text, "Où le contrat a-t-il été signé ou le lieu mentionné ?")
        if answer:
            extracted_data["Location"] = answer
        
        client, supplier = self._extract_parties_from_domicile(full_text)
        if client:
            extracted_data["Client"] = client.split("\n")[0].strip()
        if supplier:
            extracted_data["Supplier"] = supplier.split("\n")[0].replace("Nom de la Société", "").strip()
        
        obj = self._extract_object_first_page(pdf_path)
        if obj:
            extracted_data["Object"] = obj

        if extracted_data["Total Amount"]:
            extracted_data["Total Amount"] = extracted_data["Total Amount"].replace(" ", "").replace(",", ".")

        if extracted_data["Currency"]:
            extracted_data["Currency"] = extracted_data["Currency"].upper()

        return extracted_data, full_text # Return full_text as well