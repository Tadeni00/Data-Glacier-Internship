import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

# Create flask app
iris_app = Flask(__name__)

# Load Pickle Model
model = pickle.load(open("model.pkl", "rb"))

@iris_app.route("/")
def Home():
    return render_template("index.html")

@iris_app.route("/predict", methods = ["POST"])
def predict():
    float_features = [float(x) for x in request.form.values()]
    features = [np.array(float_features)]
    prediction = model.predict(features)
    return render_template("index.html", prediction_text = "The flower species is {}".format(prediction))

if __name__ == "__main__":
    iris_app.run(debug=True)