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

    # Define Kafka's response complexity
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
            messages=[{"role": "system", "content": prompt}],
            max_tokens=150
        )
        reply = response["choices"][0]["message"]["content"].strip()
        return jsonify({"response": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))  # Get assigned port from Render
    app.run(host='0.0.0.0', port=port)

