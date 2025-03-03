@app.route('/chat', methods=['POST'])
def chat():
    print("POST request to /chat received!")  # Log that the route was accessed

    data = request.json
    if not data:
        print("No data received in the body!")  # Log if data is not coming through
        return jsonify({"error": "No message provided"}), 400
    
    user_message = data.get("message", "")
    language = data.get("language", "en")
    age_group = data.get("age", "adult")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Kafka response logic remains here...
    return jsonify({"response": "Kafka's reply here!"})  # Temporary mock for testing
