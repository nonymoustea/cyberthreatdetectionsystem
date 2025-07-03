from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
import sys
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
import json
import platform
from attachment_processor import predict_attachment

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'

# Cross-platform upload folder configuration
if platform.system() == 'Windows':
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
else:
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists with proper permissions
try:
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    # Test write permissions
    test_file = os.path.join(app.config['UPLOAD_FOLDER'], 'test_permissions.tmp')
    with open(test_file, 'w') as f:
        f.write('test')
    os.remove(test_file)
    print(f"✅ Upload directory ready: {app.config['UPLOAD_FOLDER']}")
except Exception as e:
    print(f"❌ Error setting up upload directory: {e}")
    print("Please ensure the application has write permissions to the current directory")

# Store analysis history in memory (in production, use a database)
analysis_history = []

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_analysis_result(filename, result, confidence=None):
    """Save analysis result to history"""
    analysis_data = {
        'id': str(uuid.uuid4()),
        'filename': filename,
        'result': result,
        'confidence': confidence,
        'timestamp': datetime.now().isoformat(),
        'threat_level': 'HIGH' if result == 'Phishing' else 'LOW'
    }
    analysis_history.append(analysis_data)
    return analysis_data


@app.route('/')
def index():
    """Main dashboard page"""
    recent_analyses = sorted(analysis_history, key=lambda x: x['timestamp'], reverse=True)[:10]
    
    # Calculate statistics
    total_files = len(analysis_history)
    phishing_count = len([a for a in analysis_history if a['result'] == 'Phishing'])
    legitimate_count = len([a for a in analysis_history if a['result'] == 'Legitimate'])
    
    stats = {
        'total_files': total_files,
        'phishing_count': phishing_count,
        'legitimate_count': legitimate_count,
        'phishing_rate': round((phishing_count / total_files * 100) if total_files > 0 else 0, 1)
    }
    
    return render_template('dashboard.html', 
                         recent_analyses=recent_analyses, 
                         stats=stats)


@app.route('/analyze')
def analyze_page():
    """File upload and analysis page"""
    return render_template('analyze.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and analysis"""
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add timestamp to avoid filename conflicts
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Analyze the file
            result = predict_attachment(filepath)
            
            # Save analysis result
            analysis_data = save_analysis_result(file.filename, result)
            
            # Clean up uploaded file
            os.remove(filepath)
            
            flash(f'Analysis complete: {result}', 
                  'success' if result == 'Legitimate' else 'warning')
            
            return redirect(url_for('result', analysis_id=analysis_data['id']))
            
        except Exception as e:
            # Clean up uploaded file in case of error
            if os.path.exists(filepath):
                os.remove(filepath)
            flash(f'Error analyzing file: {str(e)}', 'error')
            return redirect(request.url)
    else:
        flash('Invalid file type. Please upload txt, pdf, or image files.', 'error')
        return redirect(request.url)


@app.route('/result/<analysis_id>')
def result(analysis_id):
    """Display analysis result"""
    analysis = next((a for a in analysis_history if a['id'] == analysis_id), None)
    if not analysis:
        flash('Analysis not found', 'error')
        return redirect(url_for('index'))
    
    return render_template('result.html', analysis=analysis)


@app.route('/history')
def history():
    """Display analysis history"""
    sorted_history = sorted(analysis_history, key=lambda x: x['timestamp'], reverse=True)
    return render_template('history.html', analyses=sorted_history)


@app.route('/api/stats')
def api_stats():
    """API endpoint for dashboard statistics"""
    total_files = len(analysis_history)
    phishing_count = len([a for a in analysis_history if a['result'] == 'Phishing'])
    legitimate_count = len([a for a in analysis_history if a['result'] == 'Legitimate'])
    
    return jsonify({
        'total_files': total_files,
        'phishing_count': phishing_count,
        'legitimate_count': legitimate_count,
        'phishing_rate': round((phishing_count / total_files * 100) if total_files > 0 else 0, 1)
    })


@app.route('/api/recent')
def api_recent():
    """API endpoint for recent analyses"""
    recent = sorted(analysis_history, key=lambda x: x['timestamp'], reverse=True)[:5]
    return jsonify(recent)


if __name__ == '__main__':
    # Cross-platform startup configuration
    system_info = {
        'system': platform.system(),
        'python_version': sys.version.split()[0],
        'platform': platform.platform()
    }
    
    print("🛡️  AI Email Threat Detector Starting...")
    print(f"📊 System: {system_info['system']}")
    print(f"🐍 Python: {system_info['python_version']}")
    print(f"💻 Platform: {system_info['platform']}")
    print("=" * 50)
    
    try:
        # Use different default host for Windows vs Unix
        if platform.system() == 'Windows':
            app.run(debug=True, host='127.0.0.1', port=5050)
        else:
            app.run(debug=True, host='0.0.0.0', port=5050)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("💡 Try running with a different port: python app.py --port 8080")
        sys.exit(1) 