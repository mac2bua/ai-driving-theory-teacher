import streamlit as st
import json
import random
import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
import os
import openai


# Display the header image
st.image('./images/header_image.webp', use_column_width=True)  # Update the path to your image


# Load questions
@st.cache_data
def load_questions():
    with open('./data/index_to_question.json', 'r') as f:
        return json.load(f)

questions = load_questions()

# Load FAISS index
@st.cache_resource
def load_index():
    return faiss.read_index('data/questions_index.faiss')

index = load_index()

# Load embedding model
@st.cache_resource
def load_embedding_model():
    return SentenceTransformer("multi-qa-distilbert-cos-v1")

embedding_model = load_embedding_model()

# Set OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Define search and generate functions
def search_question(query, index, questions, embedding_model, k=5):
    # Encode the query
    query_embedding = embedding_model.encode([query])

    # Search the index
    distances, indices = index.search(query_embedding, k)

    # Retrieve the top k questions
    retrieved_questions = [questions[idx] for idx in indices[0]]
    return retrieved_questions, indices[0]

def generate_answer(query, retrieved_docs):
    context = "\n".join([f"Q: {doc['question']}\nA: {doc['correct_options']}" for doc in retrieved_docs])
    prompt = f"""
    You are an AI assistant helping users prepare for the German driving theory exam.

    Context:
    {context}

    Question:
    {query}

    Answer the question using the context above, don't include the letter at the beginning of each correct option. If the answer is not in the context, say "I'm sorry, I don't have enough information to answer that question."
    """

    response = openai.ChatCompletion.create(
        model='gpt-4o-mini',
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
        temperature=0,
    )
    return response.choices[0].message.content.strip()

# Sidebar for mode selection
mode = st.sidebar.selectbox("Select Mode", ["Practice Mode", "Ask a Question"])

if mode == "Practice Mode":
    # Initialize session state variables if not already present
    if 'selected_theme' not in st.session_state:
        st.session_state['selected_theme'] = None
    if 'current_question' not in st.session_state:
        st.session_state['current_question'] = None
    if 'options_selected' not in st.session_state:
        st.session_state['options_selected'] = []

    # Sidebar for theme selection
    theme_list = list(set([q['theme'] for q in questions]))
    selected_theme = st.sidebar.selectbox('Select a Theme:', theme_list, key='theme_select')
    if selected_theme != st.session_state.selected_theme:
        st.session_state.selected_theme = selected_theme
        st.session_state.current_question = None  # Reset question when theme changes

    # Filter questions by selected theme
    theme_questions = [q for q in questions if q['theme'] == st.session_state.selected_theme]

    # Button to get a random question
    if st.button('Get Random Question'):
        st.session_state.current_question = random.choice(theme_questions)
        st.session_state.options_selected = [False] * len(st.session_state.current_question['options'])

    # Display the current question
    if st.session_state.current_question:
        st.write('**Question:**', st.session_state.current_question['question'])
        all_options = st.session_state.current_question['options']
        
        # Create checkboxes for options
        for i, option in enumerate(all_options):
            if option.strip():
                st.session_state.options_selected[i] = st.checkbox(option.strip(), key=f'option_{i}', value=st.session_state.options_selected[i])

        # Button to submit answers
        if st.button('Submit Answers'):
            correct_answers = st.session_state.current_question['correct_options']
            correct_answers = [option.strip() for option in correct_answers]
            correct_indices = [i for i, option in enumerate(all_options) if option.strip() in correct_answers]
            user_answers = [i for i, option in enumerate(all_options) if st.session_state.options_selected[i]]
            
            if set(user_answers) == set(correct_indices):
                st.success("Correct! Well done.")
            else:
                st.error("Incorrect. Try again!")
            st.write("**Correct Answers:**")
            for idx in correct_indices:
                st.write(all_options[idx])

            # Display comments if any
            if st.session_state.current_question.get('comments'):
                st.write("**Explanation:**")
                st.write(st.session_state.current_question['comments'])

elif mode == "Ask a Question":
    st.title("AI Driving Instructor")

    user_query = st.text_input("Enter your question about the German driving theory exam:")
    if user_query:
        with st.spinner("Generating answer..."):
            retrieved_docs, indices = search_question(user_query, index, questions, embedding_model, k=5)
            answer = generate_answer(user_query, retrieved_docs)
            st.write("**Answer:**")
            st.write(answer)

            # Optionally display retrieved questions
            if st.checkbox("Show retrieved context"):
                for doc in retrieved_docs:
                    st.write(f"**Question:** {doc['question']}")
                    st.write(f"**Answer:** {doc['correct_options']}")
                    if doc.get('comments'):
                        st.write(f"**Explanation:** {doc['comments']}")
                    st.write("---")
        
        feedback = st.radio("Was this answer helpful?", ("Yes", "No"))
        if feedback == "No":
            feedback_text = st.text_input("Please tell us how we can improve:")
        if st.button("Submit Feedback"):
            feedback_data = {
                "query": user_query,
                "answer": answer,
                "feedback": feedback,
                "comments": feedback_text if feedback == "No" else ""
            }
            # Save feedback to a JSON file
            with open('data/user_feedback.json', 'a') as f:
                f.write(json.dumps(feedback_data) + "\n")
            st.success("Thank you for your feedback!")

# Refresh the page without changing states
st.sidebar.button("Refresh")
