from flask import Flask, jsonify, request
import copy

app = Flask(__name__)

WINDOW_SIZE = 10
current_window = []

# Mock data to simulate fetched numbers
mock_data = {
    'p': [2, 3, 5, 7, 11],    # Prime numbers
    'f': [1, 1, 2, 3, 5],     # Fibonacci numbers
    'e': [2, 4, 6, 8, 10],    # Even numbers
    'r': [6, 9, 12, 15, 18],  # Random numbers
}

def fetch_numbers(number_id):
    return mock_data.get(number_id, None)

def update_window(new_numbers):
    global current_window
    previous_window = copy.deepcopy(current_window)
    for num in new_numbers:
        if num not in current_window:
            if len(current_window) >= WINDOW_SIZE:
                current_window.pop(0)
            current_window.append(num)
    return previous_window, current_window

def calculate_average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

@app.route('/numbers/<number_id>', methods=['GET'])
def get_numbers(number_id):
    number_id = number_id.lower()
    
    if number_id not in mock_data:
        return jsonify({"error": "Invalid number ID"}), 400

    numbers = fetch_numbers(number_id)
    if numbers is None:
        return jsonify({"error": "Failed to fetch numbers"}), 400
    
    prev_window, curr_window = update_window(numbers)
    avg = calculate_average(curr_window)
    
    response = {
        "numbers": numbers,
        "windowPrevState": prev_window,
        "windowCurrState": curr_window,
        "avg": round(avg, 2)
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9876, debug=True)
