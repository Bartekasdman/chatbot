from flask import Flask, render_template, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["POST"])
def chat():
    msg = request.json["msg"]
    response = get_Chat_response(msg)
    return jsonify({'reply': response})


# Twój istniejący kod ...

def process_data(data):
    # Przykładowa logika biznesowa: obliczanie sumy i średniej wartości w danych
    data_sum = sum(data)
    data_avg = data_sum / len(data)

    # Przygotowanie odpowiedzi z wynikami
    response = {
        'sum': data_sum,
        'avg': data_avg
    }
    return response

@app.route("/process", methods=["POST"])
def process():
    data = request.json["data"]
    response = process_data(data)
    return jsonify(response)

# Twój istniejący kod ...


def get_Chat_response(text):
    
    if text.lower() == "Hello":
        return "Hello! How can I help you??"
    elif text.lower() == "Goodbye":
        return "Goodbye It was nice to meet you."

    else:
       
        input_ids = tokenizer.encode(text + tokenizer.eos_token, return_tensors='pt')

        
        bot_input_ids = torch.cat([chat_history_ids, input_ids], dim=-1) if 'chat_history_ids' in globals() else input_ids
        chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

        
        response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        return response

if __name__ == '__main__':
    app.run()
