import os

import torch
from transformers import CLIPProcessor, CLIPModel
from PIL import Image

from photoviewer.settings import MEDIA_ROOT


class ClipTagger:
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    
    def __init__(self, image_path, labels, dynamic_threshold: float = 0.5):
        self.image_path = os.path.join(MEDIA_ROOT, image_path)
        self.image = Image.open(self.image_path).convert("RGB")
        self.labels = labels
        self.threshold = dynamic_threshold
        
    def _top_k_labels(self, cosine_similarities, k=5):
        # Get the top k labels corresponding to the highest cosine similarities
        top_k_values, top_k_indices = torch.topk(cosine_similarities, k=k)
        
        # Select Labels Above Threshold
        multi_labels = [self.labels[i] for i in top_k_indices]
        return multi_labels
    
    def _dynamic_thresholding(self, cosine_similarities):
        max_sim = cosine_similarities.max().item()  # Get the highest score
        min_sim = cosine_similarities.min().item()  # Get the lowest score
        threshold = min_sim + self.threshold * (max_sim - min_sim)  # Dynamic threshold (adjustable)
        
        # Select Labels Above Threshold
        multi_labels = [self.labels[i] for i in range(len(self.labels)) if cosine_similarities[i] > threshold]
        return multi_labels
        
    def get_image_tags(self):
        # Define Labels (Multiple Object Categories)
        inputs = self.processor(text=self.labels, images=self.image, return_tensors="pt", padding=True)
        # Pass through model
        outputs = self.model(**inputs)
        cosine_similarities = outputs.logits_per_image.squeeze(0)
        multi_labels = self._top_k_labels(cosine_similarities)
        
        return multi_labels