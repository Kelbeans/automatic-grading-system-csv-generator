# Quick test to see if Flask server starts
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Server is running!</h1>'

if __name__ == '__main__':
    print("\n" + "="*70)
    print("Testing Flask Server")
    print("="*70)
    print("\nIf you see 'Running on http://127.0.0.1:5000' below, the server works!")
    print("="*70 + "\n")
    app.run(debug=True, port=5000)
