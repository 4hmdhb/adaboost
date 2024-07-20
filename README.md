
---

# Machine Learning Projects

## Description

This repository contains the implementation of two key machine learning projects.

1. **Movie Recommender System**: A personalized movie recommendation system using Singular Value Decomposition (SVD) and Latent Factor Models (LFM).
2. **IM2SPAIN: Geo-location Prediction using k-NN**: A geo-location prediction system utilizing k-Nearest Neighbors (k-NN) to estimate the latitude and longitude of images based on their CLIP embeddings.

See "**solution_writeup.pdf**" for graphs and performance evalution. See "**hw7.pdf**" for project description.

## Deliverables

### Movie Recommender System

1. **Training the Model**:
    - Trained a personalized movie recommendation model using SVD and LFM.
    - Evaluated the model's performance using Mean Squared Error (MSE), training accuracy, and validation accuracy.

2. **Optimal Dimensionality Reduction**:
    - Determined the optimal number of dimensions \( d \) for feature vectors.
    - Compared training and validation accuracies for different values of \( d \).

### IM2SPAIN: Geo-location Prediction

1. **Data Visualization**:
    - Visualized image locations and applied Principal Component Analysis (PCA) to image features.

2. **k-NN Regression**:
    - Implemented k-NN regression to predict image geo-locations.
    - Evaluated the performance using Mean Displacement Error (MDE) and determine the optimal number of neighbors \( k \).

## Installation

To set up this project on your local machine, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone git@github.com:4hmdhb/adaboost.git
    cd adaboost
    ```

2. **Create and activate a virtual environment** (optional but recommended):
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```


## Usage

### Movie Recommender System

1. **Training the Model**:
    - Ensure the dataset is in the `movie_data/` directory with files `movie_train.mat` and `movie_validate.txt`.
    - Run the training script:
        ```bash
        python movie_recommender.py
        ```
    - This will produce the training MSE, training accuracy, and validation accuracy for various values of \( d \), and save the plots in the project directory.

2. **Model Evaluation**:
    - To evaluate the model on a new dataset or validate the results, run:
        ```bash
        python evaluate_recommender.py
        ```

### IM2SPAIN: Geo-location Prediction

1. **Visualize the Data**:
    - Plot the image locations and apply PCA to the image features:
        ```bash
        python im2spain_visualize.py
        ```

2. **Run k-NN for Geo-location Prediction**:
    - Modify the `im2spain_starter.py` script as needed and run:
        ```bash
        python im2spain_starter.py
        ```
    - This script will perform k-NN regression, plot the MDE vs. \( k \), and evaluate the performance.

---
