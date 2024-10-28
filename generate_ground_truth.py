import json
import openai
import os

# Set your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Load generated questions
with open('data/generated_questions.json', 'r') as f:
    generated_questions = json.load(f)

ground_truth_entries = []

for idx, question_data in enumerate(generated_questions):
    # Extract the question text
    question = question_data["question"]

    # Optionally rephrase the question using OpenAI API
    def rephrase_question(question):
        prompt = f"""
Rephrase the following question for clarity:

'{question}'
"""
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{"role": "user", "content": prompt}],
            max_tokens=60,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip().strip('"').strip("'")

    rephrased_query = rephrase_question(question)

    # Generate the ground truth answer using OpenAI API
    def generate_ground_truth_answer(question_data):
        # Prepare the prompt
        prompt = f"""
Based on the following question and correct option(s), provide a complete and concise answer:

Question:
{question_data['question']}

Correct Option(s):
{chr(10).join(question_data['correct_options'])}

Include any additional relevant information from the 'comments' section if available.

Answer:
"""
        # If comments are available, include them
        comments = question_data.get('comments', '').strip()
        if comments:
            prompt += f"\nComments:\n{comments}"

        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()

    ground_truth_answer = generate_ground_truth_answer(question_data)

    # Create the ground truth entry
    ground_truth_entry = {
        "query": rephrased_query,
        "relevant_doc_id": idx,
        "ground_truth_question": question,
        "ground_truth_answer": ground_truth_answer
    }

    ground_truth_entries.append(ground_truth_entry)

# Save the ground truth data
with open('data/ground_truth.json', 'w') as f:
    json.dump(ground_truth_entries, f, indent=4)
