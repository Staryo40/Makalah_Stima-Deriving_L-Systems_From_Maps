from util import *
from classes import *

data = os.path.join(os.getcwd(), "data", "bandung.json")

patterns = load_patterns_from_json(data)
plot_patterns(patterns, show_labels=False)
plt.show()