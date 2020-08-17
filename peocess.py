import numpy as np

data = [4,7,5,4,6,5,6]

mean1 = np.mean(data)
std1 = np.std(data)

red = (mean1 - std1, mean1 + std1)
green = (mean1 - std1 * 2, mean1 + std1 * 2)

print(f"mean1= {mean1}, std1= {std1}, red={red}, green= {green}")