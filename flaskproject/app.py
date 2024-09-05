from flask import Flask, render_template, request, jsonify
import replicate
import os
import json
app = Flask(__name__)

# Set your Replicate API token
os.environ['REPLICATE_API_TOKEN'] = "r8_C2lwJukQk3VSkO5wCZGH8SQ9jTWTT4D3z2z1u"

# Define your model ID from Replicate
model_id = "meta/llama-2-13b-chat:56acad22679f6b95d6e45c78309a2b50a670d5ed29a37dd73d182e89772c02f1"

# 14ce4448d5e7e9ed0c37745ac46eca157aab09061f0c179ac2b323b5de56552b
generated_output = None
# Function to get response from the model
def get_llama_response(input_text, no_ques, difficulty):
    # Define the prompt template
    template = f"""
    Generate a multiple-choice quiz on the topic "{input_text}" of total questions {no_ques}  at a {difficulty} difficulty level. Provide the output in this exact JSON format:
    
    [
      {{
        "question": "Question 1 text here",
        "options": ["Option A text", "Option B text", "Option C text", "Option D text"]
      }},
      {{
        "question": "Question 2 text here",
        "options": ["Option A text", "Option B text", "Option C text", "Option D text"]
      }},
      ...
    ]
    """ 

    # Call the model using Replicate's API
    output = replicate.run(
        model_id,
        input={
            "prompt": template,
            "max_length": 4000,
            "temperature": 0.01,
        }
    )

    
    # Convert generator to string
    output_str = "".join(output)
    print(output_str)
    return output_str

@app.route('/')
def index():
    return render_template('index.html', output=[])

 
@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    input_text = data['input_text']
    no_ques = int(data['no_ques'])  
    difficulty = data['difficulty']

    output = get_llama_response(input_text, no_ques, difficulty)
    start_index = output.index('[')
    end_index = output.rindex(']') + 1

# Extract the JSON portion
    json_string = output[start_index:end_index]

# Step 2: Parse the JSON data
    data = json.loads(json_string)
    print(f"Output passed to template: {data}")  # Debug print


    return jsonify(data)
if __name__ == '__main__':
    app.run(debug=True)
