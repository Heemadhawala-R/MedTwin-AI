from flask import Flask, render_template, request
from model import predict_risk, MODEL_ACCURACY
from health_score import calculate_health_score

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html', accuracy=MODEL_ACCURACY)


@app.route('/predict', methods=['POST'])
def predict():
    try:
        age         = int(request.form['age'])
        hr          = int(request.form['heart_rate'])
        bp          = int(request.form['systolic_bp'])
        spo2        = int(request.form['oxygen_level'])
        blood_sugar = int(request.form['Blood_sugar'])

        if not (1 <= age <= 120):
            raise ValueError("Age must be between 1 and 120.")
        if not (30 <= hr <= 220):
            raise ValueError("Heart rate must be between 30 and 220.")
        if not (60 <= bp <= 250):
            raise ValueError("Systolic BP must be between 60 and 250.")
        if not (70 <= spo2 <= 100):
            raise ValueError("Oxygen level must be between 70 and 100.")
        if not (40 <= blood_sugar <= 400):
            raise ValueError("Blood sugar must be between 40 and 400.")

        result     = predict_risk(age, hr, bp, spo2, blood_sugar)
        score_data = calculate_health_score(age, hr, bp, spo2, blood_sugar)

        return render_template(
            'result.html',
            age=age, heart_rate=hr, systolic_bp=bp,
            oxygen_level=spo2, Blood_sugar=blood_sugar,
            health_score=score_data["score"],
            grade=score_data["grade"],
            reasons=score_data["reasons"],
            tips=score_data["tips"],
            risk_label=result["risk_label"],
            accuracy=result["accuracy"],
            probabilities=result["probabilities"],
            explanations=result["explanations"],
        )

    except ValueError as e:
        return render_template('index.html', error=str(e), accuracy=MODEL_ACCURACY)


if __name__ == "__main__":
    print("Starting MedTwin-AI...")
    app.run(debug=True)
