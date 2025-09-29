from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify, current_app
import os
from werkzeug.utils import secure_filename
from app.services.openai_service import OpenAIImageService
from app.utils.file_utils import save_uploaded_file
import uuid

design_bp = Blueprint('design', __name__)

# Design options
ROOM_TYPES = [
    'living room', 'bedroom', 'kitchen', 'bathroom', 'dining room',
    'home office', 'hallway', 'basement', 'attic', 'garage'
]

DESIGN_STYLES = [
    'modern', 'contemporary', 'minimalist', 'scandinavian', 'industrial',
    'bohemian', 'traditional', 'rustic', 'art deco', 'mid-century modern',
    'farmhouse', 'mediterranean', 'victorian', 'eclectic'
]

COLOR_PALETTES = [
    'any', 'neutral', 'warm', 'cool', 'earth tones', 'monochrome',
    'bold and vibrant', 'pastel', 'jewel tones', 'black and white'
]

@design_bp.route('/')
def design_home():
    """Main design tool page."""
    if 'username' not in session:
        flash('Please log in to use the design tools', 'warning')
        return redirect(url_for('auth.login'))
    
    return render_template('design/home.html',
                         room_types=ROOM_TYPES,
                         design_styles=DESIGN_STYLES,
                         color_palettes=COLOR_PALETTES)

@design_bp.route('/upload', methods=['POST'])
def upload_image():
    """Handle image upload and initial processing."""
    if 'username' not in session:
        return jsonify({'success': False, 'error': 'Please log in first'}), 401
    
    if 'image' not in request.files:
        return jsonify({'success': False, 'error': 'No image file provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400
    
    # Save the uploaded file
    success, result, filepath = save_uploaded_file(file)
    
    if not success:
        return jsonify({'success': False, 'error': result}), 400
    
    # Store file info in session for the redesign process
    session['uploaded_image'] = {
        'filename': result,
        'filepath': filepath,
        'original_name': file.filename
    }
    
    return jsonify({
        'success': True,
        'filename': result,
        'message': 'Image uploaded successfully'
    })

@design_bp.route('/redesign', methods=['POST'])
def redesign_image():
    """Process image redesign using OpenAI."""
    if 'username' not in session:
        return jsonify({'success': False, 'error': 'Please log in first'}), 401
    
    if 'uploaded_image' not in session:
        return jsonify({'success': False, 'error': 'No image uploaded'}), 400
    
    try:
        # Get form data
        room_type = request.form.get('room_type', 'living room')
        design_style = request.form.get('design_style', 'modern')
        color_palette = request.form.get('color_palette', 'any')
        is_furnished = request.form.get('furnished') == 'furnished'
        user_prompt = request.form.get('user_prompt', '').strip()
        
        # Get uploaded image info
        image_info = session['uploaded_image']
        image_path = image_info['filepath']
        
        # Initialize OpenAI service
        openai_service = OpenAIImageService()
        
        # Generate comprehensive prompt
        prompt = openai_service.generate_design_prompt(
            room_type, design_style, color_palette, is_furnished, user_prompt
        )
        
        # Process the image
        result = openai_service.edit_image(image_path, prompt)
        
        if result['success']:
            # Generate unique filename for the result
            result_filename = f"redesign_{uuid.uuid4().hex}.png"
            result_path = os.path.join(current_app.config['UPLOAD_FOLDER'], result_filename)
            
            # Download and save the generated image
            if openai_service.download_generated_image(result['image_url'], result_path):
                # Store result in session
                session['redesign_result'] = {
                    'original_filename': image_info['filename'],
                    'result_filename': result_filename,
                    'prompt_used': result['prompt_used'],
                    'room_type': room_type,
                    'design_style': design_style,
                    'color_palette': color_palette,
                    'is_furnished': is_furnished,
                    'user_prompt': user_prompt
                }
                
                return jsonify({
                    'success': True,
                    'result_filename': result_filename,
                    'prompt_used': result['prompt_used']
                })
            else:
                return jsonify({'success': False, 'error': 'Failed to save generated image'}), 500
        else:
            return jsonify({'success': False, 'error': result['error']}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': f'Processing error: {str(e)}'}), 500

@design_bp.route('/result')
def view_result():
    """Display the redesign result."""
    if 'username' not in session:
        flash('Please log in to view results', 'warning')
        return redirect(url_for('auth.login'))
    
    if 'redesign_result' not in session:
        flash('No redesign result found', 'error')
        return redirect(url_for('design.design_home'))
    
    result_data = session['redesign_result']
    return render_template('design/result.html', result=result_data)

@design_bp.route('/gallery')
def gallery():
    """View user's design history/gallery."""
    if 'username' not in session:
        flash('Please log in to view gallery', 'warning')
        return redirect(url_for('auth.login'))
    
    # In a real app, you'd fetch this from a database
    # For now, we'll just show the current session result if available
    results = []
    if 'redesign_result' in session:
        results.append(session['redesign_result'])
    
    return render_template('design/gallery.html', results=results)

@design_bp.route('/clear-session')
def clear_session():
    """Clear design-related session data."""
    session.pop('uploaded_image', None)
    session.pop('redesign_result', None)
    flash('Session cleared', 'info')
    return redirect(url_for('design.design_home'))
