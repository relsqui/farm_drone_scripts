def maybe_harvest_sunflower(current_sizes):
  petals = measure()
  if len(current_sizes) == 0 or len(current_sizes) > 10 or petals >= max(current_sizes) or num_items(Items.Power) == 0:
    harvest()
    if petals in current_sizes:
      current_sizes.remove(petals)
  return current_sizes