import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor

# -----------------------------
# 1. Load your dataset
# -----------------------------
data = pd.read_csv("/Users/akashbarpanda/Documents/summer/internship/.venv/MLcodes/practise/ball_by_ball_filled.csv")  # replace with your CSV path

# Strip any whitespace in column names
data.columns = data.columns.str.strip()

# -----------------------------
# 2. Define features and target
# -----------------------------
features = ['batting_team', 'batsman', 'non_striker', 'bowler', 'venue', 'match_type', 'overs']
target = 'runs.total'

X = data[features]
y = data[target]

# -----------------------------
# 3. Encode categorical columns
# -----------------------------
le_dict = {}
X_encoded = X.copy()

for col in X.columns:
    if X[col].dtype == 'object':
        le = LabelEncoder()
        X_encoded[col] = le.fit_transform(X[col])
        le_dict[col] = le
    else:
        le_dict[col] = None  # numeric columns don't need encoding

# -----------------------------
# 4. Train a model (example)
# -----------------------------
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_encoded, y)

# -----------------------------
# 5. Function to predict from random row
# -----------------------------
def predict_from_random_row(model, X, X_encoded, le_dict):
    # Pick a random row
    idx = np.random.randint(0, X.shape[0])
    row = X.iloc[idx]

    actual_runs = row[target] if target in row else None

    # Extract features for prediction
    X_row = row[features].to_frame().T

    # Encode categorical features
    for col in features:
        if le_dict[col] is not None:
            X_row[col] = le_dict[col].transform(X_row[col])

    # Predict
    predicted_runs = model.predict(X_row)[0]

    print(f"Random row index: {idx}")
    print("Input features:")
    print(row[features])
    print(f"Actual runs: {actual_runs}")
    print(f"Predicted runs: {predicted_runs:.2f}\n")

    return predicted_runs, actual_runs

# -----------------------------
# 6. Test the prediction
# -----------------------------
predicted, actual = predict_from_random_row(model, X, X_encoded, le_dict)
