from flask import Flask, jsonify, request
import copy

app = Flask(__name__)

WINDOW_LIMIT = 10
current_list = []

# Mock data to simulate fetched numbers
sample_data = {
    'p': [2, 3, 5, 7, 11],    # Prime numbers
    'f': [1, 1, 2, 3, 5],     # Fibonacci numbers
    'e': [2, 4, 6, 8, 10],    # Even numbers
    'r': [6, 9, 12, 15, 18],  # Random numbers
}

def retrieve_numbers(id_type):
    return sample_data.get(id_type, None)

def refresh_window(new_list):
    global current_list
    previous_list = copy.deepcopy(current_list)
    for number in new_list:
        if number not in current_list:
            if len(current_list) >= WINDOW_LIMIT:
                current_list.pop(0)
            current_list.append(number)
    return previous_list, current_list

def compute_avg(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

@app.route('/numbers/<id_type>', methods=['GET'])
def get_and_process_numbers(id_type):
    id_type = id_type.lower()
    
    if id_type not in sample_data:
        return jsonify({"error": "Invalid number type"}), 400

    fetched_numbers = retrieve_numbers(id_type)
    if fetched_numbers is None:
        return jsonify({"error": "Failed to retrieve numbers"}), 400
    
    previous_state, current_state = refresh_window(fetched_numbers)
    average = compute_avg(current_state)
    
    response = {
        "numbers": fetched_numbers,
        "windowPrevState": previous_state,
        "windowCurrState": current_state,
        "avg": round(average, 2)
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9876, debug=True)
