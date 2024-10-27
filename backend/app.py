from flask import Flask,request, jsonify
app = Flask(__name__)

@app.route("/extract-skills", methods=["POST"])
def extract_skills():
    # Dummy response - you’ll replace this with actual model logic later
    data = request.json.get("text", "")
    response = {"skills": ["Python", "Flask", "Docker"]}  # example skills
    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)