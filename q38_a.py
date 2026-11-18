# Speculative decoding, simulated: a cheap draft model proposes gamma tokens, the target verifies them.
import random

def simulate(alpha, gamma, steps=20000, seed=0):
    rng, produced = random.Random(seed), 0
    for _ in range(steps):                       # each step = one target-model forward pass
        accepted = 0
        while accepted < gamma and rng.random() < alpha:
            accepted += 1
        produced += accepted + 1                 # +1: target always yields one token (correction or bonus)
    return produced / steps

def expected(alpha, gamma):                      # Leviathan et al. (2023)
    return (1 - alpha ** (gamma + 1)) / (1 - alpha)

for alpha in [0.6, 0.8]:
    for gamma in [2, 4, 6]:
        print(f"alpha={alpha} gamma={gamma}: tokens per target pass simulated {simulate(alpha, gamma):.2f}"
              f" vs formula {expected(alpha, gamma):.2f}")
print("\nOutput distribution is unchanged: rejected draft tokens are resampled from the target model.")
