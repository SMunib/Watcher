import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Generate random coordinates (replace this with your coordinates)
num_coordinates = 100
coordinates = np.random.rand(num_coordinates, 2) * 10  # 2D coordinates in the range [0, 10)

# Plot the original coordinates
plt.figure(figsize=(8, 6))
plt.scatter(coordinates[:, 0], coordinates[:, 1], color='blue', label='Original')

# Apply K-means clustering
num_clusters = 3  # Specify the number of clusters
kmeans = KMeans(n_clusters=num_clusters)
kmeans.fit(coordinates)
print(coordinates)
cluster_centers = kmeans.cluster_centers_

# Plot the cluster centers
plt.scatter(cluster_centers[:, 0], cluster_centers[:, 1], color='red', marker='x', s=100, label='Cluster Centers')

# Plot the clustered points
for i in range(num_clusters):
    cluster_points = coordinates[kmeans.labels_ == i]
    plt.scatter(cluster_points[:, 0], cluster_points[:, 1], label=f'Cluster {i+1}')

plt.title('K-means Clustering')
plt.xlabel('X-coordinate')
plt.ylabel('Y-coordinate')
plt.legend()
plt.grid(True)
plt.show()
