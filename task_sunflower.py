import drone
import field
import nav

def plant_sunflower(state):
    field.plant_if_necessary(Entities.Sunflower)
    petals = measure()  
    if petals not in state["sizes"]:
        state["sizes"][petals] = []
    state["sizes"][petals].append((get_pos_x(), get_pos_y()))

def harvest_sunflowers(state):
    # while num_items(Items.Power) < 3 * plan.min_required[Items.Power]:
    while len(state["sizes"]) > 0:
        max_petals = max(list(state["sizes"]))
        for pos in state["sizes"][max_petals]:
            x, y = pos
            nav.go_to(x, y)
            if not can_harvest():
                continue
            harvest()
            state["sizes"][max_petals].remove(pos)
            if len(state["sizes"][max_petals]) == 0:
                state["sizes"].pop(max_petals)
            # plant_sunflower(state)

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