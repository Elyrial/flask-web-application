from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Get the JSON data from the request
        req = request.get_json(force=True)
        query = req['queryResult']['queryText']
        intent = req['queryResult']['intent']['displayName']

        # GPT intent
        if intent == 'gpt':
            print(f"User query: {query}")
            query = query + ' in one brief paragraph'

            # Call openai API
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant, answer in one brief paragraph"},
                    {"role": "user", "content": query}
                ],
                max_tokens=100,
                temperature=0.7,
            )

            # Extract the generated text
            generated_text = response.choices[0].message.content.strip()
            print(f"Generated text: {generated_text}")

            # Return the response to the dialogflow 
            return jsonify({
                'fulfillmentText': generated_text
            })

        else:
            return jsonify({
                'fulfillmentText': f"Unhandled intent: {intent}"
            })

    except Exception as e:
        # Log the error and return a meaningful error message
        print(f"Error in webhook: {e}")
        return jsonify({
            'fulfillmentText': f"An error occurred: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
