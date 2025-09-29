import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_uploaded_file(file, upload_folder=None):
    """
    Save uploaded file with a unique name.
    
    Args:
        file: FileStorage object from request.files
        upload_folder: Optional custom upload folder
    
    Returns:
        tuple: (success, filename_or_error_message, filepath)
    """
    if not file or file.filename == '':
        return False, 'No file selected', None
    
    if not allowed_file(file.filename):
        return False, 'File type not allowed', None
    
    try:
        # Generate unique filename
        original_filename = secure_filename(file.filename)
        file_extension = original_filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
        
        # Use provided folder or default
        folder = upload_folder or current_app.config['UPLOAD_FOLDER']
        filepath = os.path.join(folder, unique_filename)
        
        # Save the file
        file.save(filepath)
        
        return True, unique_filename, filepath
    
    except Exception as e:
        return False, f'Error saving file: {str(e)}', None

def get_file_size_mb(filepath):
    """Get file size in MB."""
    try:
        size_bytes = os.path.getsize(filepath)
        size_mb = size_bytes / (1024 * 1024)
        return round(size_mb, 2)
    except:
        return 0

def cleanup_old_files(directory, max_age_hours=24):
    """Remove files older than specified hours."""
    import time
    
    try:
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                file_age = current_time - os.path.getmtime(filepath)
                if file_age > max_age_seconds:
                    os.remove(filepath)
    except Exception as e:
        print(f"Error cleaning up files: {str(e)}")
