
import spacy
from spacy.matcher import PhraseMatcher
from transformers import pipeline
import re
import json
import os

# Load the existing data from the JSON file
'''REPLACE THE FILENAME WITH THE FILE YOU WANT TO FILTER'''
filename = f'filteredOverallRecords.json'  # Replace with your actual file name


# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# AI-related keywords list
ai_related_terms = [
    # Core AI Concepts
    "AI", "artificial intelligence", "machine learning", "deep learning", "neural network",
    
    # Subfields
    "natural language processing", "NLP", "computer vision", "reinforcement learning",
    "generative AI", "supervised learning", "unsupervised learning", "semi-supervised learning",
    "transfer learning", "explainable AI", "AI ethics", "AI safety", "AI alignment",
    
    # Applications
    "chatbot", "predictive modeling", "automation", "AI-powered", "AI-driven", "AI-based",
    "AI-enabled", "AI system", "AI model", "AI algorithm", "AI application", "AI platform",
    "AI solution", "AI tool", "AI framework", "AI technology",
    
    # Emerging Trends
    "large language model", "LLM", "transformer model", "GPT", "BERT", "generative adversarial network",
    "GAN", "diffusion model", "AI chip", "AI accelerator",
    
    # Industry-Specific (General)
    "autonomous vehicle", "self-driving car", "AI tutor", "AI recommendation", "AI analytics",
    "AI forecasting", "AI imaging", "AI automation", "AI personalization", "AI customer service",
    
    # Tools and Frameworks
    "TensorFlow", "PyTorch", "Keras", "Scikit-learn", "OpenCV", "Hugging Face", "LangChain",
    
    # Generic Terms
    "AI community", "AI research", "AI development", "AI project", "AI startup", "AI innovation"
]

# Initialize PhraseMatcher
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")  # Case-insensitive matching
# Create patterns for the PhraseMatcher
patterns = [nlp.make_doc(term) for term in ai_related_terms]
matcher.add("AI_Terms", patterns)

# Load multi-label classification model
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Define industry categories
industry_labels = [
    "Technology & IT",                    # Software, IT services, cybersecurity, telecommunications, and research
    "Finance & Banking",                  # Financial services, banking, fintech, insurance, and investment management
    "Healthcare & Pharmaceuticals",       # Medical services, healthcare technologies, pharmaceuticals, biotech, and wellness
    "Energy & Utilities",                 # Renewable and traditional energy, utilities, sustainability, and environmental services
    "Retail & E-Commerce",                # Retail, online marketplaces, consumer goods, and supply chain management
    "Entertainment & Media",              # Gaming, music, film, television, streaming, and digital media
    "Manufacturing & Engineering",        # Production, manufacturing, mechanical, electrical, civil, industrial engineering, and construction
    "Transportation & Logistics",         # Transportation, shipping, supply chain management, and logistics
    "Education & Training",               # Education, e-learning, professional development, and training services
    "Legal & Compliance",                 # Legal services, corporate law, regulatory affairs, compliance, and intellectual property
    "Real Estate & Property",             # Property sales, leasing, management, and development
    "Marketing & Advertising",            # Marketing, advertising, branding, public relations, and digital marketing
    "Human Resources & Talent Management",# HR services, recruitment, talent acquisition, and employee relations
    "Agriculture & Environmental",        # Farming, agriculture, forestry, sustainability, and environmental conservation
    "Consumer Goods & Services",          # Consumer products, lifestyle services, retail, and hospitality
    "Sports, Fitness & Recreation",       # Sports, fitness, recreation, wellness, and active lifestyle
    "Non-Profit & Social Services",       # Charities, NGOs, community services, and social impact
    "Aerospace & Defense",                # Aviation, aerospace engineering, defense technologies, and military services
]


# Function to detect AI-related terms
def detect_ai_terms(text):
    """Detect AI-related terms in text using rule-based matching."""
    doc = nlp(text)
    matches = matcher(doc)
    ai_terms = [doc[start:end].text for match_id, start, end in matches]
    return ai_terms

# Function to mask AI-related terms
def mask_ai_terms(text):
    """Replace AI-related terms with a stronger placeholder to reduce bias."""
    pattern = re.compile(r'\b(' + '|'.join(re.escape(term) for term in ai_related_terms) + r')\b', flags=re.IGNORECASE)
    return pattern.sub("[MASK]", text)  # Replacing with '[MASK]'

# Function for industry classification
def classify_industry(text):
    """Classify text into multiple industries using zero-shot classification."""
    result = classifier(text, industry_labels, multi_label=True, hypothesis_template="This text discusses {} in relation to AI and its applications across different domains.")
    
    # Combine labels and scores into a list of tuples
    label_score_pairs = list(zip(result["labels"], result["scores"]))
    
    # Sort the list by scores in descending order
    sorted_pairs = sorted(label_score_pairs, key=lambda x: x[1], reverse=True)
    
    # Extract up to 5 labels (or fewer if there aren't enough)
    return [label for label, score in sorted_pairs[:min(5, len(sorted_pairs))]]

# Combined process: Detect, Mask, and Classify
def process_text(text):
    """Determine the industry classification of a given text with AI masking."""
    
    # Step 1: Detect AI-related terms
    ai_terms = detect_ai_terms(text)
    
    if ai_terms:
        # Step 2: Create a masked version of the text
        masked_text = mask_ai_terms(text)
        
        # Step 3: Run classification on both original and masked text
        original_categories = classify_industry(text)
        masked_categories = classify_industry(masked_text)

        # Step 4: If masked version removes AI bias, replace original result
        if "Technology & IT" in original_categories and "Technology & IT" not in masked_categories:
            return masked_categories if masked_categories else ["General"]

        return original_categories  if original_categories else ["General"] # Keep original if still valid
    
    # If no AI-related terms are found, use standard classification
    return classify_industry(text)


with open(filename, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Assuming the data is a list of posts, and each post is a dictionary (like the `post_data` structure)
for index, post in enumerate(data): 
    print(index)
    # Add the subreddit attribute to each post (you can adjust as needed based on your structure)
    post["category"] = process_text(post["text"])

# Save the updated data back to the JSON file
with open(filename, 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4)
print('Done')