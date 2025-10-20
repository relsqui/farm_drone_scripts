import field
import plan

def spawn_or_do(task):
  if num_drones() < max_drones():
    return spawn_drone(task)
  else:
    task()

def all_finished(drones):
    if drones == None:
        return False
    for drone in drones:
        if has_finished(drone):
            drones.remove(drone)
        else:
            return False
    return True

def await_all(drones):
  if drones == None:
    return
  for drone in drones:
    if drone:
      wait_for(drone)

def make_area_task(fn, x0, y0, x1, y1, args = []):
  def task():
    fn(x0, y0, x1, y1, args)
  return task

def make_column_task(fn):
  def task():
    start_y = get_pos_y()
    just_started = True
    while just_started == True or get_pos_y() != start_y:
      just_started = False
      fn()
      move(North)
  return task

def replant_task():
  harvest_task()
  field.plant_crop(plan.get_next_crop())

def harvest_task():
  if can_harvest():
    harvest()
