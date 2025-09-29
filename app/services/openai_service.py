import openai
import os
import requests
from PIL import Image
import io
import base64
from flask import current_app

class OpenAIImageService:
    """Service class for OpenAI image operations."""
    
    def __init__(self):
        openai.api_key = current_app.config.get('OPENAI_API_KEY')
    
    @staticmethod
    def allowed_file(filename):
        """Check if file extension is allowed."""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']
    
    def prepare_image_for_openai(self, image_path):
        """Prepare image for OpenAI API by ensuring it's in the right format."""
        try:
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize if too large (OpenAI has size limits)
                max_size = (1024, 1024)
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                # Save to bytes
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='PNG')
                img_byte_arr.seek(0)
                
                return img_byte_arr
        except Exception as e:
            raise Exception(f"Error preparing image: {str(e)}")
    
    def generate_design_prompt(self, room_type, design_style, color_palette, 
                             is_furnished, user_prompt):
        """Generate a comprehensive prompt for interior design."""
        base_prompt = f"Transform this {room_type} interior into a {design_style} style design"
        
        if color_palette and color_palette != 'any':
            base_prompt += f" using a {color_palette} color palette"
        
        if is_furnished:
            base_prompt += " with modern, stylish furniture and decor"
        else:
            base_prompt += " focusing on architectural elements, keeping it minimally furnished"
        
        if user_prompt:
            base_prompt += f". Additional requirements: {user_prompt}"
        
        base_prompt += ". Maintain the room's basic structure and lighting. Make it photorealistic and professionally designed."
        
        return base_prompt
    
    def edit_image(self, image_path, prompt, mask_path=None):
        """
        Edit an image using OpenAI's image editing API.
        
        Args:
            image_path: Path to the original image
            prompt: Text description of desired changes
            mask_path: Optional path to mask image (for selective editing)
        
        Returns:
            Dictionary with success status and result data
        """
        try:
            if not openai.api_key:
                return {
                    'success': False, 
                    'error': 'OpenAI API key not configured'
                }
            
            # Prepare the image
            image_data = self.prepare_image_for_openai(image_path)
            
            # Prepare the request parameters
            request_params = {
                'prompt': prompt,
                'n': 1,
                'size': '1024x1024',
                'response_format': 'url'
            }
            
            # If mask is provided, use the edit endpoint
            if mask_path:
                mask_data = self.prepare_image_for_openai(mask_path)
                response = openai.Image.create_edit(
                    image=image_data,
                    mask=mask_data,
                    **request_params
                )
            else:
                # Use variation/edit without mask
                response = openai.Image.create_edit(
                    image=image_data,
                    **request_params
                )
            
            if response.data:
                image_url = response.data[0].url
                return {
                    'success': True,
                    'image_url': image_url,
                    'prompt_used': prompt
                }
            else:
                return {
                    'success': False,
                    'error': 'No image generated'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'OpenAI API error: {str(e)}'
            }
    
    def download_generated_image(self, image_url, save_path):
        """Download the generated image from OpenAI and save it locally."""
        try:
            response = requests.get(image_url)
            response.raise_for_status()
            
            with open(save_path, 'wb') as f:
                f.write(response.content)
            
            return True
        except Exception as e:
            print(f"Error downloading image: {str(e)}")
            return False
