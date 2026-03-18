import random, math

def change(chance: float | int, dif: float | int, num: float, plus_chance: int | float = 0.5):
    if random.random() > chance: return num
    else:
        if plus_chance==0.5: res=eval(f"{num}{random.choice(("+", "-"))}{dif}")
        else:
            if random.random()<plus_chance: res=num+dif
            else: res=num-dif
    return float(res)

def percent(num: int | float, percents: int | float): return num*percents/100

def dif(a: int | float, b: int | float, percents: bool = True) -> float:
    diference = float(abs(a-b) / a*100) if percents else float(abs(a-b))
    return diference

def average(*values: int | float) -> float:
    num=0
    for val in values: num+=val
    return float(num/len(values))

def sigmoid(x, min_val: float | int = 0, max_val: float | int = 1):
        if x < -500: res = 0
        elif x > 500: res = 1
        else: res = 1 / (1 + math.exp(-x))
        return min_val + (res * (max_val - min_val))

def fact(x: int):
    res=0
    for i in range(x): res+=i
    return res