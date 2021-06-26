import random, string
from datetime import datetime
codes = []
start = datetime.now()
print("script started at :",start)
for i in range(100000):
    code = "".join(random.choice(string.hexdigits) for _ in range(6))
    print("code:",code)
    codes.append(code)

repeated = 0
for i in range(len(codes)):
    if codes[i] in codes[i+1:]:
        repeated += 1
        print("code repeated:",codes[i])    
end = datetime.now()
print("total codes length:",len(codes))
print("total repeated:",repeated)

print("script ended at:",end,"|total time taken:",end-start)