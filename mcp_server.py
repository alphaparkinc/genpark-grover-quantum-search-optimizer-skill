import sys
import json
from client import GroverSearchOptimizer

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    if method == "search_key":
        qubits = params.get("num_qubits", 4)
        target = params.get("target", 7)
        opt = GroverSearchOptimizer(qubits)
        return opt.search(lambda x: x == target)
    return {"error": "Unknown method"}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        req = json.loads(line)
        res = handle_request(req)
        print(json.dumps(res))
        sys.stdout.flush()

if __name__ == "__main__":
    main()
