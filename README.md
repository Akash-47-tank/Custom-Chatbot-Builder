# Custom Chatbot Builder for Small Businesses

<div align="center">

![GitHub](https://img.shields.io/github/license/yourusername/custom-chatbot-builder)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-macOS%20(M1)-lightgrey)

</div>

A professional chatbot builder that allows small businesses to create custom AI chatbots using their FAQs and business information. Optimized for Apple Silicon (M1) Macs.

## 🌟 Features

- 🤖 Easy-to-use interface for inputting business details and FAQs
- 🧠 Automatic chatbot training using state-of-the-art NLP models
- ⚡️ Optimized performance using Apple M1's MPS backend
- 📤 Export functionality for integration with various platforms
- 📝 Comprehensive logging and error handling
- 🏗️ Professional, modular codebase

## 📦 Project Structure

```
📦 Custom_Chatbot_Builder
 ┣ 📂 assets
 ┃ ┣ 🖼️ chat_interface.png
 ┃ ┗ 🖼️ training_interface.png
 ┣ 📂 src
 ┃ ┗ 📂 chatbot
 ┃   ┣ 📂 api          ⚡️ REST API endpoints
 ┃   ┣ 📂 config       ⚙️ Configuration files
 ┃   ┣ 📂 data         🔄 Data processing modules
 ┃   ┗ 📂 models       🧠 ML model training & inference
 ┣ 📂 data
 ┃ ┗ 📄 chatbot_export.json   💾 Training data & exports
 ┣ 📄 requirements.txt        📦 Project dependencies
 ┗ 📄 README.md              📚 Documentation
```

## 🖼️ Screenshots

<div align="center">
  <img src="assets/chat_interface.png" alt="Chat Interface" width="80%" />
  <p><em>Chat Interface - Interact with your trained chatbot</em></p>
  
  <img src="assets/training_interface.png" alt="Training Interface" width="80%" />
  <p><em>Training Interface - Configure and train your chatbot</em></p>
</div>

## 🚀 Quick Start

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

4. Start the application:
   ```bash
   python src/chatbot/api/app.py
   ```

## 💻 Development

```bash
# Run tests
pytest tests/

# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint code
flake8 src/ tests/
```

## 📘 Documentation

Each component in the project structure serves a specific purpose:

- `api/` - RESTful endpoints for chatbot interaction and data handling
- `config/` - Environment variables and configuration management
- `data/` - Data processing pipelines and transformations
- `models/` - Machine learning models and training utilities

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## ⭐️ Show your support

Give a ⭐️ if this project helped you!
