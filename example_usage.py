from client import GroverSearchOptimizer

def main():
    print("=== Grover Quantum Search Optimizer ===")
    # 5 qubits = 32 item search space
    optimizer = GroverSearchOptimizer(num_qubits=5)
    secret_key = 23

    res = optimizer.search(lambda x: x == secret_key)
    print("Search Result:", res)
    assert res["best_candidate"] == secret_key
    assert res["candidate_is_valid"] is True
    assert res["success_probability"] > 0.95

    print("Grover Quantum Search Optimizer verified successfully!")

if __name__ == "__main__":
    main()
