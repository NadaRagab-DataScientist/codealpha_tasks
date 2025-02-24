# -*- coding: utf-8 -*-
"""Iris_Project(Task1).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1y5nCrTs2tEwdvKkqSLE4MwtbzZytIEmM

**Step 1: Define the Problem**

You need to create a machine learning model that can classify the species of iris flowers (Setosa, Versicolor, and Virginica) based on their physical measurements, such as sepal length, sepal width, petal length, and petal width.

**Step 2: Data Collection**

**Step 3: Data Exploration (Exploratory Data Analysis - EDA)**

**Step 1: Install Required Libraries**

**Task: Iris Flower Classification using Machine Learning :**

The Iris flower dataset contains measurements of iris flowers, classified into three species: Setosa, Versicolor, and Virginica. The dataset includes four features for each flower:
1.	Sepal Length
2.	Sepal Width
3.	Petal Length
4.	Petal Width

Goal is to build a machine learning model that can classify these flowers based on their measurements.
"""

!pip install dash

"""**Step 2: Import Necessary Libraries**"""

import dash
from dash import dcc, html
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go
from dash.dependencies import Input, Output

import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

"""**Step 3: Load the Iris Dataset**"""

from google.colab import drive
drive.mount('/content/drive')

# Load the Iris dataset from a CSV file
df = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/Iris.csv')  # Make sure to update the file path

# Display the first Five rows of the DataFrame
df.head()

df.info()

df.shape

# Summary statistics
df.describe()

# Check for missing values
df.isnull().sum()

"""**Step 4: Data Visualization For Numerical Columns**

**4.1 Pairplot: Visualize relationships between all features colored by species**
"""

sns.pairplot(df, hue='Species', palette='deep')
plt.suptitle('Pairplot of Iris Dataset', y=1.02, fontsize=16, fontweight='bold')
plt.show()

"""**4.2 Correlation Heatmap: Visualize correlations between features**

"""

plt.figure(figsize=(8, 6))
sns.heatmap(df.drop('Species', axis=1).corr(), annot=True, cmap='coolwarm', vmin=-1, vmax=1, linewidths=0.5)    # drop Species(object) from Hearmap(For Number Columns)
plt.title('Correlation Heatmap of Features', fontsize=16, fontweight='bold')
plt.show()

"""**4.3 Histograms: Visualize distributions of each feature**"""

# Drop the 'Species' column as it's categorical and not relevant for histograms
df_features = df.drop('Species', axis=1)

# Create a color palette with as many colors as there are features
colors = sns.color_palette("Set2", n_colors=len(df_features.columns))

# Create a figure with enough space for all the subplots (5 histograms in total)
fig, axes = plt.subplots(len(df_features.columns), 1, figsize=(8, 16))  # 5 rows, 1 column grid

# Loop through each feature and create a subplot for each
for i, feature in enumerate(df_features.columns):
    axes[i].hist(df_features[feature], bins=20, color=colors[i], edgecolor='black', alpha=0.7)  # Plot histogram
    axes[i].set_title(f'Histogram of {feature}', fontsize=14, fontweight='bold')  # Title for each subplot
    axes[i].set_xlabel(feature)  # Label x-axis
    axes[i].set_ylabel('Frequency')  # Label y-axis
    axes[i].grid(True)  # Add grid lines

# Adjust layout to ensure the subplots are spaced properly
plt.tight_layout()

# Display the plot
plt.show()

"""**4.4 Boxplot: Visualize the distribution of each feature by species**"""

# List of features to create boxplots for (excluding 'species')
features = df.drop('Species', axis=1).columns  # These are the 4 features excluding 'species'

# Create a 2x2 grid for subplots (since there are 4 features)
fig, axes = plt.subplots(3, 2, figsize=(14, 10))  # 2 rows, 2 columns

# Create a list of colors for each feature
colors = sns.color_palette("Set2", n_colors=len(features))

# Loop through each feature and plot in a separate subplot
for i, feature in enumerate(features):
    ax = axes.flatten()[i]  # Use flat indexing to access the subplots
    sns.boxplot(x=df[feature], palette=[colors[i]], ax=ax)  # Plot the boxplot
    ax.set_title(f'Boxplot of {feature}', fontsize=14, fontweight='bold')  # Set title
    ax.set_xlabel(feature)  # Set x-axis label
    ax.set_ylabel('Values')  # Set y-axis label

