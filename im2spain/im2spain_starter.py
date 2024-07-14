"""
The goal of this assignment is to predict GPS coordinates from image features using k-Nearest Neighbors.
Specifically, have featurized 28616 geo-tagged images taken in Spain split into training and test sets (27.6k and 1k).

The assignment walks students through:
    * visualizing the data
    * implementing and evaluating a kNN regression model
    * analyzing model performance as a function of dataset size
    * comparing kNN against linear regression

Images were filtered from Mousselly-Sergieh et al. 2014 (https://dl.acm.org/doi/10.1145/2557642.2563673)
and scraped from Flickr in 2024. The image features were extracted using CLIP ViT-L/14@336px (https://openai.com/clip/).
"""

import matplotlib.pyplot as plt
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors


def plot_data(train_feats, train_labels):
    """
    Input:
        train_feats: Training set image features
        train_labels: Training set GPS (lat, lon)

    Output:
        Displays plot of image locations, and first two PCA dimensions vs longitude
    """
    # Plot image locations (use marker='.' for better visibility)
    plt.scatter(train_labels[:, 1], train_labels[:, 0], marker=".")
    plt.title('Image Locations')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.show()

    # Run PCA on training_feats
    ##### TODO(a): Your Code Here #####
    transformed_feats = StandardScaler().fit_transform(train_feats)
    transformed_feats = PCA(n_components=2).fit_transform(transformed_feats)

    # Plot images by first two PCA dimensions (use marker='.' for better visibility)
    plt.scatter(transformed_feats[:, 0],     # Select first column
                transformed_feats[:, 1],     # Select second column
                c=train_labels[:, 1],
                marker='.')
    plt.colorbar(label='Longitude')
    plt.title('Image Features by Longitude after PCA')
    plt.show()


def grid_search(train_features, train_labels, test_features, test_labels, is_weighted=False, verbose=True):
    knn = NearestNeighbors(n_neighbors=100).fit(train_features)
    if verbose:
        print(f'Running grid search for k (is_weighted={is_weighted})')
    ks = list(range(1, 11)) + [20, 30, 40, 50, 100]
    mean_errors = []

    for k in ks:
        distances, indices = knn.kneighbors(test_features, n_neighbors=k)
        errors = []
        for i, nearest in enumerate(indices):
            # Evaluate mean displacement error in miles for each test image
            # Assume 1 degree latitude is 69 miles and 1 degree longitude is 52 miles
            y = test_labels[i]
            if (is_weighted):
                weights = [1 / (a + 1e-8) for a in distances[i]]
                mean_lat = np.average(train_labels[nearest][:, 0], weights=weights)
                mean_lon = np.average(train_labels[nearest][:, 1], weights=weights)
            else:
                mean_lat = np.mean(train_labels[nearest][:, 0])
                mean_lon = np.mean(train_labels[nearest][:, 1])
            e = np.sqrt(((y[0] - mean_lat) * 69)**2 + ((y[1] - mean_lon)*52)**2)
            errors.append(e)
        e = np.mean(np.array(errors))
        mean_errors.append(e)
        if verbose:
            print(f'{k}-NN mean displacement error (miles): {e:.1f}')

    # Plot error vs k for k Nearest Neighbors
    if verbose:
        plt.plot(ks, mean_errors)
        plt.xlabel('k')
        plt.ylabel('Mean Displacement Error (miles)')
        plt.title('Mean Displacement Error (miles) vs. k in kNN')
        plt.show()
    return min(mean_errors)


def mean_dis_error(predictions, truth):
    displacements = predictions - truth
    displacements = np.array([((a[0] * 69)**2, (a[1] * 52)**2) for a in displacements ])
    displacements = np.sqrt(np.sum(displacements, axis=1))
    return np.mean(displacements)    


def main():
    print("Predicting GPS from CLIP image features\n")

    # Import Data
    print("Loading Data")
    data = np.load('im2spain_data.npz')

    train_features = data['train_features']  # [N_train, dim] array
    test_features = data['test_features']    # [N_test, dim] array
    train_labels = data['train_labels']      # [N_train, 2] array of (lat, lon) coords
    test_labels = data['test_labels']        # [N_test, 2] array of (lat, lon) coords
    train_files = data['train_files']        # [N_train] array of strings
    test_files = data['test_files']          # [N_test] array of strings

    # Data Information
    print('Train Data Count:', train_features.shape[0])

    # Part A: Feature and label visualization (modify plot_data method)
    plot_data(train_features, train_labels)

    # Part C: Find the 5 nearest neighbors of test image 53633239060.jpg
    knn = NearestNeighbors(n_neighbors=3).fit(train_features)

    # Use knn to get the k nearest neighbors of the features of image 53633239060.jpg
    ##### TODO(c): Your Code Here #####
    index = np.where(test_files == "53633239060.jpg")[0]
    distances, indices = knn.kneighbors([test_features[index[0]]])
    print(distances)
    print(train_files[indices])
    print("test coordinate: ", test_labels[index[0]])
    print("train coordinates: ", train_labels[indices])


    # Part D: establish a naive baseline of predicting the mean of the training set
    ##### TODO(d): Your Code Here #####
    
    centroid_lat = np.mean(train_labels[:, 0])
    centroid_lon = np.mean(train_labels[:, 1])
    predictions = np.array([(centroid_lat, centroid_lon)] * len(test_features))
    displacements = predictions - test_labels
    displacements = np.array([((a[0] * 69)**2, (a[1] * 52)**2) for a in displacements ])
    displacements = np.sqrt(np.sum(displacements, axis=1))
    mde = np.mean(displacements)
    print("Mean Displacement Error (Miles):", mde)


    # Part E: complete grid_search to find the best value of k
    grid_search(train_features, train_labels, test_features, test_labels)

    # Parts G: rerun grid search after modifications to find the best value of k
    grid_search(train_features, train_labels, test_features, test_labels, is_weighted=True)

    # Part H: compare to linear regression for different # of training points
    mean_errors_lin = []
    mean_errors_nn = []
    ratios = np.arange(0.1, 1.1, 0.1)
    for r in ratios:
        num_samples = int(r * len(train_features))
        ##### TODO(h): Your Code Here #####
        indices = np.random.choice(num_samples, size=num_samples, replace=False)

        train_f_sample = train_features[indices]
        train_l_sample = train_labels[indices]

        model = LinearRegression()
        model.fit(train_f_sample, train_l_sample)        

        y_pred = model.predict(test_features)
        e_lin = mean_dis_error(y_pred, test_labels)

        e_nn = grid_search(train_f_sample, train_l_sample, test_features, test_labels, verbose=False)

        mean_errors_lin.append(e_lin)
        mean_errors_nn.append(e_nn)

        print(f'\nTraining set ratio: {r} ({num_samples})')
        print(f'Linear Regression mean displacement error (miles): {e_lin:.1f}')
        print(f'kNN mean displacement error (miles): {e_nn:.1f}')

    # Plot error vs training set size
    plt.plot(ratios, mean_errors_lin, label='lin. reg.')
    plt.plot(ratios, mean_errors_nn, label='kNN')
    plt.xlabel('Training Set Ratio')
    plt.ylabel('Mean Displacement Error (miles)')
    plt.title('Mean Displacement Error (miles) vs. Training Set Ratio')
    plt.legend()
    plt.show()
       

if __name__ == '__main__':
    main()
