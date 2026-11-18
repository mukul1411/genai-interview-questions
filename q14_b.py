# When does fine-tuning pay for itself versus long few-shot prompts? A back-of-envelope model.
# All prices are illustrative placeholders; substitute your provider's current rates.
calls_per_month = 2_000_000
price_in_per_mtok = 1.00            # USD per million input tokens (base model)
price_in_ft_per_mtok = 1.50         # fine-tuned models often cost more per token
task_tokens = 300
few_shot_tokens = 1_500             # the examples you'd no longer need after fine-tuning
fine_tune_one_off = 5_000           # training + data labelling + evaluation effort

few_shot_monthly = calls_per_month * (task_tokens + few_shot_tokens) / 1e6 * price_in_per_mtok
fine_tuned_monthly = calls_per_month * task_tokens / 1e6 * price_in_ft_per_mtok
saving = few_shot_monthly - fine_tuned_monthly
print(f"few-shot  : ${few_shot_monthly:>10,.0f} / month")
print(f"fine-tuned: ${fine_tuned_monthly:>10,.0f} / month  (+ ${fine_tune_one_off:,} one-off)")
print(f"payback   : {fine_tune_one_off / saving:.1f} months" if saving > 0 else "never pays back")
