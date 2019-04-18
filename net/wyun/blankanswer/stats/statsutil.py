import numpy as np
from scipy import stats

def print_stats(my_list):
    lst = map(int, my_list)
    np_a = np.asarray(lst)
    print 'max:', max(lst), ', mean: ', sum(lst) / len(lst), ', min: ', min(lst), \
        ', 98%: ', np.percentile(np_a, 98), ', 50%: ', np.percentile(np_a, 50)
