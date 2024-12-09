import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import matplotlib.pyplot as plt

# Load the labeled CSV file
input_file = 'revised_labeled_flows.csv'
data = pd.read_csv(input_file)

# Encode the label column as integers
label_mapping = {'Realm': 0, 'Sliver': 1, 'HeadHunter': 2, 'benign': 3}
data['label'] = data['label'].map(label_mapping)

# Handle missing values: Impute with the mean for numerical columns
imputer = SimpleImputer(strategy='constant', fill_value=0)
data_imputed = pd.DataFrame(imputer.fit_transform(data.drop(columns=['label', 'sa', 'da'])), columns=data.drop(columns=['label', 'sa', 'da']).columns)

# Now include the label column back into the dataset
data_imputed['label'] = data['label']

# Split the dataset into features (X) and target (y)
X = data_imputed.drop(columns=['label'])
y = data_imputed['label']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Scale the features for better performance with KNN
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Initialize and train the KNN classifier
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train_scaled, y_train)

# Make predictions on the test set
y_pred = knn.predict(X_test_scaled)

# Evaluate the model
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred, target_names=label_mapping.keys()))

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=label_mapping.keys(), yticklabels=label_mapping.keys())
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

