from flask import Blueprint, request, render_template_string, redirect, url_for, session, send_file, make_response
import os
from app.utils.config import Config

files_bp = Blueprint('files', __name__)

@files_bp.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
            
        # VULNERABILITY: 4. Missing input validation on file upload
        if not os.path.exists(Config.UPLOAD_FOLDER):
            os.makedirs(Config.UPLOAD_FOLDER)
        
        file.save(os.path.join(Config.UPLOAD_FOLDER, file.filename))
        return redirect(url_for('files.list_files'))
        
    return """
    <h1>Upload File</h1>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="Upload">
    </form>
    <a href="/">Home</a>
    """
    
@files_bp.route('/files')
def list_files():
    if not os.path.exists(Config.UPLOAD_FOLDER):
        os.makedirs(Config.UPLOAD_FOLDER)
    files = os.listdir(Config.UPLOAD_FOLDER)
    files_html = "".join([f'<li><a href="{url_for("files.download_file", file=f)}">{f}</a></li>' for f in files])
    return f"""
    <h1>Files</h1>
    <ul>{files_html}</ul>
    <p>Try accessing system files via the URL parameter!</p>
    <a href="{url_for('files.upload_file')}">Upload New File</a>
    """

@files_bp.route('/download')
def download_file():
    filename = request.args.get('file')
    # VULNERABILITY: 6. Path traversal
    filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
    try:
        if os.path.exists(filepath):
            return send_file(filepath, as_attachment=True)
        else:
            return "File not found", 404
    except Exception as e:
        return str(e), 500
