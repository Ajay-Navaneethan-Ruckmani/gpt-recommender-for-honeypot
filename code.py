import openai
import json
from flask import Flask, render_template, request

# Initialize Flask app
app = Flask(__name__)

# Function to get GPT-4 recommendation
def get_gpt_recommendation(user_query, api_key):
    # Initialize the OpenAI library with the provided API key
    openai.api_key = api_key

    # Query the GPT-4 model
    response = openai.Completion.create(
        engine="gpt-4.0-turbo",
        prompt=user_query,
        max_tokens=50  # Adjust the limit as needed
    )

    # Extract and clean the GPT-4 response
    gpt_response = response.choices[0].text.strip()

    return gpt_response

# Function to extract data from Cowrie logs
def extract_data_from_logs(log_path):
    ssh_attempts = 0
    telnet_attempts = 0
    successful_logins = 0
    failed_logins = 0
    commands_executed = 0

    with open(log_path + '/cowrie.json', 'r') as f:
        for line in f:
            log = json.loads(line)

            if log.get('protocol') == 'ssh':
                ssh_attempts += 1
            if log.get('protocol') == 'telnet':
                telnet_attempts += 1
            if log.get('eventid') == 'cowrie.login.success':
                successful_logins += 1
            if log.get('eventid') == 'cowrie.login.failed':
                failed_logins += 1
            if log.get('eventid') == 'cowrie.command.input':
                commands_executed += 1

    return ssh_attempts, telnet_attempts, successful_logins, failed_logins, commands_executed

# Flask route for handling user queries and recommendations
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_query = request.form.get('query')
        api_key = request.form.get('api_key')
        recommendation = get_gpt_recommendation(user_query, api_key)
        return render_template('index.html', recommendation=recommendation)

    return render_template('index.html', recommendation=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
