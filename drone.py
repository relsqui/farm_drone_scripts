import field
import plan
import nav

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

def make_area_task(x0, y0, x1, y1, fn, initial_state = {}):
  # currently x0, y0 should be NW of x1, y1
  def task():
    state = initial_state
    dir = East
    goal = {East: x1, West: x0}
    nav.go_to(x0, y0)
    while get_pos_y() <= y1:
      while get_pos_x() != goal[dir]:
        state = fn(state)
        move(dir)
      dir = nav.opposite[dir]
      move(South)
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
