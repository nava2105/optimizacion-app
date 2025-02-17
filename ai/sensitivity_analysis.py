import numpy as np
import joblib
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# File where the trained model will be stored
MODEL_FILE = "ai/sensitivity_model.pkl"
DATA_FILE = "ai/training_data.npz"  # File to store training data


def train_sensitivity_model(X, y):
    """
    Trains a Random Forest model for sensitivity analysis.
    Saves the trained model to a file.
    """
    X = np.array(X)
    y = np.array(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Save the trained model and training data
    joblib.dump(model, MODEL_FILE)
    np.savez(DATA_FILE, X=X, y=y)
    print("Sensitivity Analysis Model trained and saved.")


def analyze_sensitivity(data):
    """
    Uses the trained model for sensitivity analysis.
    Automatically retrains with new data and updates the model.
    """
    new_X = np.array(data["scenarios"])
    new_y = np.array(data["objective_values"])

    # Load existing data if available
    if os.path.exists(DATA_FILE):
        stored_data = np.load(DATA_FILE)
        X = np.vstack((stored_data["X"], new_X))
        y = np.hstack((stored_data["y"], new_y))
    else:
        X, y = new_X, new_y

    # Retrain model with updated data
    train_sensitivity_model(X, y)

    # Load the updated model
    model = joblib.load(MODEL_FILE)

    # Make predictions
    predictions = model.predict(new_X)

    return {
        "sensitivity_coefficients": predictions.tolist(),
        "model_updated": True
    }
