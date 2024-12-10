
def new_row(m, value):
    return np.full((1, m.shape[1]), value)

def new_column(m, value):
    return np.full((m.shape[0], 1), value)

def move_up(m, value):
    return np.pad(m[1:], ((0, 1), (0, 0)), constant_values=value)

def move_down(m, value):
    return np.pad(m[:-1], ((1, 0), (0, 0)), constant_values=value)

def move_left(m, value):
    return np.pad(m[:,1:], ((0, 0), (0, 1)), constant_values=value)

def move_right(m, value):
    return np.pad(m[:,:-1], ((0, 0), (1, 0)), constant_values=value)
