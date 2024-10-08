import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import streamlit as st

# load data
data = pd.read_csv('creditcard.csv')

# separate legitimate and fraudulent transactions
legit = data[data.Class == 0]
fraud = data[data.Class == 1]

# undersample legitimate transactions to balance the classes
legit_sample = legit.sample(n=len(fraud), random_state=2)
data = pd.concat([legit_sample, fraud], axis=0)

# split data into training and testing sets
X = data.drop(columns="Class", axis=1)
y = data["Class"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=2)

# train logistic regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# evaluate model performance
train_acc = accuracy_score(model.predict(X_train), y_train)
test_acc = accuracy_score(model.predict(X_test), y_test)

# create Streamlit app
st.title("Credit Card Fraud Detection Model")
st.write("Enter the following features (comma separated) to check if the transaction is legitimate or fraudulent:")

# create input fields for user to enter feature values
input_df = st.text_input('Input All features (comma separated):')

# create a button to submit input and get prediction
submit = st.button("Submit")

if submit:
    try:
        # get input feature values
        input_df_lst = input_df.split(',')
        
        # Clean input and remove unwanted characters
        cleaned_input = [i.strip().replace('"', '') for i in input_df_lst]
        
        # Convert to float
        features = np.array([float(i) for i in cleaned_input])
        
        # ensure correct number of features
        if len(features) == X.shape[1]:
            # make prediction
            features = features.reshape(1, -1)
            prediction = model.predict(features)
            
            # display result
            if prediction[0] == 0:
                st.write("Legitimate transaction")
            else:
                st.write("Fraudulent transaction")
        else:
            st.error(f"Expected {X.shape[1]} features, but got {len(features)}.")
    
    except ValueError as e:
        st.error(f"Please enter valid numeric values for all features. Error: {str(e)}")
