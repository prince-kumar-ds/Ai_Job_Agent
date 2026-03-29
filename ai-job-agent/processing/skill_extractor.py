# processing/skill_extractor.py

from sentence_transformers import SentenceTransformer, util
import torch

# -------------------------------
# 1. Load Model (only once)
# -------------------------------
model = SentenceTransformer('all-MiniLM-L6-v2')


# -------------------------------
# 2. Skill Dictionary
# -------------------------------
domain_keywords = {

    "Core AI/ML": [
        "machine learning", "deep learning", "artificial intelligence",
        "neural networks", "supervised learning", "unsupervised learning"
    ],

    "Data Science": [
        "data analysis", "data visualization", "exploratory data analysis",
        "eda", "feature engineering", "data cleaning"
    ],

    "NLP": [
        "natural language processing", "nlp",
        "text preprocessing", "tokenization", "tf-idf", "word embeddings"
    ],

    "Libraries": [
        "numpy", "pandas", "matplotlib", "seaborn",
        "scikit-learn", "tensorflow", "keras", "pytorch",
        "nltk", "spacy", "xgboost"
    ],

    "Programming": [
        "python", "java", "sql", "c++"
    ],

    "Tools & Deployment": [
        "streamlit", "flask", "fastapi", "docker", "aws", "git"
    ]
}


# -------------------------------
# 3. Flatten keywords
# -------------------------------
def load_keywords():
    keywords = []
    for category in domain_keywords.values():
        keywords.extend(category)

    # Remove duplicates
    keywords = list(set(keywords))

    return keywords


# -------------------------------
# 4. Create keyword embeddings
# -------------------------------
def create_keyword_embeddings(keywords):
    return model.encode(
        keywords,
        convert_to_tensor=True,
        normalize_embeddings=True
    )


# -------------------------------
# 5. Extract keywords with scores
# -------------------------------
def extract_keywords_with_scores(content, keywords, keyword_embeddings, threshold=0.35):
    """
    Extract relevant skills from text using semantic similarity
    """

    # Encode content
    content_embedding = model.encode(
        [content],
        convert_to_tensor=True,
        normalize_embeddings=True
    )

    # Compute similarity
    similarities = util.cos_sim(content_embedding, keyword_embeddings)[0]

    # Collect results
    results = [
        (keywords[i], float(similarities[i]))
        for i in range(len(keywords))
        if similarities[i] >= threshold or keywords[i] in content.lower()
    ]

    # Sort by score
    results = sorted(results, key=lambda x: x[1], reverse=True)

    return results


# -------------------------------
# 6. Wrapper function (EASY USE)
# -------------------------------
def extract_skills(content):
    keywords = load_keywords()
    keyword_embeddings = create_keyword_embeddings(keywords)

    return extract_keywords_with_scores(content, keywords, keyword_embeddings)