# app.py
from flask import Flask, render_template, request, jsonify
from crew import run_support_crew

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    try:
        raw_data = request.get_data(as_text=True).strip()
        print(f"🔴 Raw Request: {repr(raw_data)}")
        print(f"📎 Content-Type: {request.content_type}")

        query = ""

        # Try 1: JSON
        if request.is_json:
            try:
                data = request.get_json()
                if isinstance(data, dict):
                    query = data.get("query", "").strip()
            except:
                pass

        # Try 2: Raw string
        if not query and raw_data:
            query = raw_data.strip().strip('"')

        if not query:
            return jsonify({"response": "Please enter a question."})

        print(f"✅ Using Query: '{query}'")

        # Run the crew
        response = run_support_crew(query)
        return jsonify({"response": response})

    except Exception as e:
        print(f"💥 Error in /ask: {e}")
        return jsonify({"response": "Sorry, we couldn't process your request."})

if __name__ == "__main__":
    app.run(debug=True)