# Adjust layout for better spacing
plt.tight_layout()

# Display the plot
plt.show()

"""**4.5 Violin Plot: Compare distributions of features by species**"""

plt.figure(figsize=(12, 8))
sns.violinplot(x='Species', y='SepalLengthCm', data=df, palette='pastel')
plt.title('Violin Plot of Sepal Length by Species', fontsize=16, fontweight='bold')
plt.show()

"""**4.6 Data Visualization For Categorical Columns**"""

# 1. Use value_counts() to count occurrences of each category
species_count = df['Species'].value_counts()
print(species_count)  # Print the value counts to check

# 2. Create a subplot grid (2 rows, 1 column) for count plot and pie chart
fig, axes = plt.subplots(2, 1, figsize=(8, 12))

# 3. Count Plot (top subplot)
sns.countplot(data=df, x='Species', palette='viridis', ax=axes[0])  # Use 'viridis' color palette for count plot
axes[0].set_title('Count Plot of Iris Species', fontsize=16, fontweight='bold')
axes[0].set_xlabel('Species')
axes[0].set_ylabel('Count')

# 4. Pie Chart (bottom subplot) with slicing
explode = (0.1, 0, 0)  # Slicing the first slice to make it stand out (exploded)
colors = sns.color_palette('Set1', n_colors=len(species_count))  # Using a different color palette for the pie chart
species_count.plot.pie(autopct='%1.1f%%', colors=colors, ax=axes[1], explode=explode, startangle=90, legend=False)
axes[1].set_title('Pie Chart of Iris Species Distribution', fontsize=16, fontweight='bold')
axes[1].set_ylabel('')  # Hide the y-axis label for the pie chart

# Adjust layout to ensure proper spacing between subplots
plt.tight_layout()

# Display the plots
plt.show()

"""**Step 4: Data Cleaning**

**1. Remove Duplicates**
"""

# Check for duplicates
duplicates = df[df.duplicated()]
print(f"Duplicate rows: \n{duplicates}")

# Drop duplicate rows if found
df = df.drop_duplicates()

"""**2. Handle Missing Values and Drop irrevlant columns with dataset**"""

# Check for missing values
print(df.isnull().sum())

# Drop the 'Id' column from the DataFrame
df = df.drop('Id', axis=1)

# Verify that the 'Id' column is removed
df.head()

"""**3. Handle Outliers**"""

# Step 1: Define a function to handle outliers using IQR (removing outliers)
def handle_outliers_remove(df):
    # Loop over numerical columns
    for column in df.select_dtypes(include=['float64']).columns:
        # Calculate Q1 (25th percentile) and Q3 (75th percentile)
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1

        # Define outlier thresholds
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        # Remove rows where values are outside the IQR range
        df = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

    return df

# Step 2: Visualize the boxplots after handling outliers
def visualize_boxplots_after(df, title="Boxplots of Features After Handling Outliers"):
    # Create a color palette
    colors = sns.color_palette("Set2", len(df.select_dtypes(include=['float64', 'int64']).columns))

    # Set up subplots for each numerical feature
    num_cols = len(df.select_dtypes(include=['float64']).columns)
    n_rows = (num_cols + 1) // 2  # Calculate the number of rows needed for subplots
    plt.figure(figsize=(12, 8))

    for i, column in enumerate(df.select_dtypes(include=['float64']).columns):
        plt.subplot(n_rows, 2, i+1)  # Adjust the grid dynamically
        sns.boxplot(x=df[column], color=colors[i])  # Plot the boxplot with different colors
        plt.title(f'Boxplot of {column}', fontsize=14, fontweight='bold')
        plt.grid(True)

    plt.tight_layout()
    plt.suptitle(title, fontsize=16, fontweight='bold', y=1.02)  # Add a title for all subplots
    plt.show()

# Step 3: Apply the function to remove outliers
df= handle_outliers_remove(df)

# Step 4: Visualize the boxplots after handling outliers
visualize_boxplots_after(df, title="Boxplots After Handling Outliers")

