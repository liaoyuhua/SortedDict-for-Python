from sorted_dict import SortedDict


if __name__ == "__main__":
    sd = SortedDict(by="key") # or by="value"
    sd[1] = 10
    sd[2] = 2
    sd[3] = 3
    sd[4] = 9
    sd[5] = 5

    print(sd)
    print(sd.keys())
    print(sd.values())
    print(sd.items()) 
