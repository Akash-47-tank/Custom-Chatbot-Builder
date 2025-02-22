"""Model training and inference utilities for the chatbot builder."""

from pathlib import Path
from typing import Optional, Tuple

import torch
from datasets import Dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
)

from chatbot.config.config import MODEL_CONFIG, MODELS_DIR, TRAINING_CONFIG
from chatbot.utils.logger import get_logger

logger = get_logger()


class ChatbotTrainer:
    """Train and manage the chatbot model."""

    def __init__(self):
        """Initialize the chatbot trainer."""
        try:
            self.device = MODEL_CONFIG["device"]
            self.model_name = MODEL_CONFIG["base_model"]
            
            # Initialize tokenizer and model
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
            
            # Add special tokens and set padding token
            special_tokens = {
                "sep_token": "###",
                "pad_token": "[PAD]",
            }
            self.tokenizer.add_special_tokens(special_tokens)
            
            # Set pad_token to eos_token if it doesn't exist
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                
            # Resize model embeddings to account for new tokens
            self.model.resize_token_embeddings(len(self.tokenizer))
            
            # Move model to appropriate device (MPS for M1 Mac)
            self.model.to(self.device)
            
            logger.info(f"Initialized model {self.model_name} on device {self.device}")
        except Exception as e:
            logger.error(f"Error initializing ChatbotTrainer: {str(e)}")
            raise

    def train(
        self,
        dataset: Dataset,
        output_dir: Optional[Path] = None
    ) -> Tuple[float, Path]:
        """
        Fine-tune the model on the provided dataset.

        Args:
            dataset (Dataset): Prepared and tokenized dataset
            output_dir (Optional[Path]): Directory to save the model

        Returns:
            Tuple[float, Path]: Training loss and path to saved model
        """
        try:
            if output_dir is None:
                output_dir = MODELS_DIR / "fine_tuned"

            training_args = TrainingArguments(
                output_dir=str(output_dir),
                num_train_epochs=TRAINING_CONFIG["num_epochs"],
                per_device_train_batch_size=TRAINING_CONFIG["batch_size"],
                learning_rate=TRAINING_CONFIG["learning_rate"],
                warmup_steps=TRAINING_CONFIG["warmup_steps"],
                max_grad_norm=TRAINING_CONFIG["max_grad_norm"],
                gradient_accumulation_steps=TRAINING_CONFIG["gradient_accumulation_steps"],
                logging_dir=str(output_dir / "logs"),
                save_strategy="no",  
                remove_unused_columns=True,
                logging_steps=1,
                use_mps_device=self.device == "mps",
                fp16=False,  
                optim="adamw_torch",  
                max_steps=50,  
            )

            trainer = Trainer(
                model=self.model,
                args=training_args,
                train_dataset=dataset,
                data_collator=lambda data: {
                    'input_ids': torch.stack([torch.tensor(x['input_ids']) for x in data]),
                    'attention_mask': torch.stack([torch.tensor(x['attention_mask']) for x in data]),
                    'labels': torch.stack([torch.tensor(x['labels']) for x in data])
                }
            )

            # Clear GPU memory before training
            if self.device == "mps":
                torch.mps.empty_cache()

            # Train the model
            logger.info("Starting model training...")
            train_result = trainer.train()
            
            # Save the model
            trainer.save_model()
            logger.info(f"Model saved to {output_dir}")

            return train_result.training_loss, output_dir
        except Exception as e:
            logger.error(f"Error during training: {str(e)}")
            raise

    def generate_response(self, question: str) -> str:
        """
        Generate a response for the given question.

        Args:
            question (str): Input question

        Returns:
            str: Generated response
        """
        try:
            # Prepare input
            input_text = f"{question} ###"
            input_ids = self.tokenizer.encode(input_text, return_tensors="pt").to(self.device)

            # Generate response
            with torch.no_grad():
                output_ids = self.model.generate(
                    input_ids,
                    max_length=MODEL_CONFIG["max_length"],
                    temperature=MODEL_CONFIG["temperature"],
                    top_p=MODEL_CONFIG["top_p"],
                    pad_token_id=self.tokenizer.eos_token_id,
                )

            # Decode and clean response
            response = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
            response = response.split("###")[-1].strip()

            logger.debug(f"Generated response for question: {question}")
            return response
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise

    def load_model(self, model_path: Path) -> None:
        """
        Load a fine-tuned model from disk.

        Args:
            model_path (Path): Path to the saved model

        Returns:
            None
        """
        try:
            self.model = AutoModelForCausalLM.from_pretrained(str(model_path))
            self.model.to(self.device)
            logger.info(f"Loaded model from {model_path}")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
