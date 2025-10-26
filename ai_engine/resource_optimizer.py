"""
Resource Optimizer for Disaster Response
Optimal allocation of resources (ambulances, rescue teams, etc.)
Algorithms: K-Means clustering (for demand zones) + Hungarian Algorithm (assignment)
"""

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from scipy.optimize import linear_sum_assignment

class ResourceOptimizer:

    def cluster_incident_areas(self, incident_coords, n_zones):
        """
        Clusters incident locations into n_zones (using K-Means).
        Returns cluster centers and labels for each incident.
        """
        kmeans = KMeans(n_clusters=n_zones, random_state=42, n_init=10)
        labels = kmeans.fit_predict(incident_coords)
        centers = kmeans.cluster_centers_
        return centers, labels

    def assign_resources(self, resource_coords, demand_coords):
        """
        Assigns resources (ambulances, fire trucks) to demand sites using Hungarian Method.
        Input: resource_coords, demand_coords - arrays of (lat, lng)
        Output: List of assignments [(resource_index, demand_index)]
        """
        cost_matrix = np.linalg.norm(resource_coords[:, None, :] - demand_coords[None, :, :], axis=2)
        row_ind, col_ind = linear_sum_assignment(cost_matrix)
        assignments = list(zip(row_ind.tolist(), col_ind.tolist()))
        return assignments, cost_matrix[row_ind, col_ind]

    def simulate(self):
        """
        Demo: 8 incidents, 8 ambulances. Assign the closest ambulance to each incident zone.
        """
        # Random (lat, lng) for incidents and ambulances
        np.random.seed(0)
        incident_coords = np.random.uniform([28.5, 77.0], [28.8, 77.5], (8,2))
        ambulance_coords = np.random.uniform([28.5, 77.0], [28.8, 77.5], (8,2))
        
        print("\nIncident locations:\n", incident_coords)
        print("Ambulance locations:\n", ambulance_coords)
        
        # Do clustering (3 demand zones, for demo)
        centers, labels = self.cluster_incident_areas(incident_coords, n_zones=3)
        print("\nCluster centers (demand zones):\n", centers)

        # Optimal assignment
        assignments, costs = self.assign_resources(ambulance_coords, incident_coords)
        print("\nAssignments (Resource -> Incident):")
        for res_i, dem_i, cost in zip(*zip(*assignments), costs):
            print(f"Ambulance {res_i} → Incident {dem_i} | Distance: {cost:.4f}")

if __name__ == "__main__":
    optimizer = ResourceOptimizer()
    optimizer.simulate()
