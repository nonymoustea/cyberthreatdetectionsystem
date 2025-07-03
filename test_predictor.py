from attachment_processor import predict_attachment
import os

# Test files (ensure these exist in the same directory)
test_files = ['sample_email.txt', 'sample_invoice.pdf', 'phishing_screenshot.png']

for file_path in test_files:
    if os.path.exists(file_path):
        result = predict_attachment(file_path)
        print(f'{file_path} => {result}')
    else:
        print(f'{file_path} not found. Please ensure the test files are available.')
