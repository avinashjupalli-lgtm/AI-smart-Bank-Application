import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier

from sklearn.model_selection import (
    train_test_split,
    cross_val_score
)

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)

import matplotlib.pyplot as plt

# ----------------------------
# Load Dataset
# ----------------------------

data = pd.read_csv("dataset.csv")

print("\nDataset Loaded Successfully\n")
print("Dataset Shape:", data.shape)

# ----------------------------
# Features & Target
# ----------------------------

X = data.drop("risk", axis=1)
y = data["risk"]

# ----------------------------
# Train Test Split
# ----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ----------------------------
# Train Model
# ----------------------------

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# ----------------------------
# Prediction
# ----------------------------

y_pred = model.predict(X_test)

# ----------------------------
# Accuracy
# ----------------------------

accuracy = accuracy_score(
    y_test,
    y_pred
)

print("Accuracy :", accuracy)

# ----------------------------
# Precision
# ----------------------------

precision = precision_score(
    y_test,
    y_pred,
    average="weighted"
)

print("Precision :", precision)

# ----------------------------
# Recall
# ----------------------------

recall = recall_score(
    y_test,
    y_pred,
    average="weighted"
)

print("Recall :", recall)

# ----------------------------
# F1 Score
# ----------------------------

f1 = f1_score(
    y_test,
    y_pred,
    average="weighted"
)

print("F1 Score :", f1)

# ----------------------------
# Classification Report
# ----------------------------

print("\nClassification Report\n")

print(
    classification_report(
        y_test,
        y_pred
    )
)

# ----------------------------
# Confusion Matrix
# ----------------------------

cm = confusion_matrix(
    y_test,
    y_pred
)

print("\nConfusion Matrix\n")

print(cm)

# ----------------------------
# Save Confusion Matrix Image
# ----------------------------

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm
)

disp.plot()

plt.savefig(
    "confusion_matrix.png"
)

plt.close()

# ----------------------------
# Cross Validation
# ----------------------------

# ----------------------------
# Cross Validation
# ----------------------------

scores = cross_val_score(
    model,
    X,
    y,
    cv=2
)

print(
    "\nCross Validation Scores:",
    scores
)

print(
    "Average CV Accuracy:",
    scores.mean()
)
# ----------------------------
# Save Evaluation Results
# ----------------------------

with open(
    "evaluation.txt",
    "w"
) as f:

    f.write(
        f"Accuracy : {accuracy}\n"
    )

    f.write(
        f"Precision : {precision}\n"
    )

    f.write(
        f"Recall : {recall}\n"
    )

    f.write(
        f"F1 Score : {f1}\n"
    )

# ----------------------------
# Save Model
# ----------------------------

joblib.dump(
    model,
    "fraud_model.pkl"
)

print(
    "\nFraud Model Saved Successfully"
)