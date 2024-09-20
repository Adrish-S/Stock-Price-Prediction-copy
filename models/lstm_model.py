import tensorflow
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Input
from tensorflow.keras.regularizers import l2


def build_lstm_model(input_shape):
    model = Sequential()

    # Use Input layer instead of passing input_shape directly to the LSTM layer
    model.add(Input(shape=input_shape))

    # LSTM layers with regularization
    model.add(LSTM(128, activation='relu', return_sequences=True, kernel_regularizer=l2(0.001)))
    model.add(Dropout(0.3))  # Dropout to reduce overfitting
    model.add(LSTM(64, activation='relu', kernel_regularizer=l2(0.001)))
    model.add(Dropout(0.3))

    # Output layer with sigmoid for binary classification
    model.add(Dense(1, activation='sigmoid'))

    # Compile the model
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    return model


