import json, advmilp as A, sys
roles = [{'kind': 'min', 'cls': i} for i in range(3)] + [{'kind': 'vert', 'z': z} for z in range(3)]
st, msg, sol = A.run(roles)
print(st, msg); print(json.dumps(sol))
