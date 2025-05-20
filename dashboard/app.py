from flask import Flask, render_template, request
from llm_service import get_recent_samples_and_insights

app = Flask(__name__)

@app.route('/')
def index():
    samples, llm_response = get_recent_samples_and_insights()
    return render_template("index.html", samples=samples, llm_output=llm_response)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
