import fitz  # PyMuPDF for PDF processing
import re
from transformers import pipeline
import os


class FreeContractExtractor:
    def __init__(self):
        # Multilingual model for QA (works better with French)
        self.qa_pipeline = pipeline(
            "question-answering",
            model="mrm8488/bert-multi-cased-finetuned-xquadv1"
        )
        print("Initialized multilingual QA model (mrm8488/bert-multi-cased-finetuned-xquadv1).")

    def _extract_text_from_pdf(self, pdf_path):
        """Extracts text from a PDF file."""
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
        """Split text into chunks so QA model can handle it."""
        words = text.split()
        for i in range(0, len(words), max_words):
            yield " ".join(words[i:i+max_words])

    def _ask_question(self, context, question):
        if not context.strip():
            return None
        try:
            best_answer, best_score = None, 0
            # Run QA over chunks
            for chunk in self._chunk_text(context):
                result = self.qa_pipeline(question=question, context=chunk)
                if result and result['score'] > best_score:
                    best_answer, best_score = result['answer'].strip(), result['score']
            return best_answer
        except Exception as e:
            print(f"Error asking question '{question}': {e}")
            return None


    def _regex_extract(self, text, pattern):
        """Helper for regex extraction"""
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return None
    #///////////////////////////////////////////////////////////////////
    def _extract_parties_from_domicile(self, text):
        """
        Extract Client and Supplier details from Article 28 (Election de domicile).
        """
        client = self._regex_extract(
            text,
            r"Pour le CLIENT\s*:\s*([\s\S]+?)(?=Pour le PRESTATAIRE)"
        )
        supplier = self._regex_extract(
            text,
            r"Pour le PRESTATAIRE\s*:\s*([\s\S]+?)(?=ARTICLE|\Z)"
        )
        return client, supplier
    #///////////////////////////////////////////////////////////////////
    def _extract_object_first_page(self, pdf_path):
        """
        Extracts contract Object from the first page after the keyword 'POUR'.
        """
        text = ""
        try:
            document = fitz.open(pdf_path)
            first_page = document.load_page(0)
            text = first_page.get_text("text")
            document.close()
        except Exception as e:
            print(f"Error reading first page: {e}")
            return None

        # Look for "POUR <object>"
        match = re.search(
            r"POUR\s+([\s\S]{20,300})",  # capture multiple lines after POUR
            text,
            re.IGNORECASE
        )
        if match:
            obj = match.group(1).strip()
            # stop at first line break with year or "Article"
            obj = re.split(r"\n\d{4}|\nARTICLE", obj)[0].strip()
            return obj

        return None


    #///////////////////////////////////////////////////////////////////

    def extract_to_dict(self, pdf_path):
        """
        Extracts key information from a contract PDF using hybrid Regex + QA.
        """
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

        # --- Regex extraction (structured fields) ---
        extracted_data["Contract Number"] = self._regex_extract(full_text, r"CONTRAT\s*(?:N°|No)\s*([A-Z0-9/.-]+)")
        extracted_data["Total Amount"] = self._regex_extract(full_text, r"Montant\s+(?:HT|total)[^\d]*([\d\s.,]+)")
        extracted_data["Currency"] = self._regex_extract(full_text, r"\b(MAD|Dirhams?|DH|EUR|USD)\b")
        extracted_data["Date"] = self._regex_extract(full_text, r"\b(20\d{2})\b")  # simple year match

        answer = self._ask_question(full_text, "Où le contrat a-t-il été signé ou le lieu mentionné ?")
        if answer:
            extracted_data["Location"] = answer
        # Try to use Article 28 first
        client, supplier = self._extract_parties_from_domicile(full_text)
        if client:
            extracted_data["Client"] = client.split("\n")[0].strip()
        if supplier:
            extracted_data["Supplier"] = supplier.split("\n")[0].replace("Nom de la Société", "").strip()
        obj = self._extract_object_first_page(pdf_path)
        if obj:
            extracted_data["Object"] = obj

        # --- QA extraction (free-text fields) ---
        questions = {
            # "Supplier": "Qui est le prestataire ou fournisseur ?",
            # "Client": "Qui est le client ?",
            # "Object": "Quel est l'objet du contrat ?",
        }

        for key, question in questions.items():
            answer = self._ask_question(full_text, question)
            if answer:
                extracted_data[key] = answer

        # Post-processing
        if extracted_data["Total Amount"]:
            extracted_data["Total Amount"] = extracted_data["Total Amount"].replace(" ", "").replace(",", ".")

        if extracted_data["Currency"]:
            extracted_data["Currency"] = extracted_data["Currency"].upper()

        return extracted_data


# Example usage
if __name__ == "__main__":
    extractor = FreeContractExtractor()
    info = extractor.extract_to_dict("CRra.pdf")
    print("\nExtracted Information:")
    for k, v in info.items():
        print(f"{k}: {v}")
