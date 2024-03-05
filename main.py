from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Load the saved model
with open('series_model.pkl', 'rb') as apk:
    model = pickle.load(apk)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    name = request.form['name']
    category = request.form['category']
    input_data = [float(request.form['input1']), int(request.form['input2'])]


    prediction_arr = model.predict([input_data])[0]
    prediction = int(prediction_arr[0])
    message = "Good 👍:\nA captivating masterpiece that leaves you craving for more!" if prediction == 1 else "Bad 👎:\nA disappointing flop that fails to engage its audience."
    
    return render_template('result.html',name=name, category=category, prediction=message)

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
