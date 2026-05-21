import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import joblib

# ✅ FIXED PATH
data = pd.read_csv("../data/crop_data.csv")

X = data[['N','P','K','temperature','humidity','ph','rainfall']]
y = data['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)

model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# save model
joblib.dump(model, "../data/model.pkl")
joblib.dump(scaler, "../data/scaler.pkl")
print("✅ Model trained & saved successfully")