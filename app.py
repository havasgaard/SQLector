from flask import Flask, request, render_template
import main  # Importer main.py-filen (eller den filen du har koden for skanning i)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        target_url = request.form["url"]
        scan_result = main.scan_url(target_url)  # Kall scan_url-funksjonen fra main.py
        return render_template("result.html", result=scan_result)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
