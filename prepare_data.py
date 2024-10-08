from sentence_transformers import SentenceTransformer
import faiss
import pandas as pd
import numpy as np
import json

def main():
    # Load your generated questions
    with open('data/generated_questions.json', 'r') as f:
        questions = json.load(f)

    # Initialize the embedding model
    model_name = "multi-qa-distilbert-cos-v1"
    embedding_model = SentenceTransformer(model_name)

    # Encode the questions
    embeddings = []
    for q in questions:
        q_text = f"{q['theme']} {q['chapter']} {q['question']}"
        embedding = embedding_model.encode(q_text)
        embeddings.append(embedding)
    embeddings = np.array(embeddings)

    # Define the dimension
    dimension = embeddings.shape[1]

    # Create FAISS index
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    # Save the index
    faiss.write_index(index, 'data/questions_index.faiss')

    # Save the mapping of index to questions
    with open('data/index_to_question.json', 'w') as f:
        json.dump(questions, f)

if __name__ == "__main__":
    main()