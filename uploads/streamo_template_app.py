import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

st.title("Interactive Linear Regression Example")

st.write("## Project Description")
st.write("This interactive Streamlit app demonstrates linear regression on a synthetic dataset.")

# User input for controlling the number of data points and other parameters
num_data_points = st.sidebar.slider("Number of Data Points", 50, 500, 100)
random_seed = st.sidebar.slider("Random Seed", 0, 100, 0)
test_size = st.sidebar.slider("Test Size (fraction)", 0.1, 0.5, 0.2)

# Generate random data for x and add noise to y
np.random.seed(random_seed)
x = 2 * np.random.rand(num_data_points, 1)
y = 2 * x + 1 + np.random.randn(num_data_points, 1)

# Convert to DataFrame for better visualization and manipulation
df = pd.DataFrame({'X': x.flatten(), 'Y': y.flatten()})

st.write("## Data Exploration")
st.write(df.head())
st.write("Scatter plot of the data")
fig, ax = plt.subplots()
ax.scatter(x, y)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Data Visualization')
st.pyplot(fig)

# Data Preparation
x_train, x_test, y_train, y_test = train_test_split(df[['X']], df['Y'], test_size=test_size, random_state=0)

# Create a Linear Regression model and fit it to the training data
model = LinearRegression()
model.fit(x_train, y_train)

# Model Evaluation
# Make predictions
y_pred = model.predict(x_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
st.write(f"## Model Evaluation")
st.write(f"Mean Squared Error: {mse}")

# Visualization of Results
st.write("## Visualization of Results")
fig, ax = plt.subplots()
ax.scatter(x, y, label='Actual')
ax.plot(x, model.predict(df[['X']]), color='red', label='Fitted line')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Linear Regression Result')
ax.legend()
st.pyplot(fig)
