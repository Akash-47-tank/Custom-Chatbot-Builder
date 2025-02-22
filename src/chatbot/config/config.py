"""Configuration settings for the chatbot builder."""

import os
from pathlib import Path
from typing import Dict, Optional

import torch
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
ROOT_DIR = Path(__file__).parent.parent.parent.parent
SRC_DIR = ROOT_DIR / "src"
DATA_DIR = ROOT_DIR / "data"
LOGS_DIR = ROOT_DIR / "logs"
MODELS_DIR = ROOT_DIR / "models"

# Create directories if they don't exist
for directory in [DATA_DIR, LOGS_DIR, MODELS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Device configuration
DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"

# Model configuration
MODEL_CONFIG = {
    "base_model": "distilgpt2",  # Using a smaller model
    "device": "mps" if torch.backends.mps.is_available() else "cpu"
}

# Training configuration
TRAINING_CONFIG = {
    "num_epochs": 1,  # Reduced to 1 epoch
    "batch_size": 2,  # Smaller batch size
    "learning_rate": 1e-4,
    "warmup_steps": 10,
    "max_grad_norm": 1.0,
    "max_length": 128,  # Reduced sequence length
    "gradient_accumulation_steps": 4  # Add gradient accumulation to save memory
}

# Generation configuration
GENERATION_CONFIG = {
    "max_length": 128,  # Reduced max length for generation
    "num_beams": 2,  # Reduced beam search
    "temperature": 0.7,
    "top_k": 50,
    "top_p": 0.9,
    "no_repeat_ngram_size": 2
}

# Logging configuration
LOGGING_CONFIG = {
    "log_file": LOGS_DIR / "chatbot.log",
    "level": "INFO",
    "rotation": "1 day",
    "retention": "1 week",
}

# Sample industries and their default FAQs
SAMPLE_INDUSTRIES: Dict[str, Dict[str, str]] = {
    "retail": {
        "What are your store hours?": "Our store is open Monday through Saturday from 9 AM to 6 PM.",
        "Do you offer returns?": "Yes, we offer returns within 30 days of purchase with original receipt.",
    },
    "restaurant": {
        "Do you take reservations?": "Yes, we accept reservations through our website or by phone.",
        "Are you open for lunch?": "Yes, we serve lunch from 11 AM to 3 PM daily.",
    },
    "fitness": {
        "What are your membership options?": "We offer monthly and annual memberships with various packages.",
        "Do you offer personal training?": "Yes, we have certified personal trainers available for one-on-one sessions.",
    },
}
