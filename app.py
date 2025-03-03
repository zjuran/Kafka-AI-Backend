from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv

# Initialize Flask app
app = Flask(__name__)

# Load environment variables
load_dotenv()

# OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Define the '/chat' route
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message", "")
    language = data.get("language", "en")
    age_group = data.get("age", "adult")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Kafka's response style based on age group
    complexity_levels = {
        "child": "Respond in a simple and clear way suitable for a child.",
        "teen": "Respond in a thoughtful but accessible way suitable for a teenager.",
        "adult": "Respond in a deep, introspective, and philosophical way, true to Kafka’s style."
    }

    prompt = f"""
    You are Franz Kafka. Respond in {language}.
    Adjust your tone based on age: {complexity_levels[age_group]}.

    Your responses should:
    - Reflect Kafka's themes of alienation, bureaucracy, existential dread, and absurdity.
    - Be poetic, mysterious, and slightly unsettling.
    - Reference Kafka’s own works (e.g., The Trial, The Metamorphosis) when relevant.
    - If appropriate, make the visitor feel as if they are trapped in a surreal, bureaucratic nightmare.

    Question: "{user_message}"

    Kafka:
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": prompt},
                      {"role": "user", "content": user_message}],
            max_tokens=150
        )
        reply = response['choices'][0]['message']['content'].strip()
        return jsonify({"response": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return jsonify({"message": "Kafka AI Backend is running!"})

if __name__ == '__main__':
    app.run(debug=True)
