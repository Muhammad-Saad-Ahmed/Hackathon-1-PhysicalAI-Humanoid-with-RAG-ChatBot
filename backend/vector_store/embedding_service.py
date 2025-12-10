from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np


class EmbeddingService:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize the embedding service with a pre-trained model.

        Args:
            model_name: Name of the sentence transformer model to use
        """
        self.model = SentenceTransformer(model_name)

    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.

        Args:
            text: Input text to embed

        Returns:
            List of float representing the embedding vector
        """
        embedding = self.model.encode([text])
        return embedding[0].tolist()

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.

        Args:
            texts: List of input texts to embed

        Returns:
            List of embedding vectors (each vector is a list of floats)
        """
        embeddings = self.model.encode(texts)
        return [embedding.tolist() for embedding in embeddings]

    def similarity(self, text1: str, text2: str) -> float:
        """
        Calculate cosine similarity between two texts.

        Args:
            text1: First text
            text2: Second text

        Returns:
            Cosine similarity score between 0 and 1
        """
        embedding1 = np.array(self.embed_text(text1))
        embedding2 = np.array(self.embed_text(text2))

        # Calculate cosine similarity
        dot_product = np.dot(embedding1, embedding2)
        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return float(dot_product / (norm1 * norm2))