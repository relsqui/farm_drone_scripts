hat_by_upgrade = {
    Unlocks.Grass: Hats.Green_Hat,
    Unlocks.Trees: Hats.Tree_Hat,
    Unlocks.Carrots: Hats.Carrot_Hat,
    Unlocks.Watering: Hats.Purple_Hat,
    Unlocks.Pumpkins: Hats.Pumpkin_Hat,
    Unlocks.Megafarm: Hats.Gray_Hat,
    Unlocks.Cactus: Hats.Cactus_Hat,
    Unlocks.Mazes: Hats.Gold_Hat
}

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

def set_hat_for_upgrade(upgrade):
  if upgrade in hat_by_upgrade:
    hat = hat_by_upgrade[upgrade]
    if hat in get_available_hats():
      change_hat(hat)
      return
  change_hat(Hats.Straw_Hat)  