t = [11,2,3,4,562,1,213]

for i in range(len(t)):
    print(t[i])
    if i % 2 == 0:
        del t[i]
        
print(t)