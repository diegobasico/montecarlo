# %%
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng()
h = plt.hist(rng.triangular(-3, 0, 8, 100000), bins=200,
             density=False)
plt.show()
