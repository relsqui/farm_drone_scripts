import pumpkin
import upgrade

min_required = {
  Items.Carrot: 1000,
  Items.Hay: 1000,
  Items.Wood: 1000,
  Items.Power: 100
}

item_priority = [Items.Hay, Items.Wood, Items.Carrot, Items.Power]

producer = {
  Items.Carrot: Entities.Carrot,
  Items.Hay: Entities.Grass,
  Items.Power: Entities.Sunflower,
  Items.Cactus: Entities.Cactus
}

def get_missing_requirements():
  missing = []
  for item in item_priority:
    if item in min_required and num_items(item) < min_required[item]:
      missing.append(item)
  return missing

def get_needed_product():
  required_items = get_missing_requirements()
  if len(required_items) > 0:
    return required_items[0]

  min_stock = None
  min_item = None
  required_only = [Items.Power]
  next_upgrade_cost = upgrade.get_next_upgrade_cost()
  for item in item_priority:
    stock = num_items(item)
    if item in next_upgrade_cost and stock < next_upgrade_cost[item]:
      return item
    if item in required_only:
      # Skip things we don't arbitrarily stock when not collecting them
      continue
    if min_stock == None or stock < min_stock:
      # Then return whatever we have least of
      min_stock = stock
      min_item = item
  return min_item

def get_next_crop():
  x, y = get_pos_x(), get_pos_y()
  needed_product = get_needed_product()

  if pumpkin.in_pumpkin_zone(x, y):
    return Entities.Pumpkin
  elif needed_product == Items.Wood:
    if (x % 2) + (y % 2) == 1:
      return Entities.Tree
    else:
      return Entities.Bush
  return producer[needed_product]
