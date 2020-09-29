
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout


'''
Getting the training set. This code is adapted for data downloaded from here:
    For this particular link it is Apple Corp
    https://www.nasdaq.com/market-activity/stocks/aapl/historical
    
    for code you need to download data at MAX button (training set)
    and 1M button - test set
    
    End name it according to the code below
    - for training set don't change anything
    - test set name: HistoricalQuotes_month.csv
'''
dataset_train = pd.read_csv('HistoricalQuotes.csv')
dataset_train[' Open'] = dataset_train[' Open'].str.replace('$', '')
set_strings = dataset_train.iloc[:, 3:4].values
training_set = set_strings.astype(np.float)
row_count = len(training_set)


from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range = (0, 1))
training_set_scaled = sc.fit_transform(training_set)


X_train = []
y_train = []
for i in range(60, row_count):
    X_train.append(training_set_scaled[i-60:i, 0])
    y_train.append(training_set_scaled[i, 0])
X_train, y_train = np.array(X_train), np.array(y_train)

X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

regressor = Sequential()

regressor.add(LSTM(units = 50, return_sequences = True, input_shape = (X_train.shape[1], 1)))
regressor.add(Dropout(0.2))
regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))
regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))
regressor.add(LSTM(units = 50))
regressor.add(Dropout(0.2))
regressor.add(Dense(units = 1))

regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')

regressor.fit(X_train, y_train, epochs = 100, batch_size = 32)

dataset_test = pd.read_csv('HistoricalQuotes_month.csv')
dataset_test[' Open'] = dataset_test[' Open'].str.replace('$', '')
set_strings = dataset_test.iloc[:, 3:4].values
real_stock_price = set_strings.astype(np.float)


dataset_total = pd.concat((dataset_train[' Open'], dataset_test[' Open']), axis = 0)
inputs = dataset_total[len(dataset_total) - len(dataset_test) - 60:].values
inputs = inputs.reshape(-1,1)
inputs = sc.transform(inputs)
X_test = []
for i in range(60, 80):
    X_test.append(inputs[i-60:i, 0])
X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
predicted_stock_price = regressor.predict(X_test)
predicted_stock_price = sc.inverse_transform(predicted_stock_price)

plt.plot(real_stock_price, color = 'red', label = 'Real Stock Price')
plt.plot(predicted_stock_price, color = 'blue', label = 'Predicted Stock Price')
plt.title('Stock Price Prediction')
plt.xlabel('Time')
plt.ylabel('Stock Price')
plt.legend()
plt.show()