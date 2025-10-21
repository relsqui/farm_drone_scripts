import drone
import field
import nav
import plan

def plant_sunflower(state):
    field.plant_if_necessary(Entities.Sunflower)
    petals = measure()  
    if petals not in state["sizes"]:
        state["sizes"][petals] = []
    state["sizes"][petals].append((get_pos_x(), get_pos_y()))

def harvest_sunflowers(state):
    while num_items(Items.Power) < 2 * plan.min_required[Items.Power]:
        max_petals = max(list(state["sizes"]))
        x, y = state["sizes"][max_petals][0]
        nav.go_to(x, y)
        while not can_harvest():
            pass
        harvest()
        plant_sunflower(state)

def make_sunflower_task(from_xy, to_xy):
    return drone.make_area_task({
        "from": from_xy,
        "to": to_xy,
        "task_fn": plant_sunflower,
        "end_fn": harvest_sunflowers,
        "state": {
            "sizes": {}
        }
    })