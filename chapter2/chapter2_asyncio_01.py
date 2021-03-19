with open(__file__) as f:
    data = f.read()
# The program will block here until the data has been read
print(data)
