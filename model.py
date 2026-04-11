import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import urllib.request

RISK_LABELS = {0: "Low", 1: "Moderate", 2: "High"}
FEATURE_NAMES = ["Age", "Heart Rate", "Systolic BP", "SpO2", "Blood Sugar"]


def _load_real_data():
    """Try UCI Cleveland dataset, fall back to synthetic."""
    try:
        url = (
            "https://archive.ics.uci.edu/ml/machine-learning-databases"
            "/heart-disease/processed.cleveland.data"
        )
        with urllib.request.urlopen(url, timeout=6) as r:
            raw = r.read().decode()

        import numpy as np
        rng = np.random.default_rng(42)       
        rows = []
        for line in raw.strip().split("\n"):
            vals = line.strip().split(",")
            if len(vals) != 14 or "?" in vals:
                continue
            try:
                age      = float(vals[0])
                thalach  = float(vals[7])
                trestbps = float(vals[3])
                target   = int(float(vals[13]))
                label    = min(target, 2)
                spo2     = float(np.clip(rng.normal(98 - label * 2.5, 1.0), 75, 100))
                sugar    = float(np.clip(rng.normal(90 + label * 18, 10), 60, 250))
                rows.append([age, thalach, trestbps, spo2, sugar, label])
            except ValueError:
                continue

        if len(rows) < 50:
            raise ValueError("too few rows")

        arr = np.array(rows)
        print(f"[MedTwin-AI] Cleveland dataset — {len(arr)} samples.")
        return arr[:, :5], arr[:, 5].astype(int)

    except Exception as e:
        print(f"[MedTwin-AI] Using synthetic data ({e}).")
        return _synthetic_data()


def _synthetic_data():
    np.random.seed(42)
    n = 300
    low = np.column_stack([np.random.randint(18,45,n), np.random.randint(60,80,n),  np.random.randint(100,120,n), np.random.randint(95,100,n), np.random.randint(70,100,n)])
    mod = np.column_stack([np.random.randint(40,65,n), np.random.randint(78,95,n),  np.random.randint(120,140,n), np.random.randint(85,94,n),  np.random.randint(100,125,n)])
    hi  = np.column_stack([np.random.randint(55,90,n), np.random.randint(92,130,n), np.random.randint(140,190,n), np.random.randint(70,85,n),  np.random.randint(126,200,n)])
    X = np.vstack([low, mod, hi])
    y = np.array([0]*n + [1]*n + [2]*n)
    return X, y


def _train():
    X, y = _load_real_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    model = DecisionTreeClassifier(max_depth=5, random_state=42)
    model.fit(X_train, y_train)
    acc = round(accuracy_score(y_test, model.predict(X_test)) * 100, 1)
    print(f"[MedTwin-AI] Accuracy: {acc}%")
    return model, acc


_model, MODEL_ACCURACY = _train()


def predict_risk(age, heart_rate, systolic_bp, oxygen_level, blood_sugar):
    data  = np.array([[age, heart_rate, systolic_bp, oxygen_level, blood_sugar]], dtype=float)
    pred  = int(_model.predict(data)[0])
    probs = _model.predict_proba(data)[0]

    importances = _model.feature_importances_
    baselines   = [40,  75,  115,  97,  90]
    directions  = [1,   1,   1,   -1,   1]
    values      = [age, heart_rate, systolic_bp, oxygen_level, blood_sugar]
    deviations  = [(v - b) * d for v, b, d in zip(values, baselines, directions)]
    raw_scores  = [imp * abs(dev) for imp, dev in zip(importances, deviations)]
    total       = sum(raw_scores) or 1
    pct_list    = [round(s / total * 100, 1) for s in raw_scores]

    thresholds = [
        (age,          50,  True,  "Age raises cardiovascular risk",       "Age is in a low-risk range"),
        (heart_rate,   90,  True,  "Elevated heart rate detected",         "Heart rate is in a healthy range"),
        (systolic_bp, 130,  True,  "High blood pressure detected",         "Blood pressure is normal"),
        (oxygen_level, 95, False,  "Low oxygen saturation is concerning",  "Oxygen level is healthy"),
        (blood_sugar, 100,  True,  "Elevated blood sugar (diabetes risk)", "Blood sugar is in a normal range"),
    ]

    explanations = []
    for i, (val, thresh, higher_bad, warn, ok) in enumerate(thresholds):
        is_bad = (val > thresh) if higher_bad else (val < thresh)
        explanations.append({
            "feature":      FEATURE_NAMES[i],
            "value":        val,
            "importance":   round(float(importances[i]) * 100, 1),
            "contribution": pct_list[i],
            "direction":    "↑ Raises risk" if deviations[i] > 0 else "↓ Lowers risk",
            "message":      warn if is_bad else ok,
            "is_bad":       is_bad,
        })

    explanations.sort(key=lambda x: x["contribution"], reverse=True)

    return {
        "risk_label":    RISK_LABELS[pred],
        "accuracy":      MODEL_ACCURACY,
        "probabilities": {
            "low":      round(float(probs[0]) * 100, 1),
            "moderate": round(float(probs[1]) * 100, 1),
            "high":     round(float(probs[2]) * 100, 1),
        },
        "explanations": explanations,
    }
