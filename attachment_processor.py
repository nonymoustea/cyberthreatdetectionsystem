import mimetypes
import os
import platform
from PIL import Image
import pytesseract
from pdfminer.high_level import extract_text
import joblib

# Windows-specific Tesseract configuration
if platform.system() == 'Windows':
    # Common Windows Tesseract installation paths
    possible_paths = [
        r'C:\Program Files\Tesseract-OCR\tesseract.exe',
        r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
        r'C:\Users\{}\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'.format(os.getenv('USERNAME', '')),
    ]
    
    # Try to find Tesseract executable
    for path in possible_paths:
        if os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            break
    else:
        # If not found in common paths, try environment variable
        tesseract_cmd = os.getenv('TESSERACT_CMD')
        if tesseract_cmd and os.path.exists(tesseract_cmd):
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

def process_pdf_attachment(file_path):
    return extract_text(file_path)

def process_image_attachment(file_path):
    image = Image.open(file_path)
    return pytesseract.image_to_string(image)

def process_text_attachment(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def predict_attachment(file_path):
    try:
        # Use cross-platform path handling
        if not os.path.exists(file_path):
            return 'File not found'
            
        model = joblib.load('text_model.pkl')
        vectorizer = joblib.load('text_vectorizer.pkl')

        mimetype, _ = mimetypes.guess_type(file_path)
        
        # More robust file type detection
        file_extension = os.path.splitext(file_path)[1].lower()
        
        try:
            if mimetype == 'application/pdf' or file_extension == '.pdf':
                content = process_pdf_attachment(file_path)
            elif (mimetype and mimetype.startswith('image/')) or file_extension in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']:
                content = process_image_attachment(file_path)
            elif mimetype == 'text/plain' or file_extension == '.txt':
                content = process_text_attachment(file_path)
            else:
                return 'Unsupported file type'
        except Exception as e:
            return f'Error processing file: {str(e)}'

        if not content or content.strip() == '':
            return 'No content extracted from file'

        features = vectorizer.transform([content])
        prediction = model.predict(features)[0]
        return 'Phishing' if prediction == 1 else 'Legitimate'
        
    except FileNotFoundError:
        return 'Model files not found. Please ensure text_model.pkl and text_vectorizer.pkl exist.'
    except Exception as e:
        return f'Prediction error: {str(e)}'
