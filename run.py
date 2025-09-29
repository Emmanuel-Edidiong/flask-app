from app import create_app
import os

# Create the Flask application
app = create_app()

if __name__ == '__main__':
    # Get port from environment or default to 5001
    port = int(os.environ.get('PORT', 5001))
    
    # Run the application
    app.run(
        host='0.0.0.0',
        port=port,
        debug=app.config.get('DEBUG', True)
    )
