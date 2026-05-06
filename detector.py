import numpy as np
from sklearn.ensemble import IsolationForest

# -----------------------------------------------------------
# ------Train Model
# -----------------------------------------------------------


def train_model():
    # build and train model from normal data
    np.random.seed(42)
    normal_data = np.column_stack([
        np.random.uniform(220, 240, 200),  # normal voltage
        np.random.uniform(8, 14, 200),     # normal current
        np.random.uniform(1800, 2800, 200)   # normal power
    ])

    # Train Isolation Forest model

    model = IsolationForest(
        contamination=0.2,  # maybe 20% anomalies
        random_state=42.
    )
    model.fit(normal_data)
    return model

# ---load model from startup


model = train_model()

# -----------------------------------------------------------
# ------Detect Anomalies
# -----------------------------------------------------------


def detect_anomaly(voltage: float, current: float, power: float) -> dict:
    # predict if the data is an anomaly

    # change to array for maodel
    data = np.array([[voltage, current, power]])

    # predict -1 is anomaly, 1 is normal
    prediction = model.predict(data)[0]
    score = model.score_samples(data)[0]  # anomaly score

    is_anomaly = prediction == -1
    return {
        "is_anomaly": is_anomaly,
        "score": round(float(score), 4),
        "severity": get_severity(score)
    }


def get_severity(score: float) -> str:
    # change score to severity level
    if score > -0.1:
        return "normal"
    elif score > -0.3:
        return "low"
    elif score > -0.5:
        return "medium"
    else:
        return "high"
