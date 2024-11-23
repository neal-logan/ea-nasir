import ibis
ibis.options.interactive = True

def load_data_local(path : str, files : list[str])-> ibis.:

    frames = []

    for file in files:
        frames.append(df.read_csv(path + file))

    

    return df



def load_data_remote()