# -*- coding: utf-8 -*-
"""ANN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1x8Ty-lEPjxWFNI_r39mZBs4EPtJ__FOn

# **Artificial Neural Networks**

# Part 1 : Data Preprocessing

## Import the Libraries
"""

import numpy as np
import pandas as pd
import tensorflow as tf

"""## Importing the Dataset"""

dataset = pd.read_csv('Churn_Modelling.csv')
X = dataset.iloc[:,3:-1].values
y = dataset.iloc[:,-1].values

"""## Encoding the Categorical Data:

### Label Encoding the "Gender" Column:
"""

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
X[:,2] = le.fit_transform(X[:,2])

"""### OneHotEncoding the "Geography" Column:"""

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
ct = ColumnTransformer(transformers = [('encoder', OneHotEncoder(), [1])], remainder = 'passthrough')
X = ct.fit_transform(X)
X = np.array(X)

print(X)

"""## Splitting the data into Training and Test set:"""

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

"""## Feature Scaling:"""

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

"""# Part 2 : Building the ANN

## Initializing the ANN :
"""

ann = tf.keras.models.Sequential()

"""## Adding the input layer and the first Hidden Layer:"""

ann.add(tf.keras.layers.Dense(units = 6, activation = 'relu'))

"""## Adding the second hidden layer:"""

ann.add(tf.keras.layers.Dense(units = 6, activation = 'relu'))

"""## Adding the output Layer:"""

ann.add(tf.keras.layers.Dense(units = 1, activation = 'sigmoid'))

"""# Training the ANN:

## Compiling the ANN:
"""

ann.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

"""## Training the ANN on the Training Set:"""

ann.fit(X_train, y_train, batch_size = 32, epochs = 100)

"""# Predicting and evaluating the model:

Question:
Geography = France,
Credit Score = 600,
Gender = Male,
Age = 40 years old,
Tenure = 3 years,
Balance = $60000,
No. of Products = 3,
Credit Card = Yes,
Active Member = Yes,
Salary Estimated = $50000,
Should we say goodbye to that customer?
"""

print(ann.predict(sc.transform([[1, 0, 0, 600, 1, 40, 3, 60000, 2, 1, 1, 50000]])))

"""## Predicting the test set results:"""

y_pred = ann.predict(X_test)
y_pred = (y_pred>0.5)
print(np.concatenate((y_pred.reshape(len(y_pred), 1), y_test.reshape(len(y_test), 1)),1))

"""## Making the confusion matrix:"""

from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test, y_pred)
print(cm)
accuracy_score(y_test, y_pred)