import sqlite3
import csv
from flask import Flask, render_template, request, send_file
import pickle
import os

app = Flask(__name__)


def get_db():
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    return connection


# Load the saved model
with open("series_model.pkl", "rb") as apk:
    model = pickle.load(apk)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    name = request.form["name"]
    category = request.form["category"]
    input_data = [float(request.form["input1"]), int(request.form["input2"])]

    prediction_arr = model.predict([input_data])[0]
    prediction = int(prediction_arr[0])
    message = (
        "Good 👍:\nA captivating masterpiece that leaves you craving for more!"
        if prediction == 1
        else "Bad 👎:\nA disappointing flop that fails to engage its audience."
    )

    # Save data to database
    db = get_db()
    db.execute(
        "INSERT INTO ratings (name, category, imdb_rating, rotten_tomato_rating, prediction) VALUES (?, ?, ?, ?, ?)",
        (name, category, input_data[0], input_data[1], prediction),
    )
    db.commit()
    db.close()

    return render_template(
        "result.html", name=name, category=category, prediction=message
    )


@app.route("/db")
def data():
    db = get_db()
    ratings = db.execute("SELECT * FROM ratings").fetchall()

    with open("/tmp/data.csv", "w") as f:
        out = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        header = [
            "id",
            "created",
            "name",
            "category",
            "imdb_rating",
            "rotten_tomato_rating",
            "prediction",
        ]
        out.writerow(header)

        for rec in ratings:
            out.writerow([rec[c] for c in header])
    db.close()
    return render_template("data.html", ratings=ratings, value="data.csv")


@app.route("/download/<file_name>")
def download(file_name):
    try:
        return send_file(
            "/tmp/" + file_name,
            as_attachment=True,
        )
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    app.run(debug=True, port=os.getenv("PORT", default=5000))
