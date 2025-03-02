from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Load OpenAI API Key securely from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message", "")
    language = data.get("language", "en")
    age_group = data.get("age", "adult")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Define how Kafka should respond based on age
    complexity_levels = {
        "child": "Respond in a simple and clear way suitable for a child, avoiding complex philosophical concepts.",
        "teen": "Respond in a thoughtful but accessible way suitable for a teenager, introducing some existential ideas.",
        "adult": "Respond in a deep, introspective, and philosophical way, embracing Kafka’s signature style of absurdity, alienation, and bureaucracy."
    }

    # Construct the Kafka-like prompt
    prompt = f"""
    You are Franz Kafka. You are speaking to a visitor in {language}. 
    Adjust your tone based on their age: {complexity_levels[age_group]}.
    
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
            messages=[{"role": "system", "content": prompt}],
            max_tokens=150
        )
        reply = response["choices"][0]["message"]["content"].strip()
        return jsonify({"response": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
