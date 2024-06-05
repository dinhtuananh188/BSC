import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import matplotlib.pyplot as plt
import joblib

# Load data from Excel file
file_path = 'data.csv'
df = pd.read_csv(file_path)

# Assume the last column contains labels
x = df.iloc[:, :5].values.astype(float)
y_ = df.iloc[:, 5].values.reshape(-1, 1)
print("Number of rows in the DataFrame:", len(df))

# Convert label data for machine learning
encoder = OneHotEncoder(sparse=False)
y = encoder.fit_transform(y_)

# Split data for training and testing
train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.20, random_state=42)

# Build a neural network model
model = Sequential()
model.add(Dense(10, input_shape=(x.shape[1],), activation='relu', name='fc1'))
model.add(Dense(10, activation='relu', name='fc2'))
model.add(Dense(y.shape[1], activation='softmax', name='output'))

# Use the Adam optimizer with a learning rate of 0.001
optimizer = Adam(lr=0.001)
model.compile(optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

print('Neural Network Model Summary:')
print(model.summary())

# Train the model
history = model.fit(train_x, train_y, verbose=2, batch_size=49, epochs=1000, validation_data=(test_x, test_y))

# Save the model
model.save('trained_model.h5')

# Save the encoder
joblib.dump(encoder, 'label_encoder.joblib')

# Evaluate the model on the test set
results = model.evaluate(test_x, test_y)

print('Final test set loss: {:4f}'.format(results[0]))
print('Final test set accuracy: {:4f}'.format(results[1]))

# Plot loss and accuracy
plt.figure(figsize=(12, 4))

# Loss plot
plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Training and Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

# Accuracy plot
plt.subplot(1, 2, 2)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Training and Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

# Show the plots
plt.show()
