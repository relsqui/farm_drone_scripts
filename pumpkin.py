pumpkin_margin = 4

def in_pumpkin_zone(x, y):
    return False
    min_pumpkin = pumpkin_margin
    max_pumpkin = get_world_size() - pumpkin_margin - 1
    if (x >= min_pumpkin and x <= max_pumpkin and y >= min_pumpkin and y <= max_pumpkin):
        return True
    return False

def maybe_harvest_pumpkin(seen_so_far):
    expected_pumpkins = (get_world_size() - (2 * pumpkin_margin)) ** 2
    seen_so_far += 1
    if seen_so_far == expected_pumpkins or not in_pumpkin_zone(get_pos_x(), get_pos_y()):
        harvest()
        seen_so_far = 0
    return seen_so_far