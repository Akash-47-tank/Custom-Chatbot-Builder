"""Data processing utilities for the chatbot builder."""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pandas as pd
from datasets import Dataset
from transformers import PreTrainedTokenizer

from chatbot.config.config import DATA_DIR, SAMPLE_INDUSTRIES
from chatbot.utils.logger import get_logger

logger = get_logger()


class DataProcessor:
    """Process and prepare data for chatbot training."""

    def __init__(self, tokenizer: PreTrainedTokenizer):
        """
        Initialize the data processor.

        Args:
            tokenizer (PreTrainedTokenizer): Tokenizer for processing text
        """
        self.tokenizer = tokenizer
        self.sep_token = "###"
        logger.info("DataProcessor initialized")

    def parse_faq_input(self, raw_text: str) -> List[Tuple[str, str]]:
        """
        Parse raw FAQ input text into question-answer pairs.

        Args:
            raw_text (str): Raw FAQ text input

        Returns:
            List[Tuple[str, str]]: List of (question, answer) tuples
        """
        try:
            qa_pairs = []
            lines = raw_text.strip().split("\n")
            
            for line in lines:
                if "Q:" in line and "A:" in line:
                    q_part = line.split("A:")[0].replace("Q:", "").strip()
                    a_part = line.split("A:")[1].strip()
                    qa_pairs.append((q_part, a_part))
            
            logger.info(f"Parsed {len(qa_pairs)} FAQ pairs")
            return qa_pairs
        except Exception as e:
            logger.error(f"Error parsing FAQ input: {str(e)}")
            raise

    def prepare_training_data(
        self,
        business_data: Dict[str, str],
        custom_faqs: List[Tuple[str, str]],
        industry: str
    ) -> Dataset:
        """
        Prepare training data by combining business info, custom FAQs, and industry samples.

        Args:
            business_data (Dict[str, str]): Business information
            custom_faqs (List[Tuple[str, str]]): Custom FAQ pairs
            industry (str): Business industry

        Returns:
            Dataset: Prepared dataset for training
        """
        try:
            # Combine custom FAQs with industry samples
            all_qa_pairs = custom_faqs.copy()
            if industry in SAMPLE_INDUSTRIES:
                all_qa_pairs.extend(
                    [(q, a) for q, a in SAMPLE_INDUSTRIES[industry].items()]
                )

            # Create training examples
            examples = []
            for question, answer in all_qa_pairs:
                # Format: question ### answer
                text = f"{question} {self.sep_token} {answer}"
                examples.append({"text": text})

            # Convert to Dataset
            dataset = Dataset.from_pandas(pd.DataFrame(examples))
            logger.info(f"Prepared dataset with {len(examples)} examples")
            return dataset
        except Exception as e:
            logger.error(f"Error preparing training data: {str(e)}")
            raise

    def tokenize_data(self, dataset: Dataset) -> Dataset:
        """
        Tokenize the dataset for model training.

        Args:
            dataset (Dataset): Raw dataset

        Returns:
            Dataset: Tokenized dataset
        """
        try:
            def tokenize_function(examples):
                # Tokenize inputs
                model_inputs = self.tokenizer(
                    examples["text"],
                    padding="max_length",
                    truncation=True,
                    max_length=self.tokenizer.model_max_length,
                    return_tensors=None  # Return as lists instead of tensors
                )
                
                # Create labels (same as inputs for causal language modeling)
                model_inputs["labels"] = model_inputs["input_ids"].copy()
                
                return model_inputs

            tokenized_dataset = dataset.map(
                tokenize_function,
                batched=True,
                remove_columns=dataset.column_names,
                desc="Tokenizing data"
            )
            
            logger.info("Dataset tokenized successfully")
            return tokenized_dataset
        except Exception as e:
            logger.error(f"Error tokenizing data: {str(e)}")
            raise

    def export_chatbot_data(
        self,
        business_data: Dict[str, str],
        qa_pairs: List[Tuple[str, str]],
        output_file: Optional[Path] = None
    ) -> Path:
        """
        Export chatbot data to JSON format for integration.

        Args:
            business_data (Dict[str, str]): Business information
            qa_pairs (List[Tuple[str, str]]): Question-answer pairs
            output_file (Optional[Path]): Output file path

        Returns:
            Path: Path to the exported JSON file
        """
        try:
            export_data = {
                "business_info": business_data,
                "qa_pairs": [
                    {"question": q, "answer": a} for q, a in qa_pairs
                ]
            }

            if output_file is None:
                output_file = DATA_DIR / "chatbot_export.json"

            with open(output_file, "w") as f:
                json.dump(export_data, f, indent=2)

            logger.info(f"Exported chatbot data to {output_file}")
            return output_file
        except Exception as e:
            logger.error(f"Error exporting chatbot data: {str(e)}")
            raise
