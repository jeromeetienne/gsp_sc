import time
import multiprocessing as mp
import matplotlib.pyplot as plt
import numpy as np


class AsyncPlotter:
    def __init__(self, processes=mp.cpu_count()):
        self.manager = mp.Manager()
        self.nc = self.manager.Value("i", 0)
        self.pids = []
        self.processes = processes

    def async_plotter(self, nc, fig, filename, processes):
        while nc.value >= processes:
            time.sleep(0.1)
        nc.value += 1
        fig.savefig(filename)
        plt.close(fig)
        nc.value -= 1

    def save(self, fig, filename):
        p = mp.Process(target=self.async_plotter, args=(self.nc, fig, filename, self.processes))
        p.start()
        self.pids.append(p)

    def join(self):
        for p in self.pids:
            p.join()


a = AsyncPlotter()

for i in range(5):
    fig = plt.figure()
    plt.plot(np.random.rand(10))
    a.save(fig, f"figure_{i}.png")

a.join()
