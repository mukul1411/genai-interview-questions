# The two losses behind preference tuning, computed on one example.
import math

sigmoid = lambda z: 1 / (1 + math.exp(-z))

# 1) RLHF step 1: a reward model trained with the Bradley-Terry loss on a human preference pair.
r_chosen, r_rejected = 1.8, 0.6                   # reward model scores for preferred / dispreferred
bt_loss = -math.log(sigmoid(r_chosen - r_rejected))
print(f"Bradley-Terry: P(chosen > rejected) = {sigmoid(r_chosen - r_rejected):.3f}, loss = {bt_loss:.3f}")

# RLHF step 2 maximises reward minus a KL penalty that keeps the policy near the reference model.
reward, kl, beta = 1.8, 0.9, 0.1
print(f"PPO objective term: reward - beta*KL = {reward} - {beta}*{kl} = {reward - beta * kl:.2f}")

# 2) DPO skips the reward model: it uses log-prob ratios of policy vs reference directly.
logp_policy_c, logp_ref_c = -12.0, -13.0          # chosen response
logp_policy_r, logp_ref_r = -15.0, -14.0          # rejected response
beta = 0.1
margin = beta * ((logp_policy_c - logp_ref_c) - (logp_policy_r - logp_ref_r))
dpo_loss = -math.log(sigmoid(margin))
print(f"DPO: implicit reward margin = {margin:.2f}, loss = {dpo_loss:.3f} (falls as the policy prefers 'chosen')")
