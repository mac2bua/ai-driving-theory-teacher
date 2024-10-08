import openai
import json
import os

# Set your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')  # It's safer to use environment variables

# List of themes and chapters
themes_and_chapters = [
    {
        "theme": "Qualification and ability of truck drivers",
        "chapter": "Qualification and ability of truck drivers"
    },
    # Add more themes and chapters as needed
    {
        "theme": "Traffic Signs",
        "chapter": "Understanding German Traffic Signs"
    },
    {
        "theme": "Road Rules",
        "chapter": "General Road Rules and Regulations"
    },
    {
        "theme": "Vehicle Maintenance",
        "chapter": "Basic Vehicle Maintenance"
    },
    {
        "theme": "Environmental Awareness",
        "chapter": "Eco-Friendly Driving Practices"
    },
    {
        "theme": "First Aid",
        "chapter": "Emergency Situations and First Aid"
    }
]

def generate_questions(theme, chapter, num_questions=5):
    questions = []
    for _ in range(num_questions):
        prompt = f"""
As an AI assistant, generate a driving theory question for the German driving license exam in the following JSON format:

{{
    "theme": "{theme}",
    "chapter": "{chapter}",
    "question": "Your generated question here.",
    "options": [
        "A. Option A",
        "B. Option B",
        "C. Option C"
    ],
    "correct_options": [
        "Your correct option(s) here."
    ],
    "comments": "Your explanation about the correct option(s) come here."
}}

Requirements:
- The question should be relevant to the theme and chapter.
- Provide three options labeled A, B, and C.
- At least one correct option; there can be multiple correct options.
- "comments" can remain empty.
- Output only valid JSON without any additional text.

Now, generate one such question.
"""
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',  # Use 'gpt-4' if you have access
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        output = response['choices'][0]['message']['content'].strip()
        try:
            question_data = json.loads(output)
            questions.append(question_data)
        except json.JSONDecodeError:
            print("Failed to parse JSON. Response was:")
            print(output)
    return questions

def main():
    all_questions = []
    for item in themes_and_chapters:
        theme = item['theme']
        chapter = item['chapter']
        print(f"Generating questions for Theme: {theme}, Chapter: {chapter}")
        questions = generate_questions(theme, chapter, num_questions=5)
        all_questions.extend(questions)
    
    # Save the collected questions
    os.makedirs('data', exist_ok=True)
    with open('data/generated_questions.json', 'w', encoding='utf-8') as f:
        json.dump(all_questions, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
