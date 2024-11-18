import ibis
ibis.options.interactive = True

def load_data(path : str, files : list[str])-> ibis.:

    frames = []

    for file in files:
        frames.append(df.read_csv(path + file))

    

    return df
