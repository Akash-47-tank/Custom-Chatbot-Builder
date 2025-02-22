# Custom Chatbot Builder for Small Businesses

A professional chatbot builder that allows small businesses to create custom AI chatbots using their FAQs and business information. Optimized for Apple Silicon (M1) Macs.

## Features

- Easy-to-use interface for inputting business details and FAQs
- Automatic chatbot training using state-of-the-art NLP models
- Optimized performance using Apple M1's MPS backend
- Export functionality for integration with various platforms
- Comprehensive logging and error handling
- Professional, modular codebase

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/custom-chatbot-builder.git
cd custom-chatbot-builder
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On macOS
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

Custom_Chatbot_Builder_for_Small_Businesses/
├── assets/                    # Screenshots and images
│   ├── chat_interface.png
│   └── training_interface.png
├── src/                      # Source code
│   └── chatbot/
│       ├── api/             # API endpoints
│       ├── config/          # Configuration files
│       ├── data/           # Data processing modules
│       └── models/         # ML model training and inference
├── data/                    # Training data and exports
│   └── chatbot_export.json
├── requirements.txt         # Project dependencies
└── README.md               # Project documentation

## Screenshots

### Chat Interface
![Chat Interface](assets/chat_interface.png)

### Training Interface
![Training Interface](assets/training_interface.png)

## Usage

1. Start the Gradio interface:
```bash
python src/chatbot/api/app.py
```

2. Open your browser and navigate to the displayed URL
3. Input your business details and FAQs
4. Train and test your custom chatbot
5. Export the chatbot configuration for integration

## Development

- Run tests: `pytest tests/`
- Format code: `black src/ tests/`
- Sort imports: `isort src/ tests/`
- Lint code: `flake8 src/ tests/`

