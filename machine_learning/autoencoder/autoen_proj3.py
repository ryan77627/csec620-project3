import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense

input_file = "unlabeled_flows.csv"
df = pd.read_csv(input_file)

numerical_features = df.select_dtypes(include=[np.number]).columns
if numerical_features.empty:
    raise ValueError("No numerical columns found in the dataset.")

X = df[numerical_features].dropna().values 

if X.shape[0] == 0:
    raise ValueError("No valid data available after dropping missing values.")

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

input_dim = X_scaled.shape[1]
encoding_dim = 3 

input_layer = Input(shape=(input_dim,))
encoded = Dense(encoding_dim, activation='relu')(input_layer)
decoded = Dense(input_dim, activation='sigmoid')(encoded)

autoencoder = Model(inputs=input_layer, outputs=decoded)

autoencoder.compile(optimizer='adam', loss='mean_squared_error')

autoencoder.fit(X_scaled, X_scaled, epochs=50, batch_size=256, shuffle=True, validation_split=0.2)

autoencoder.save("autoencoder_model.h5")

X_pred = autoencoder.predict(X_scaled)
reconstruction_error = np.mean(np.abs(X_scaled - X_pred), axis=1)

anomaly_file = "reconstruction_errors.csv"
pd.DataFrame({"reconstruction_error": reconstruction_error}).to_csv(anomaly_file, index=False)

print(f"Reconstruction errors saved to {anomaly_file}")
