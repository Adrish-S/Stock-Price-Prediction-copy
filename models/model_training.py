# models/model_training.py

import pickle
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.regularizers import l2
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from tensorflow.keras.callbacks import EarlyStopping
from data.datacollection import prepare_data_for_lstm

def build_lstm_model(input_shape):
    model = Sequential()

    # Add LSTM layers with regularization
    model.add(
        LSTM(128, activation='relu', return_sequences=True, input_shape=input_shape, kernel_regularizer=l2(0.001)))
    model.add(Dropout(0.3))  # Adding Dropout to reduce overfitting
    model.add(LSTM(64, activation='relu', return_sequences=False, kernel_regularizer=l2(0.001)))
    model.add(Dropout(0.3))

    # Output layer with sigmoid for binary classification
    model.add(Dense(1, activation='sigmoid'))

    # Compile the model
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss='binary_crossentropy',
                  metrics=['accuracy'])

    return model
def train_model():
    # Load data and prepare sequences
    X_train, X_test, y_train, y_test, scaler = prepare_data_for_lstm('data/store_stock_data.csv')

    # Build the LSTM model
    model = build_lstm_model(input_shape=(X_train.shape[1], X_train.shape[2]))

    # Train the model
    model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2, verbose=1)

    # Save the trained model
    model.save('models/trained_lstm_model.h5')
    with open('models/scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)

    # Evaluate the model
    y_pred_prob = model.predict(X_test)
    y_pred = (y_pred_prob > 0.5).astype(int).flatten()

    # Calculate and print metrics
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model accuracy: {accuracy:.2f}")

    print("Classification Report:")
    print(classification_report(y_test, y_pred,zero_division=1))

    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    print("Model trained and saved!")
