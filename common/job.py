import time
import multiprocessing as mp

def meas_run_time(func):
    def wrapper(*args, **kwargs):
        t_ini = time.time()
        result = func(*args, **kwargs)
        print(func.__name__, f'run time : {round(time.time() - t_ini, 1)}')
        return result
    return wrapper


def mult_run(func, inputs, n_mult=4):
    pool = mp.Pool(processes=n_mult)
    return list(pool.map(func, inputs))
    # pool.close()
    # pool.join()

