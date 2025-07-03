# 🛡️ AI-Powered Email Threat Detector

This project uses artificial intelligence to detect phishing and malicious content in various email attachment formats—text, PDFs, and images. It features a **modern web interface** and combines machine learning, OCR, and content extraction techniques to provide early detection of cyber threats embedded in emails.

**✅ Cross-Platform Compatible**: Works on Windows, macOS, and Linux!

---

## 🌟 New Web Interface Features

- **📊 Real-time Dashboard** with threat statistics
- **🔄 File Upload Interface** with drag & drop support
- **📱 Responsive Design** that works on all devices
- **⚡ Live Analysis Results** with detailed recommendations
- **📈 Analysis History** tracking and search
- **🛡️ Enhanced Security Recommendations** based on threat level

---

## 🚀 Quick Start

### Windows Users
1. **Double-click** `run_windows.bat`
2. **Follow the prompts** (installs dependencies automatically)
3. **Open** http://localhost:5050 in your browser

### macOS/Linux Users
1. **Open Terminal** in project directory
2. **Run** `./run_unix.sh`
3. **Open** http://localhost:5050 in your browser

### Manual Start
```bash
# Windows
python app.py

# macOS/Linux  
python3 app.py
```

---

## 📌 Project Objectives

1. **Threat Analysis**: Identify common cyber threats delivered through email attachments
2. **AI Detection System**: Machine learning model to detect phishing across multiple file types
3. **Web Interface**: User-friendly dashboard for threat analysis and management
4. **Cross-Platform Support**: Compatible with Windows, macOS, and Linux systems

---

## 🚀 Features

### Core Detection Features
- 📄 **Multi-Format Support**: `.txt`, `.pdf`, `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`
- 🧠 **AI-Powered Detection**: Trained phishing classifier using machine learning
- 🖼️ **OCR Processing**: Extract and analyze text from images
- 📊 **Confidence Scoring**: Threat level assessment with confidence metrics

### Web Interface Features
- **🎨 Modern UI**: Bootstrap 5 with custom security-focused design
- **📱 Mobile Responsive**: Works perfectly on phones, tablets, and desktops
- **⚡ Real-time Analysis**: Instant file processing and results
- **📈 Statistics Dashboard**: Track threats, analysis history, and trends
- **🔍 Search & Filter**: Find past analyses quickly
- **🛡️ Enhanced Recommendations**: Detailed security guidance based on results

---

## 🧰 Project Structure

```
cyberthreatdetectionn/
├── app.py                      # Main Flask web application
├── templates/                  # HTML templates
│   ├── base.html              # Base template
│   ├── dashboard.html         # Main dashboard
│   ├── analyze.html           # File upload page
│   ├── result.html            # Analysis results
│   └── history.html           # Analysis history
├── static/                     # Web assets
│   ├── css/style.css          # Custom styling
│   └── js/main.js             # JavaScript functionality
├── attachment_processor.py     # File analysis engine
├── train_model.py             # Model training script
├── test_predictor.py          # Testing script
├── email_fetcher.py           # Email processing (optional)
├── text_model.pkl             # Trained ML model
├── text_vectorizer.pkl        # TF-IDF vectorizer
├── phishing_emails.csv        # Training dataset
├── requirements.txt           # Python dependencies
├── run_windows.bat            # Windows launcher
├── run_unix.sh               # Unix/Linux/macOS launcher
├── SETUP.md                  # Detailed setup guide
└── README.md                 # This file
```

---

## 📦 Installation & Setup

### Automatic Setup (Recommended)

#### Windows
```cmd
# Double-click or run in Command Prompt
run_windows.bat
```

#### macOS/Linux
```bash
# Make executable and run
chmod +x run_unix.sh
./run_unix.sh
```

### Manual Setup

1. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Tesseract OCR**
   - **Windows**: Download from [UB-Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)
   - **macOS**: `brew install tesseract`
   - **Linux**: `sudo apt-get install tesseract-ocr`

3. **Start the Application**
   ```bash
   python app.py  # Windows
   python3 app.py # macOS/Linux
   ```

