# AI Driving Instructor: Your Companion for the German Driving Theory Exam

## Problem Statement

Preparing for the German driving theory exam can be a challenging endeavor. Aspiring drivers must familiarize themselves with an extensive array of traffic rules, road signs, and safety regulations specific to Germany. Traditional study methods like textbooks and passive learning often fail to provide the interactive and personalized experience needed to effectively grasp these concepts.

**AI Driving Instructor** is an interactive learning tool designed to help individuals prepare for the German driving theory exam efficiently and effectively. The application presents users with AI-generated exam questions, allowing them to select their answers in a quiz format. After each attempt, the AI Driving Instructor evaluates the responses, providing immediate feedback and detailed explanations for any mistakes made. This personalized guidance helps users understand the reasoning behind correct answers, reinforces learning, and addresses knowledge gaps.

By leveraging artificial intelligence and large language models (LLMs), the AI Driving Instructor offers a tailored educational experience that adapts to the user's learning pace and needs. The goal is to enhance comprehension, boost confidence, and ultimately increase the chances of passing the German driving theory exam.


## Data Generation

### Why Synthetic Data?

To avoid copyright issues with proprietary driving theory questions, we generate a synthetic dataset using OpenAI's GPT-3.5 language model.

### Prerequisites

- Python 3.7 or higher
- OpenAI Python library
- OpenAI API key

### Steps to Generate Data

1. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up OpenAI API Key**

- Obtain an API key from OpenAI.
- Set the API key as an environment variable:
    - On macOS/Linux:
    ```bash
    export OPENAI_API_KEY='your-api-key-here'
    ```
    - On Windows:
    ```cmd
    set OPENAI_API_KEY=your-api-key-here
    ```

3. **Run the Data Generation Script**

    ```bash
    python generate_data.py
    ```

This will generate `data/generated_questions.json`.
