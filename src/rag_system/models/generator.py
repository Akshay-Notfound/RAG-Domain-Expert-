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
            prompt = f"""You are a knowledgeable and helpful AI assistant with expertise across multiple domains including history, science, technology, languages, and general knowledge.

INSTRUCTIONS:
1. Answer the user's question comprehensively and accurately
2. If the provided context contains relevant information, use it as your primary source
3. If the context is not relevant or insufficient, use your general knowledge to provide a helpful answer
4. NEVER say "I don't know", "I don't have enough information", or "The provided documents do not contain..." - always provide the best answer you can
5. Be conversational, friendly, and helpful in your responses
6. For language-related questions (like "can you speak [language]"), answer positively and demonstrate if requested
7. Provide clear, well-structured answers

Context from documents:
{context}

User Question: {query}

Your Answer:"""
        else:
            prompt = f"""Answer the following question based on the context provided. If the context doesn't contain enough information, use your knowledge to provide a helpful answer.

Context:
{context}

Question: {query}

Answer:"""
        return prompt