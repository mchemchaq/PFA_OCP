import os
import pandas as pd
from contract_extractor import FreeContractExtractor
from pathlib import Path

def batch_extract_contracts(folder_path: str, output_file: str = "extracted_contracts.csv"):
    """Extract information from multiple PDF contracts in a folder"""
    
    extractor = FreeContractExtractor()
    results = []
    
    # Get all PDF files in the folder
    pdf_files = list(Path(folder_path).glob("*.pdf"))
    
    if not pdf_files:
        print(f"❌ No PDF files found in {folder_path}")
        return
    
    print(f"🔍 Found {len(pdf_files)} PDF files to process...")
    
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"Processing {i}/{len(pdf_files)}: {pdf_file.name}")
        
        try:
            result = extractor.extract_to_dict(str(pdf_file))
            result['Filename'] = pdf_file.name
            results.append(result)
            print(f"✅ Processed: {pdf_file.name}")
        except Exception as e:
            print(f"❌ Error processing {pdf_file.name}: {str(e)}")
            # Add empty result with filename
            empty_result = {key: None for key in ['Contract Number', 'Supplier', 'Client', 'Object', 'Total Amount', 'Currency', 'Date', 'Location']}
            empty_result['Filename'] = pdf_file.name
            empty_result['Error'] = str(e)
            results.append(empty_result)
    
    # Save results to CSV
    if results:
        df = pd.DataFrame(results)
        df.to_csv(output_file, index=False)
        print(f"📊 Results saved to: {output_file}")
        print(f"✅ Successfully processed {len([r for r in results if 'Error' not in r])} contracts")
    else:
        print("❌ No results to save")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python batch_extractor.py <folder_path> [output_file.csv]")
        print("Example: python batch_extractor.py ./contracts/ results.csv")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "extracted_contracts.csv"
    
    batch_extract_contracts(folder_path, output_file)
