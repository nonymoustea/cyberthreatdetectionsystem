# 🛡️ AI Email Threat Detector - Setup Guide

This guide will help you set up the AI Email Threat Detector on **Windows**, **macOS**, and **Linux** systems.

## 📋 Prerequisites

### All Platforms
- **Python 3.7 or higher**
- **pip** (Python package installer)
- **Git** (optional, for cloning)

### Windows-Specific
- **Microsoft Visual C++ Build Tools** (for some Python packages)
- **Tesseract OCR** - Download from: https://github.com/UB-Mannheim/tesseract/wiki
  - Add Tesseract to your system PATH

### macOS-Specific  
- **Homebrew** (recommended package manager)
- **Tesseract OCR**: `brew install tesseract`

### Linux-Specific
- **Tesseract OCR**: `sudo apt-get install tesseract-ocr` (Ubuntu/Debian)
- **Development tools**: `sudo apt-get install python3-dev`

## 🚀 Quick Start

### Windows
1. **Double-click** `run_windows.bat`
2. **Follow the prompts** - the script will automatically:
   - Check Python installation
   - Install dependencies
   - Start the application
3. **Open your browser** to `http://localhost:5050`

### macOS/Linux
1. **Open Terminal** in the project directory
2. **Run** `./run_unix.sh`
3. **Open your browser** to `http://localhost:5050`

## ⚙️ Manual Setup

### Step 1: Install Python Dependencies

#### Windows
```cmd
# Open Command Prompt or PowerShell
pip install -r requirements.txt
```

#### macOS/Linux
```bash
# Use python3 and pip3 on most systems
python3 -m pip install -r requirements.txt
```

### Step 2: Install Tesseract OCR

#### Windows
1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install the `.exe` file
3. Add to PATH: `C:\Program Files\Tesseract-OCR`
4. Verify: `tesseract --version`

#### macOS
```bash
# Using Homebrew
brew install tesseract

# Using MacPorts
sudo port install tesseract
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
sudo apt-get install libtesseract-dev
```

#### Linux (CentOS/RHEL)
```bash
sudo yum install tesseract
# or for newer versions
sudo dnf install tesseract
```

### Step 3: Verify Installation
```bash
python --version    # or python3 --version
pip --version       # or pip3 --version
tesseract --version
```

### Step 4: Start the Application

#### Windows
```cmd
python app.py
```

#### macOS/Linux
```bash
python3 app.py
```

## 🔧 Configuration

### Environment Variables (Optional)
Create a `.env` file in the project directory:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True

# Security
SECRET_KEY=your-super-secret-key-here

# Upload Configuration
MAX_UPLOAD_SIZE=16777216  # 16MB in bytes
UPLOAD_FOLDER=uploads

# Tesseract Configuration (Windows)
TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
```

### Port Configuration
If port 5050 is already in use, you can change it in `app.py`:
```python
app.run(debug=True, host='127.0.0.1', port=8080)  # Change port here
```

## 🐛 Troubleshooting

### Common Issues

#### ❌ "Python is not installed or not in PATH"
**Solution**: 
- Windows: Reinstall Python from python.org, check "Add to PATH"
- macOS: Install via Homebrew: `brew install python`
- Linux: `sudo apt-get install python3 python3-pip`

#### ❌ "tesseract is not installed or it's not in your PATH"
**Solution**:
- Verify installation: `tesseract --version`
- Add to PATH or set TESSERACT_CMD environment variable
- Windows: Add `C:\Program Files\Tesseract-OCR` to PATH

#### ❌ "Permission denied" errors
**Solution**:
- Windows: Run Command Prompt as Administrator
- macOS/Linux: Use `sudo` for system-wide installations

#### ❌ "Port 5050 is already in use"
**Solutions**:
1. Kill the process using the port
2. Change the port in `app.py`
3. On macOS: Disable AirPlay Receiver in System Preferences

#### ❌ "No module named 'cv2'" or similar import errors
**Solution**:
```bash
pip install opencv-python-headless
pip install --upgrade -r requirements.txt
```

### Platform-Specific Issues

#### Windows
- **Long path issues**: Enable long path support in Windows 10/11
- **Antivirus blocking**: Add project folder to antivirus exceptions
- **PowerShell execution policy**: Run `Set-ExecutionPolicy RemoteSigned`

#### macOS
- **Xcode command line tools**: `xcode-select --install`
- **Certificate issues**: Update certificates or use `--trusted-host` with pip

#### Linux
- **Missing system libraries**: Install `python3-dev`, `libffi-dev`, `libssl-dev`
- **Permission issues**: Don't use `sudo` with pip, use virtual environments

## 🌐 Network Access

### Local Access Only
- Default: `http://localhost:5050` or `http://127.0.0.1:5050`

### Network Access (Advanced)
To allow access from other devices on your network:
1. Change `host='127.0.0.1'` to `host='0.0.0.0'` in `app.py`
2. Access via your local IP: `http://YOUR_IP:5050`
3. **Security Note**: Only do this on trusted networks

## 📊 System Requirements

### Minimum Requirements
- **RAM**: 2GB available
- **Disk**: 500MB free space
- **CPU**: Any modern processor
- **Python**: 3.7+

### Recommended Requirements  
- **RAM**: 4GB+ available
- **Disk**: 1GB+ free space
- **CPU**: Multi-core processor
- **Python**: 3.9+

## 🔐 Security Notes

1. **Change the secret key** in production
2. **Don't expose to the internet** without proper security
3. **Validate file uploads** - the app already does this
4. **Use HTTPS** in production environments
5. **Regular updates** - keep dependencies updated

## 📞 Support

If you encounter issues:
1. Check this troubleshooting guide
2. Verify all dependencies are installed
3. Check the console output for error messages
4. Ensure you have the required system permissions

---

**Made with ❤️ for cybersecurity professionals** 