import numpy as np

from keras.models import load_model

model = load_model('model.h5')
# Assuming 'X_test' contains your test data
predictions = model.predict(X_test)

# Example: Print the first prediction
print(predictions[0])
