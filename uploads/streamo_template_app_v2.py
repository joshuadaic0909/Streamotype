import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report

# ----------------------- Functions -----------------------

def generate_fake_data(size=1000):
    np.random.seed(42)
    age = np.random.randint(20, 70, size=size)
    income = np.random.randint(10000, 100000, size=size)
    outcome = np.random.choice([0, 1], size=size)
    df = pd.DataFrame({'Age': age, 'Income': income, 'Outcome': outcome})
    return df

def plot_interactive(data):
    st.subheader("Interactive Data Exploration")
    plot_type = st.selectbox("Choose type of plot", ["Scatter", "Histogram", "Box"])
    selected_columns = st.multiselect("Select columns to plot", data.columns[:-1], default=data.columns[:-1])
    if plot_type == "Scatter" and len(selected_columns) > 1:
        fig = px.scatter(data, x=selected_columns[0], y=selected_columns[1], color="Outcome", template="plotly_dark")
    elif plot_type == "Histogram":
        fig = px.histogram(data, x=selected_columns[0], color="Outcome", template="plotly_dark")
    else:
        fig = px.box(data, x=selected_columns[0], y="Outcome", template="plotly_dark")
    st.plotly_chart(fig)

def dynamic_feature_engineering(data):
    st.subheader("Dynamic Feature Engineering")
    if st.checkbox("Add Interaction Features"):
        feature_1 = st.selectbox("Select Feature 1", data.columns[:-1], index=0)
        feature_2 = st.selectbox("Select Feature 2", data.columns[:-1], index=1)
        data[f"{feature_1}_x_{feature_2}"] = data[feature_1] * data[feature_2]
    return data

def train_and_predict(df):
    # Splitting the data
    X = df.drop('Outcome', axis=1)
    y = df['Outcome']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Model Training
    st.subheader("Model Selection and Training")
    algorithm = st.selectbox("Select a Classification Algorithm", ["Logistic Regression", "Random Forest", "Gradient Boosting"])

    if algorithm == "Random Forest":
        n_estimators = st.slider("Number of Trees", 10, 150, 100)
        max_depth = st.slider("Maximum Depth", 1, 10, 5)
        model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth)
    elif algorithm == "Gradient Boosting":
        learning_rate = st.slider("Learning Rate", 0.01, 1.0, 0.1)
        n_estimators = st.slider("Number of Estimators", 10, 150, 100)
        model = GradientBoostingClassifier(n_estimators=n_estimators, learning_rate=learning_rate)
    else:
        C = st.slider("Inverse Regularization Strength", 0.01, 10.0, 1.0)
        model = LogisticRegression(C=C)

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    st.write(classification_report(y_test, y_pred))

# ----------------------- Main App -----------------------

def run_app():
    st.title("Advanced Interactive Streamlit App")

    # Generating fake data
    df = generate_fake_data()
    st.write(df.head())

    # Data Visualization
    plot_interactive(df)
    
    # Feature Engineering
    df = dynamic_feature_engineering(df)

    # Model Training & Prediction
    if st.button("Train Model"):
        train_and_predict(df)

if __name__ == "__main__":
    run_app()
