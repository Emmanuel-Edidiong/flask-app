# Interior Design AI

An AI-powered interior design tool that transforms room images using OpenAI's image editing capabilities.

## Features

- **Image Upload**: Upload photos of any room
- **Design Customization**: Choose from multiple room types, design styles, and color palettes
- **AI Processing**: Uses OpenAI's DALL-E for realistic interior redesigns
- **User Authentication**: Simple username-based login system
- **Gallery**: View and download your design history
- **Responsive Design**: Works on desktop and mobile devices

## Design Options

### Room Types
- Living Room, Bedroom, Kitchen, Bathroom, Dining Room
- Home Office, Hallway, Basement, Attic, Garage

### Design Styles
- Modern, Contemporary, Minimalist, Scandinavian, Industrial
- Bohemian, Traditional, Rustic, Art Deco, Mid-Century Modern
- Farmhouse, Mediterranean, Victorian, Eclectic

### Color Palettes
- Any, Neutral, Warm, Cool, Earth Tones, Monochrome
- Bold and Vibrant, Pastel, Jewel Tones, Black and White

## Setup Instructions

### Prerequisites
- Python 3.8+
- OpenAI API key

### Installation

1. **Clone or download the project**
   ```bash
   cd flask-app
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

5. **Run the application**
   ```bash
   python run.py
   ```

6. **Access the app**
   Open your browser and go to `http://localhost:5001`

## Project Structure

```
flask-app/
├── app/
│   ├── __init__.py              # Application factory
│   ├── blueprints/              # Flask blueprints
│   │   ├── main.py             # Main routes
│   │   ├── auth.py             # Authentication
│   │   └── design.py           # Design tool functionality
│   ├── services/               # Business logic
│   │   └── openai_service.py   # OpenAI integration
│   ├── utils/                  # Utility functions
│   │   └── file_utils.py       # File handling utilities
│   ├── static/                 # Static files
│   │   ├── css/               # Stylesheets
│   │   ├── js/                # JavaScript files
│   │   ├── images/            # Static images
│   │   └── uploads/           # User uploaded files
│   └── templates/             # HTML templates
│       ├── auth/              # Authentication templates
│       ├── design/            # Design tool templates
│       └── base.html          # Base template
├── config/
│   └── config.py              # Configuration settings
├── requirements.txt           # Dependencies
├── run.py                    # Application entry point
└── .env.example              # Environment variables template
```

## Usage

1. **Login**: Enter any username to get started
2. **Upload Image**: Take a photo of your room and upload it
3. **Customize**: Select room type, design style, color palette, and furniture preferences
4. **Generate**: Click "Generate Design" and wait for AI processing
5. **Download**: View the before/after comparison and download your redesigned room

## API Integration

This app uses OpenAI's DALL-E image editing API. You'll need:
- An OpenAI API account
- API key with access to image editing endpoints
- Sufficient API credits for image processing

## Technologies Used

- **Backend**: Flask, Python
- **Frontend**: Bootstrap 5, JavaScript
- **AI**: OpenAI DALL-E Image Editing API
- **Image Processing**: Pillow (PIL)
- **File Handling**: Werkzeug

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational purposes. Please respect OpenAI's terms of service when using their API.

## Support

For issues or questions, please check the OpenAI API documentation or create an issue in the project repository.
