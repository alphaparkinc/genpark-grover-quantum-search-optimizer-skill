import math

class GroverSearchOptimizer:
    """Grover quantum amplitude amplification search optimizer."""
    def __init__(self, num_qubits: int):
        self.num_qubits = num_qubits
        self.n = 1 << num_qubits

    def search(self, target_predicate, max_iterations: int = None) -> dict:
        """
        target_predicate: callable(index) -> bool returning True if item is a target.
        """
        # Find actual marked targets to calculate exact optimal rotation
        marked_targets = [i for i in range(self.n) if target_predicate(i)]
        M = len(marked_targets)
        if M == 0:
            return {"error": "No target states satisfy predicate", "found": None}
        if M == self.n:
            return {"found": 0, "iterations": 0, "success_prob": 1.0}

        theta = math.asin(math.sqrt(M / self.n))
        optimal_iters = int(round((math.pi / (4.0 * theta)) - 0.5)) if theta > 0 else 0
        iters = optimal_iters if max_iterations is None else max_iterations

        # Initialize uniform superposition
        state = [1.0 / math.sqrt(self.n)] * self.n
        history = []

        for step in range(iters):
            # 1. Oracle Phase Inversion
            for i in range(self.n):
                if target_predicate(i):
                    state[i] = -state[i]

            # 2. Diffusion Operator (Inversion about the mean)
            mean_amp = sum(state) / self.n
            for i in range(self.n):
                state[i] = 2.0 * mean_amp - state[i]

            # Track peak probability
            prob_target = sum(abs(state[t]) ** 2 for t in marked_targets)
            history.append(round(prob_target, 4))

        best_index = max(range(self.n), key=lambda i: abs(state[i]) ** 2)
        success_probability = sum(abs(state[t]) ** 2 for t in marked_targets)

        return {
            "num_qubits": self.num_qubits,
            "database_size": self.n,
            "target_count": M,
            "iterations_performed": iters,
            "best_candidate": best_index,
            "candidate_is_valid": target_predicate(best_index),
            "success_probability": round(success_probability, 4),
            "amplitude_progression": history[:5]
        }
