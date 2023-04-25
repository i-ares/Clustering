# -*- coding: utf-8 -*-
"""20269_Assignment.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JOyRVHMni1MUxW5U0VbsFhOysuRJqU2X
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import csv
import sys
import seaborn as sns
from sklearn import metrics
from sklearn.metrics import silhouette_score
import scipy.cluster.hierarchy as shc
from sklearn.preprocessing import StandardScaler, normalize
import warnings
warnings.filterwarnings("ignore")

X = pd.read_csv('data.csv', delimiter=',',header = None, names = ['A','B'])
X

# Plotting the data
colors = ['yellow', 'black']
colormap = mpl.colors.ListedColormap(colors)
plt.scatter(X.A, X.B, cmap = colormap, s=10)

from sklearn.cluster import KMeans
# Using elbow method we are determining the optimal cluster number
wcss = []
scores = []



kmeans = KMeans(n_clusters = 2,
                  init = 'k-means++',
                  max_iter = 500,
                  n_init ='auto',
                  random_state = 0)
kmeans.fit(X)
  
score = silhouette_score(X, kmeans.labels_)
print("\nNumber of clusters =", 2)
print("Silhouette score = %.5f"%score)
scores.append(score)
wcss.append(kmeans.inertia_)
num_clusters = np.argmax(scores) + values[0]

"""KMeans"""

kmeans = KMeans(n_clusters = 2,            # Set amount of clusters
                init = 'k-means++',        # Initialization method for kmeans
                max_iter = 400,            # Maximum number of iterations
                n_init = 10,               # Choose how often algorithm will run with different centroid 
                random_state = 0)          # Choose random state for reproducibility

y_kmeans = kmeans.fit_predict(X)
y_kmeans

# Plotting the clusters
X = np.array(X)
plt.scatter(X[y_kmeans==0, 0], X[y_kmeans==0, 1], s=8, c='yellow', label ='Cluster 1')
plt.scatter(X[y_kmeans==1, 0], X[y_kmeans==1, 1], s=8, c='black', label ='Cluster 2')

# Plot the clusters centroids
plt.scatter(kmeans.cluster_centers_[:,0],
            kmeans.cluster_centers_[:,1],
            s = 100,                       # S implies the set centroid size
            c = 'black')                   # c implies the set centroid color
plt.title('KMeans')
plt.show()
kmeans.cluster_centers_

kmeans.predict([[0,0],[12,3]])

"""GaussianMixture"""

from sklearn.mixture import GaussianMixture
import numpy as np

n_components = np.arange(1,21)

models = [GaussianMixture(n, covariance_type = 'full', random_state = 0).fit(X) for n in n_components]
plt.plot(n_components, [m.bic(X) for m in models], label = 'BIC')
plt.plot(n_components, [m.aic(X) for m in models], label = 'AIC')
plt.legend(loc = 'best')
plt.xlabel('n_components');
plt.show()

gmm = GaussianMixture(n_components = 2)
gmm.fit(X)

labels = gmm.predict(X)
score = silhouette_score(X, labels)
print("Silhouette score = %.5f"%score)
scores.append(score)
plt.scatter(X[:, 0], X[:, 1], c = labels, cmap = 'inferno', s = 10)
plt.title('GMM')
plt.show()

"""Agglomerative Clustering"""

from sklearn.cluster import AgglomerativeClustering

plt.title('Visualising the data')
# Dendrogram = shc.dendrogram((shc.linkage(X,method = 'complete')))

ac = AgglomerativeClustering(n_clusters = 2, affinity = 'manhattan', memory = None,
                              compute_full_tree='auto', linkage= 'average', distance_threshold=None, compute_distances=False)
# visualizing the clustering

plt.scatter(X[:, 0], X[:, 1], c = ac.fit_predict(X), cmap = 'plasma', s = 8)
plt.title('Agglomerative Clustering')
plt.show()
labels= ac.labels_
score = silhouette_score(X, labels)
print("Silhouette score = %.5f"%score)
scores.append(score)

"""Spectral Clustering"""

from sklearn.cluster import SpectralClustering

# Preprocessing the data to make it visualizable
# Scaling the Data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

#Normalizing the Data
X_normalized = normalize(X_scaled)

# Converting the numpy array into a pandas DataFrame
X_normalized = pd.DataFrame(X_normalized)

# Building the clustering model
spectral_model_rbf = SpectralClustering(n_clusters=2, eigen_solver=None, n_components=None, 
                                         random_state=None, n_init=10, gamma=1.0, affinity='rbf', 
                                         n_neighbors=100, eigen_tol=0.0, assign_labels='kmeans', degree=3, 
                                         coef0=1, kernel_params=None, n_jobs=None, verbose=False)
  
# Training the model and Storing the predicted cluster labels
labels_rbf = spectral_model_rbf.fit_predict(X_normalized)

# Plotting the clustered scatter plot
  
plt.scatter(X[:,0], X[:,1], c=labels_rbf, s=8)
plt.title('Spectral clustering')
#plt.legend(('Label 0', 'Label 1'))
plt.show()
score = silhouette_score(X, labels_rbf)
print("Silhouette score = %.5f"%score)
scores.append(score)

import sys
np.set_printoptions(threshold = sys.maxsize)
from sklearn.cluster import DBSCAN
df=X.values
y_pred = DBSCAN(eps = 0.3, min_samples = 300).fit(X)
labels = y_pred.labels_
core_samples_mask = np.zeros_like(y_pred.labels_, dtype=bool)
core_samples_mask[y_pred.core_sample_indices_] = True
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
print('Number of clusters', n_clusters_)

no_clusters = len(np.unique(labels))
no_noise = np.sum(np.array(labels) == -1, axis=0)

from sklearn import cluster
dbscan = cluster.DBSCAN(eps=0.3, min_samples=300)
clustering_labels = dbscan.fit_predict(df)
plt.scatter(X["A"], X["B"], c=clustering_labels, s=8)
plt.title('DBscan clustering')
#plt.legend(('Label 0', 'Label 1'))
plt.show()

unique_labels = set(labels)
colors = ['y', 'b', 'g', 'r']

for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        # col = 'k'
        continue
  
    class_member_mask = (labels == k)
  
    xy = df[class_member_mask & core_samples_mask]
    
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
             markeredgecolor='k',
             markersize=6)
  
    xy = X[class_member_mask & ~core_samples_mask]
    plt.plot(xy.iloc[:, 0], xy.iloc[:, 1], 'o', markerfacecolor=col,
             markeredgecolor='k',
             markersize=6)
y_predicted = np.array([i for i in labels if i != -1])
plt.title('number of clusters: %d' % n_clusters_)
plt.show()

X['labels'] = clustering_labels
score = metrics.silhouette_score(X, X['labels'])
print(score)

# List of Silhouette Scores
print("List of Silhoutte Scores: \n")
scores

cl1=np.savetxt("kmeans_labels.txt", y_kmeans, fmt="%d")
cl2=np.savetxt("DBscan_labels.txt", y_predicted,fmt="%d")

#np.savetxt("20269_Soham_Bhar_MLAssignment2_labels.txt", all,fmt="%d",delimiter =',')

from google.colab import files
files.download('kmeans_labels.txt')
files.download('DBscan_labels.txt')

