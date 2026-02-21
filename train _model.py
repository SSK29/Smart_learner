import numpy as np
import joblib
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder

print("Training AI model...")

# Possible answer types
labels = ["V", "A", "R", "K"]

# Train encoder properly
encoder = LabelEncoder()
encoder.fit(labels)

# Number of questions
NUM_QUESTIONS = 30

# Generate synthetic training dataset
X = []
y = []

for i in range(2000):

    # generate random student answers
    answers = np.random.choice(labels, NUM_QUESTIONS)

    X.append(answers)

    # determine dominant learning style
    counts = {
        "Visual": list(answers).count("V"),
        "Auditory": list(answers).count("A"),
        "Reading": list(answers).count("R"),
        "Kinesthetic": list(answers).count("K")
    }

    dominant = max(counts, key=counts.get)

    y.append(dominant)

# Encode answers
X_encoded = []

for row in X:

    encoded_row = encoder.transform(row)

    X_encoded.append(encoded_row)

X_encoded = np.array(X_encoded)

# Train Decision Tree model
model = DecisionTreeClassifier(
    criterion="entropy",
    max_depth=10
)

model.fit(X_encoded, y)

# Save model
joblib.dump(model, "model.pkl")
joblib.dump(encoder, "encoder.pkl")

print("AI Model trained successfully!")
print("Model supports 30 questions.")
