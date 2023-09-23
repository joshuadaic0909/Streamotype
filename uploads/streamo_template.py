#!/usr/bin/env python
# coding: utf-8

# ###### import library

# In[2]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error


# ###### Project Description

# Python and scikit-learn to perform linear regression on a synthetic dataset to predict a continuous outcome variable based on a single predictor. The project covers key data science concepts including data exploration, data splitting, model training, model evaluation, and result visualization using matplotlib.

# ###### Create a simple dataset

# In[3]:


# Generate random data for x and add noise to y
np.random.seed(0)
x = 2 * np.random.rand(100, 1)
y = 2 * x + 1 + np.random.randn(100, 1)

# Convert to DataFrame for better visualization and manipulation
df = pd.DataFrame({'X': x.flatten(), 'Y': y.flatten()})


# ###### Data Exploration

# In[5]:


print(df.head())
plt.scatter(x, y)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Data Visualization')
plt.show()


# ###### Data Preparation

# In[7]:


x_train, x_test, y_train, y_test = train_test_split(df[['X']], df['Y'], test_size=0.2, random_state=0)


# ###### Model Building

# In[8]:


# Create a Linear Regression model and fit it to the training data
model = LinearRegression()
model.fit(x_train, y_train)


# ###### Model Evaluation

# In[10]:


# Make predictions
y_pred = model.predict(x_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")


# ###### Visualization of Results

# In[11]:


plt.scatter(x, y, label='Actual')
plt.plot(x, model.predict(df[['X']]), color='red', label='Fitted line')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Linear Regression Result')
plt.legend()
plt.show()


# In[ ]:




