"""
Generator for the RAG system.
Handles answer generation using language models.
"""

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from typing import List, Dict, Any, Optional
import google.generativeai as genai


class Generator:
    """Generate answers using a language model."""
    
    def __init__(self, model_name: str = "google/flan-t5-base", api_key: Optional[str] = None):
        """
        Initialize the generator.
        
        Args:
            model_name: Name of the Hugging Face model to use
            api_key: Google API key for Gemini (optional)
        """
        self.model_name = model_name
        self.api_key = api_key
        self.use_gemini = False
        
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.gemini_model = genai.GenerativeModel('gemini-2.0-flash')
                self.use_gemini = True
                print("Successfully initialized Google Gemini model.")
            except Exception as e:
                print(f"Failed to initialize Gemini: {e}. Falling back to local model.")
                self.use_gemini = False
        
        if not self.use_gemini:
            print(f"Loading local model: {model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    
    def generate_answer(self, context: str, query: str, max_new_tokens: int = 256) -> str:
        """
        Generate an answer based on context and query.
        
        Args:
            context: Retrieved context passages
            query: User query
            max_new_tokens: Maximum number of new tokens to generate
            
        Returns:
            Generated answer
        """
        # Create prompt
        prompt = self._create_prompt(context, query)
        
        if self.use_gemini:
            try:
                response = self.gemini_model.generate_content(prompt)
                return response.text
            except Exception as e:
                print(f"Error generating with Gemini: {e}")
                return "I encountered an error while generating the answer."
        
        # Tokenize
        inputs = self.tokenizer(
            prompt, 
            return_tensors="pt", 
            truncation=True, 
            max_length=1024
        )
        
        # Generate
        outputs = self.model.generate(
            inputs.input_ids, 
            max_new_tokens=max_new_tokens,
            num_beams=2,
            early_stopping=True
        )
        
        # Decode
        answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return answer
    
    def _create_prompt(self, context: str, query: str) -> str:
        """
        Create a prompt for the language model.
        
        Args:
            context: Retrieved context passages
            query: User query
            
        Returns:
            Formatted prompt
        """
        if self.use_gemini:
            prompt = f"""You are a helpful and knowledgeable assistant. 
You have two sources of information:
1. The provided context below.
2. Your own general knowledge.

Instructions:
- If the context contains the answer, use it and start your response with [USED_CONTEXT].
- If the context is irrelevant or does not contain the answer, use your own knowledge to answer comprehensively and start your response with [GENERAL_KNOWLEDGE].
- Do NOT say "The provided documents do not contain..." or "Based on the context...". Just answer the question directly.
- If you cannot answer from either source, say "I don't know."

Context:
{context}

Question: {query}

Answer:"""
        else:
            prompt = f"""Use only the following context to answer the question. If you cannot answer the question based on the context, say "I don't have enough information to answer that question."

Context:
{context}

Question: {query}

Answer:"""
        return prompt