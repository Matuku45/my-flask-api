from flask import Flask, request, jsonify
from flask_cors import CORS
import os  # Added import

app = Flask(__name__)
CORS(app)  # This allows requests from HTML/JavaScript in your browser

# In-memory list to store students
students = [
    {'id': 1, 'name': 'John', 'age': 20}  # Default student
]
next_id = 2  # Start from 2 since 1 is already taken

# ------------------------
# Create a Student
# ------------------------
@app.route('/students', methods=['POST'])
def create_student():
    global next_id
    data = request.get_json()

    # Validate input
    if not data or 'name' not in data or 'age' not in data:
        return jsonify({'error': 'Name and age are required.'}), 400

    # Create student
    student = {
        'id': next_id,
        'name': data['name'],
        'age': data['age']
    }
    students.append(student)
    next_id += 1

    return jsonify(student), 201  # 201 Created

# ------------------------
# Read All Students
# ------------------------
@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students), 200

# ------------------------
# Read a Single Student by ID
# ------------------------
@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = next((s for s in students if s['id'] == student_id), None)
    if student:
        return jsonify(student)
    return jsonify({'error': 'Student not found'}), 404

# ------------------------
# Update a Student
# ------------------------
@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    student = next((s for s in students if s['id'] == student_id), None)

    if not student:
        return jsonify({'error': 'Student not found'}), 404

    # Update fields if provided
    student['name'] = data.get('name', student['name'])
    student['age'] = data.get('age', student['age'])

    return jsonify(student)

# ------------------------
# Delete a Student
# ------------------------
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    global students
    students = [s for s in students if s['id'] != student_id]
    return jsonify({'message': f'Student {student_id} deleted'}), 200

# ------------------------
# Run the app
# ------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use PORT env variable or default to 5000 locally
    app.run(host="0.0.0.0", port=port)
