import hat

desired_upgrades = [
  Unlocks.Grass,
  Unlocks.Trees,
  Unlocks.Carrots,
  Unlocks.Watering,
  Unlocks.Pumpkins,
  Unlocks.Megafarm,
  Unlocks.Cactus,
  Unlocks.Mazes
]

def get_upgrade_costs():
    costs = {}
    for upgrade in desired_upgrades:
        cost = get_cost(upgrade)
        if len(cost) != 0:
            costs[upgrade] = cost
    return costs

def remaining_item_cost(cost):
    sum = 0
    for item in cost:
        sum += max(0, cost[item] - num_items(item))
    return sum

def get_all_missing_products():
    products = {}
    costs = get_upgrade_costs()
    for upgrade in costs:
        for product in costs[upgrade]:
            missing = max(0, costs[upgrade][product] - num_items(product))
            if missing:
                if product in products:
                    products[product] = min(products[product], missing)
                else:
                    products[product] = missing
    return products

def get_next_upgrade_cost():
    costs = get_upgrade_costs()
    next_upgrade = None
    items_needed = 0
    for upgrade in costs:
        remaining_cost = remaining_item_cost(costs[upgrade])
        if next_upgrade == None or remaining_cost < items_needed:
            next_upgrade = upgrade
            items_needed = remaining_cost
    hat.set_hat_for_upgrade(next_upgrade)
    return costs[next_upgrade]

def can_afford(cost):
    if cost == None:
        return False
    for item in cost:
        if num_items(item) < cost[item]:
            return False
    return True

def check_upgrades():
    costs = get_upgrade_costs()
    for upgrade in costs:
        if can_afford(costs[upgrade]):
            unlock(upgrade)
            print("Unlocked", upgrade)
            do_a_flip()