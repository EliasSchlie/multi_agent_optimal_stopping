import random
from models import House

def uniform_house_generator(n_houses: int = 20, min_quality: float = 1.0, max_quality: float = 10.0):
    """Generate houses with uniformly distributed quality scores."""
    def generator():
        houses = []
        for i in range(n_houses):
            quality = random.uniform(min_quality, max_quality)
            houses.append(House(f"house_{i+1}", quality))
        return houses
    return generator


def normal_house_generator(n_houses: int = 20, mean_quality: float = 5.5, std_quality: float = 2.0):
    """Generate houses with normally distributed quality scores."""
    def generator():
        houses = []
        for i in range(n_houses):
            quality = max(1.0, min(10.0, random.gauss(mean_quality, std_quality)))
            houses.append(House(f"house_{i+1}", quality))
        return houses
    return generator


def bimodal_house_generator(n_houses: int = 20, low_mean: float = 3.0, high_mean: float = 8.0, 
                           std: float = 1.0, high_prob: float = 0.3):
    """Generate houses with bimodal quality distribution (low and high quality markets)."""
    def generator():
        houses = []
        for i in range(n_houses):
            if random.random() < high_prob:
                quality = max(1.0, min(10.0, random.gauss(high_mean, std)))
            else:
                quality = max(1.0, min(10.0, random.gauss(low_mean, std)))
            houses.append(House(f"house_{i+1}", quality))
        return houses
    return generator
