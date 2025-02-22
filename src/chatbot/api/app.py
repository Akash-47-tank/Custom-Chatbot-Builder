"""Gradio interface for the chatbot builder."""

import json
from pathlib import Path
from typing import Dict, List, Tuple

import gradio as gr
import torch

from chatbot.config.config import DATA_DIR, DEVICE, SAMPLE_INDUSTRIES
from chatbot.data.processor import DataProcessor
from chatbot.models.trainer import ChatbotTrainer
from chatbot.utils.logger import get_logger, setup_logger

# Set up logging
setup_logger()
logger = get_logger()


class ChatbotInterface:
    """Gradio interface for the chatbot builder."""

    def __init__(self):
        """Initialize the chatbot interface."""
        try:
            self.trainer = ChatbotTrainer()
            self.processor = DataProcessor(self.trainer.tokenizer)
            logger.info("ChatbotInterface initialized")
        except Exception as e:
            logger.error(f"Error initializing ChatbotInterface: {str(e)}")
            raise

    def train_chatbot(
        self,
        business_name: str,
        industry: str,
        faq_text: str
    ) -> Tuple[str, str]:
        """
        Train the chatbot with the provided business information and FAQs.

        Args:
            business_name (str): Name of the business
            industry (str): Business industry
            faq_text (str): Raw FAQ text

        Returns:
            Tuple[str, str]: Status message and model path
        """
        try:
            gr.Info("Starting chatbot training...")
            
            # Process FAQs
            logger.info("Processing FAQs...")
            qa_pairs = self.processor.parse_faq_input(faq_text)
            gr.Info("FAQs processed successfully")
            
            # Prepare training data
            logger.info("Preparing training data...")
            business_data = {"name": business_name, "industry": industry}
            dataset = self.processor.prepare_training_data(
                business_data, qa_pairs, industry
            )
            gr.Info("Training data prepared")
            
            # Tokenize data
            logger.info("Tokenizing data...")
            tokenized_dataset = self.processor.tokenize_data(dataset)
            gr.Info("Data tokenized")
            
            # Train model
            logger.info("Training model...")
            loss, model_path = self.trainer.train(tokenized_dataset)
            gr.Info("Model training completed")
            
            # Export data
            logger.info("Exporting chatbot data...")
            export_path = self.processor.export_chatbot_data(
                business_data, qa_pairs
            )
            gr.Info("Chatbot data exported")
            
            return (
                f"Training completed! Loss: {loss:.4f}\nModel saved to: {model_path}\nData exported to: {export_path}",
                str(model_path)
            )
        except Exception as e:
            logger.error(f"Error in train_chatbot: {str(e)}")
            gr.Error(f"Error: {str(e)}")
            return f"Error: {str(e)}", ""

    def chat(
        self,
        question: str,
        model_path: str,
        history: List[Tuple[str, str]]
    ) -> Tuple[str, List[Tuple[str, str]]]:
        """
        Generate a response for the given question.

        Args:
            question (str): User's question
            model_path (str): Path to the trained model
            history (List[Tuple[str, str]]): Chat history

        Returns:
            Tuple[str, List[Tuple[str, str]]]: Bot response and updated history
        """
        try:
            if not model_path:
                return "Please train the chatbot first!", history

            if not question:
                return "Please ask a question!", history

            # Load model if needed
            if not hasattr(self, "loaded_model_path") or self.loaded_model_path != model_path:
                self.trainer.load_model(Path(model_path))
                self.loaded_model_path = model_path

            # Generate response
            response = self.trainer.generate_response(question)
            history.append((question, response))
            
            return response, history
        except Exception as e:
            logger.error(f"Error in chat: {str(e)}")
            return f"Error: {str(e)}", history


def create_interface() -> gr.Blocks:
    """
    Create the Gradio interface.

    Returns:
        gr.Blocks: Gradio interface
    """
    interface = ChatbotInterface()

    with gr.Blocks(title="Custom Chatbot Builder") as demo:
        gr.Markdown("# Custom Chatbot Builder for Small Businesses")
        
        with gr.Tab("Train Chatbot"):
            business_name = gr.Textbox(
                label="Business Name",
                placeholder="Enter your business name"
            )
            industry = gr.Dropdown(
                choices=list(SAMPLE_INDUSTRIES.keys()),
                label="Industry"
            )
            faq_input = gr.Textbox(
                label="FAQs",
                placeholder="Enter your FAQs in Q: A: format\nExample:\nQ: What are your hours? A: We're open 9-5 Monday to Friday",
                lines=10
            )
            train_button = gr.Button("Train Chatbot")
            training_output = gr.Textbox(label="Training Status")
            model_path = gr.Textbox(visible=False)
            
            train_button.click(
                fn=interface.train_chatbot,
                inputs=[
                    business_name,
                    industry,
                    faq_input
                ],
                outputs=[training_output, model_path]
            )

        with gr.Tab("Chat"):
            chatbot = gr.Chatbot(label="Chat History")
            msg = gr.Textbox(
                label="Your Question",
                placeholder="Ask a question..."
            )
            clear = gr.Button("Clear")

            msg.submit(
                fn=interface.chat,
                inputs=[msg, model_path, chatbot],
                outputs=[msg, chatbot]
            )
            clear.click(lambda: None, None, chatbot, queue=False)

    return demo


if __name__ == "__main__":
    # Log the device being used
    logger.info(f"Using device: {DEVICE}")
    
    # Create and launch the interface
    demo = create_interface()
    demo.launch(share=True)
