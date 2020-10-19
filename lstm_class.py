from Classifier import *
from datetime import date
import stock_market as sm
import numpy as np

from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout, LSTM
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau, CSVLogger
from tensorflow.keras import optimizers


########### NEED TO FIX INPUTS AND OUTPUTS

class lstm_classifier(Classifier):
    def __init__(self,ticker,inputSize=5, binary=True, risk=0.5, numTrainDays=300):
        self.type = 'LSTM'
        self.ticker=ticker
        self.days=inputSize
        self.inputSize = inputSize
        self.binary=binary
        self.risk_thresh = risk
        self.numTrainDays = numTrainDays
        self.params = {
            "batch_size": 20,  # 20<16<10, 25 was a bust
            "epochs": 300,
            "lr": 0.00010000,
            "time_steps": 60
            }
        self.model = self.create_model()



    def create_model(self):
        lstm_model = Sequential()
        # (batch_size, timesteps, data_dim)
        lstm_model.add(LSTM(100, batch_input_shape= (self.params["batch_size"], self.params["time_steps"], self.inputSize),
                            dropout=0.0, recurrent_dropout=0.0, #stateful=True, 
                            return_sequences=True, kernel_initializer='random_uniform'))
        lstm_model.add(Dropout(0.4))
        lstm_model.add(LSTM(60, dropout=0.0))
        lstm_model.add(Dropout(0.4))
        lstm_model.add(Dense(20,activation='relu'))
        lstm_model.add(Dense(1,activation='sigmoid'))
        optimizer = optimizers.RMSprop(lr=self.params["lr"])
        lstm_model.compile(loss='mean_squared_error', optimizer=optimizer)


    def trainClf(self, endDay=date.today(), numTrainDays=100):
        X, Y = self.processData(endDay, self.numTrainDays)
        self.fit(X, Y)
    

    def predict(self, inputArray):
        inputArray = np.array(inputArray)
        inputArray.reshape([1,-1])

        pred = self.model.predict(inputArray, batch_size=self.inputSize)

        if self.binary: pred = (np.array(pred)[:,1] > 0)*1

        return pred



    def fit(self, X, Y):
        history = self.model.fit(X, Y, epochs=self.params["epochs"], verbose=2, batch_size=self.params["batch_size"],
                        shuffle=False)# , validation_data=(trim_dataset(x_val, BATCH_SIZE), trim_dataset(y_val, BATCH_SIZE)))
        self.model.fit(X,Y)

    def saveModel(self):
        pickle.dump(self.model, open("lstm_model","wb"))
