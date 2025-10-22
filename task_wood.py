import drone
import field

def plant_wood(_):
    plants = [Entities.Bush, Entities.Tree]
    index = field.get_pos_adjacency()
    field.plant_if_necessary(plants[index])

def make_wood_task(from_xy, to_xy):
    return drone.make_area_task({
        "from": from_xy,
        "to": to_xy,
        "task_fn": plant_wood
    })