# Step 5: Check if outliers are removed ( prints first 5 rows)
print(df.head())

"""**4. Encoding Categorical Data**"""

# Initialize the encoder
encoder = LabelEncoder()

# Encode the 'species' column into numeric labels
df['species_encoded'] = encoder.fit_transform(df['Species'])

# Verify that the 'species' column is dropped and 'species_encoded' is present
df.head()

"""**Step 4: Data Preprocessing (Feature Scaling and Train-Test Split)**"""

# Separate features (X) and target (y)
X = df.drop(columns=['Species', 'species_encoded'])  # Drop species columns for X
y = df['species_encoded']  # Target variable

# Standardize the features using StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split the data into training and testing sets (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

"""**Step 5: Model Selection and Training (Using Logistic Regression):**"""

# Initialize the Logistic Regression model
model = LogisticRegression(max_iter=200)

# Train the model on the training data
model.fit(X_train, y_train)

# Make predictions on the test data
y_pred = model.predict(X_test)

"""**Step 5:Model Evaluation**"""

# Evaluate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')

# Print classification report (precision, recall, F1 score)
print(classification_report(y_test, y_pred, target_names=encoder.classes_))

# Print confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)
print(f'Confusion Matrix:\n{conf_matrix}')

"""**Step 6: Model Optimization(Hyperparameter Tuning with Grid Search)**"""

# Example: Tuning hyperparameters for Logistic Regression
param_grid = {'C': [0.1, 1, 10], 'solver': ['liblinear', 'lbfgs']}
grid_search = GridSearchCV(LogisticRegression(), param_grid, cv=5)

# Fit grid search
grid_search.fit(X_train, y_train)

# Display best parameters from grid search
print("Best parameters:", grid_search.best_params_)

# Evaluate the best model
best_model = grid_search.best_estimator_
y_pred_best = best_model.predict(X_test)

# Evaluate the best model performance
accuracy_best = accuracy_score(y_test, y_pred_best)
print(f'Best Model Accuracy: {accuracy_best:.2f}')

"""**Other Models (SVM, Random Forest)**"""

# Train SVM Model
svm_model = SVC(kernel='linear')
svm_model.fit(X_train, y_train)
y_pred_svm = svm_model.predict(X_test)
print(f"SVM Accuracy: {accuracy_score(y_test, y_pred_svm):.4f}")

# Train Random Forest Model
rf_model = RandomForestClassifier(n_estimators=100)
rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)
print(f"Random Forest Accuracy: {accuracy_score(y_test, y_pred_rf):.4f}")

"""**Step 7: Final Model Evaluation**"""

# Final Model (Example: Logistic Regression after hyperparameter tuning)
final_model = grid_search.best_estimator_

# Predict on the test set
y_pred_final = final_model.predict(X_test)

# Evaluate final model
print("Final Model Accuracy: ", accuracy_score(y_test, y_pred_final))

"""**Step 8: Create Dash Layout with Graphs**"""

# Create the Dash application
app = dash.Dash(__name__)

# Create interactive visualizations
# 1. Pairplot using Plotly
fig_pairplot = px.scatter_matrix(df, dimensions=["SepalLengthCm", "SepalWidthCm",
                                                 "PetalLengthCm", "PetalWidthCm"],
                                 color="Species", title="Pairplot of Iris Dataset")

# 2. Confusion Matrix Heatmap
fig_conf_matrix = go.Figure(data=go.Heatmap(z=conf_matrix,
                                            x=['setosa', 'versicolor', 'virginica'],
                                            y=['setosa', 'versicolor', 'virginica'],
                                            colorscale='Viridis'))
fig_conf_matrix.update_layout(title="Confusion Matrix", xaxis_title="Predicted", yaxis_title="Actual")

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1("Iris Flower Classification", style={'textAlign': 'center'}),

    # Pairplot visualization
    html.Div([
        dcc.Graph(figure=fig_pairplot)
    ], style={'width': '50%', 'display': 'inline-block'}),

    # Confusion matrix visualization
    html.Div([
        dcc.Graph(figure=fig_conf_matrix)
    ], style={'width': '50%', 'display': 'inline-block'}),

    # Add more visualizations here
])

if __name__ == "__main__":
    app.run_server(debug=True)