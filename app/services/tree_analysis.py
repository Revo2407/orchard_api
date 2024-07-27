import pandas as pd
import numpy as np
from scipy.spatial import ConvexHull, distance_matrix
from shapely.geometry import Point, Polygon

def find_missing_tree_centroids(tree_data, grid_size=0.00002, group_threshold=0.00005, noise_threshold=0.00002):
    coordinates = tree_data[['lng', 'lat']].values
    hull = ConvexHull(coordinates)
    hull_points = coordinates[hull.vertices]
    hull_polygon = Polygon(hull_points)

    min_lng, max_lng = coordinates[:, 0].min(), coordinates[:, 0].max()
    min_lat, max_lat = coordinates[:, 1].min(), coordinates[:, 1].max()
    lng_grid = np.arange(min_lng, max_lng, grid_size)
    lat_grid = np.arange(min_lat, max_lat, grid_size)
    lng_grid, lat_grid = np.meshgrid(lng_grid, lat_grid)

    grid_points = np.vstack((lng_grid.ravel(), lat_grid.ravel())).T

    # Check which grid points are inside the boundary using Shapely
    inside_mask = np.array([hull_polygon.contains(Point(x, y)) for x, y in grid_points])
    inside_grid_points = grid_points[inside_mask]

    tree_positions = coordinates
    distances = distance_matrix(tree_positions, inside_grid_points)
    min_distances = distances.min(axis=0)
    no_tree_points = inside_grid_points[min_distances > group_threshold]

    missing_tree_distances = distance_matrix(no_tree_points, no_tree_points)
    centroids = []
    assigned = np.zeros(no_tree_points.shape[0], dtype=bool)

    for i in range(no_tree_points.shape[0]):
        if assigned[i]:
            continue
        nearby_indices = np.where(missing_tree_distances[i] < group_threshold)[0]
        if len(nearby_indices) > 1:
            centroid = no_tree_points[nearby_indices].mean(axis=0)
        else:
            centroid = no_tree_points[i]
        centroids.append(centroid)
        assigned[nearby_indices] = True

    centroids = np.array(centroids)
    centroid_distances = [hull_polygon.exterior.distance(Point(x, y)) for x, y in centroids]
    non_noise_centroids = centroids[np.array(centroid_distances) > noise_threshold]

    return non_noise_centroids
