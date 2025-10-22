import upgrade

# How much buffer do we want to keep in stock?
# (How much can we burn through between product checks)
min_required = {
  Items.Carrot: 1000,
  Items.Hay: 1000,
  Items.Wood: 1000,
  Items.Power: 200
}

# Stock some up before we go burning it on mazes
preferred_power = 1000

# Prioritize stocking basics first to enable the rest
item_priority = [Items.Power, Items.Hay, Items.Wood, Items.Carrot]

def get_missing_requirements():
  missing = []
  for item in item_priority:
    if item in min_required and num_items(item) < min_required[item]:
      missing.append(item)
  return missing

def get_priorities():
  products = get_missing_requirements()
  for product in upgrade.get_next_upgrade_cost():
    if product not in products:
      products.append(product)
  for product in sort_keys_by_value(upgrade.get_all_missing_products()):
    if product not in products:
      products.append(product)
  return products

def sort_keys_by_value(d):
  values = []
  keys = []
  for k in d:
    values.append(d[k])
  while len(values) > 0:
    for k in d:
      if len(values) > 0 and d[k] == min(values):
        keys.append(k)
        values.remove(d[k])
  return keys
