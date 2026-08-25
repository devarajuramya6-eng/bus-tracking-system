"""
CityBus Enterprise Platform - Bi-Level Origin-Destination (OD) Matrix Inversion
File: backend/services/od_analytics/bilevel_od_inversion.py

Estimates passenger OD trip matrix from marginal stop APC boardings and alightings:
- Iterative Bi-Proportional Furness Balancing Algorithm (IPFP)
- Gravity model impedance decay f(d_ij) = exp(-beta * d_ij)
- Reconstructs commuter desire lines across corridor stops
"""

import math
from typing import List, Dict, Any


class BiLevelODInversion:
    @staticmethod
    def balance_od_matrix(boardings: List[int], alightings: List[int],
                          distance_matrix_km: List[List[float]],
                          beta_decay: float = 0.12, max_iterations: int = 25) -> List[List[float]]:
        """
        Estimates full N x N passenger trip matrix T_ij.
        """
        n = len(boardings)
        if n == 0 or len(alightings) != n:
            return []

        # Initialize base matrix with gravity deterrence
        matrix = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i < j: # Public transit travels in one forward direction along route
                    dist = distance_matrix_km[i][j] if i < len(distance_matrix_km) and j < len(distance_matrix_km[i]) else (j - i) * 2.0
                    deterrence = math.exp(-beta_decay * dist)
                    matrix[i][j] = float(boardings[i] * alightings[j]) * deterrence

        # Furness 2D balancing iterations
        for _ in range(max_iterations):
            # Row scaling (match boardings)
            for i in range(n):
                row_sum = sum(matrix[i])
                if row_sum > 0 and boardings[i] > 0:
                    scale = float(boardings[i]) / row_sum
                    for j in range(n):
                        matrix[i][j] *= scale

            # Column scaling (match alightings)
            for j in range(n):
                col_sum = sum(matrix[i][j] for i in range(n))
                if col_sum > 0 and alightings[j] > 0:
                    scale = float(alightings[j]) / col_sum
                    for i in range(n):
                        matrix[i][j] *= scale

        # Round values
        return [[round(matrix[i][j], 1) for j in range(n)] for i in range(n)]
