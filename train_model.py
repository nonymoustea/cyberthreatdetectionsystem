import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
data = pd.read_csv('phishing_emails.csv')  # Ensure this file has 'body' and 'label' columns

# Clean data
data = data[['body', 'label']].dropna()
X_raw = data['body']
y = data['label']

# Text vectorization
vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
X = vectorizer.fit_transform(X_raw)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model and vectorizer
joblib.dump(model, 'text_model.pkl')
joblib.dump(vectorizer, 'text_vectorizer.pkl')

# Evaluate model
print("Training complete.")
print("Train Accuracy: {:.2f}".format(model.score(X_train, y_train)))
print("Test Accuracy: {:.2f}".format(model.score(X_test, y_test)))
