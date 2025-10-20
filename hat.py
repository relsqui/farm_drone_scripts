def get_available_hats():
  available_hats = []
  for hat in list(Hats):
    if num_unlocked(hat) == 1:
      available_hats.append(hat)
  return available_hats

previous_hat = None
def randomize_hat():
  hats = get_available_hats()
  global previous_hat
  hat = previous_hat
  while hat == previous_hat:
    hat = hats[(random() * len(hats)) // 1]
  change_hat(hat)
  previous_hat = hat