4. **Open in Browser**
   Navigate to: http://localhost:5050

---

## 🎯 Usage Guide

### 1. Dashboard Overview
- **Statistics Cards**: View total files analyzed, threats detected, and safety metrics
- **Recent Analyses**: Quick access to latest threat assessments
- **Quick Actions**: Direct links to analyze files or view history

### 2. File Analysis
- **Upload Files**: Drag & drop or click to select files
- **Supported Formats**: TXT, PDF, PNG, JPG, JPEG, GIF, BMP (max 16MB)
- **Real-time Processing**: See results immediately after upload
- **Detailed Results**: Comprehensive threat assessment with recommendations

### 3. Security Recommendations
- **Threat-Specific Guidance**: Different advice for phishing vs. legitimate files
- **Action Checklists**: Step-by-step security procedures
- **Emergency Contacts**: Quick access to IT security resources
- **Prevention Tips**: Learn how to avoid future threats

### 4. History Management
- **Search & Filter**: Find specific analyses quickly
- **Export Data**: Copy analysis IDs and results
- **Trend Analysis**: View threat patterns over time

---

## 🔧 Configuration

### Environment Variables
Create `.env` file for custom configuration:
```env
FLASK_ENV=development
SECRET_KEY=your-secret-key
MAX_UPLOAD_SIZE=16777216
UPLOAD_FOLDER=uploads
TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe  # Windows only
```

### Port Configuration
Change port in `app.py` if 5050 is unavailable:
```python
app.run(debug=True, host='127.0.0.1', port=8080)
```

---

## 🧠 Training Your Own Model

1. **Get Dataset**: Download phishing emails dataset from [Kaggle](https://www.kaggle.com/datasets/naserabdullahalam/phishing-email-dataset)
2. **Save as**: `phishing_emails.csv` in project root
3. **Train Model**: 
   ```bash
   python train_model.py
   ```
4. **Generated Files**: `text_model.pkl` and `text_vectorizer.pkl`

---

## 🐛 Troubleshooting

### Common Issues

**❌ Port 5050 in use**
- Solution: Change port in `app.py` or kill process using port

**❌ Tesseract not found**
- Windows: Add `C:\Program Files\Tesseract-OCR` to PATH
- macOS: `brew install tesseract`
- Linux: `sudo apt-get install tesseract-ocr`

**❌ Permission errors**
- Windows: Run as Administrator
- Unix: Check file permissions, use `sudo` if needed

**❌ Import errors**
- Solution: `pip install --upgrade -r requirements.txt`

📖 **See [SETUP.md](SETUP.md) for detailed troubleshooting guide**

---

## 🔐 Security Features

- **File Validation**: Strict file type and size checking
- **Secure Upload**: Temporary file handling with automatic cleanup
- **Input Sanitization**: Protection against malicious uploads
- **Cross-Platform Security**: Safe operation on all operating systems

---

## 📊 System Requirements

### Minimum
- **OS**: Windows 10, macOS 10.14, or Linux (Ubuntu 18.04+)
- **Python**: 3.7+
- **RAM**: 2GB available
- **Disk**: 500MB free space

### Recommended
- **OS**: Latest versions of Windows, macOS, or Linux
- **Python**: 3.9+
- **RAM**: 4GB+ available
- **Disk**: 1GB+ free space

---

## 🙌 Acknowledgements

- **[Flask](https://flask.palletsprojects.com/)** - Web framework
- **[Bootstrap](https://getbootstrap.com/)** - UI framework
- **[scikit-learn](https://scikit-learn.org/)** - Machine learning
- **[pytesseract](https://github.com/madmaze/pytesseract)** - OCR processing
- **[pdfminer.six](https://github.com/pdfminer/pdfminer.six)** - PDF text extraction
- **[Font Awesome](https://fontawesome.com/)** - Icons
- **[Kaggle Dataset](https://www.kaggle.com/datasets/naserabdullahalam/phishing-email-dataset)** - Training data

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**🛡️ Built for cybersecurity professionals and organizations serious about email threat detection.**
