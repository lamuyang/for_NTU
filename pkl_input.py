def open_pkl(pkl):
    import pickle
    with open(f"{pkl}", 'rb') as fp:
        sorted = pickle.load(fp)
    fp.close()
    return sorted
