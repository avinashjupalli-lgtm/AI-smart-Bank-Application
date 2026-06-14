import joblib

model = joblib.load("fraud_model.pkl")

sample = [[70000, 10, -60000, 1]]

prediction = model.predict(sample)

print(prediction)