
import re
import collections

lines = [line.strip() for line in open("input-16-test.txt")]
#lines = [line.strip() for line in open("input-16.txt")]

class Valve:
    def __init__(self, name, flow, neighbors):
        self.name = name
        self.flow = flow
        self.neighbors = neighbors

# Parse and find AA.
aa = None
valves = {}
for line in lines:
    # Valve HH has flow rate=22; tunnel leads to valve GG
    name, flow, *neighbors = re.findall(r'([A-Z][A-Z]|[0-9]+)', line)
    v = Valve(name, int(flow), neighbors)
    if name == "AA":
        aa = v
    valves[name] = v

# Breadth-first search to find the distance from start_name to all other
# nodes that have non-zero flow.
def get_dist(start_name):
    q = collections.deque([(start_name, 0)])
    d = {}
    while q:
        name, dist = q.popleft()
        neighbors = valves[name].neighbors
        for n in neighbors:
            if n not in d:
                d[n] = dist + 1
                q.append((n, dist + 1))

    # Don't include ourselves.
    del d[start_name]

    # Remove zero-flow valves.
    d = {n: d for n, d in d.items() if valves[n].flow > 0}

    return d

# Precompute distance to every other flowable node.
dists = {}
for name in valves:
    dists[name] = get_dist(name)

# Find the pressure from this point.
# players is 2-element array of players, each being a room name.
#    The function will move players[0].
# opened is a set of players of opened valves.
# time_left is the number of minutes left.
# other_left is the number of minutes that players[1] has left
#    in their current step. This is 0 if they are available
#    to move right away.
def get_pressure(players, opened, time_left, other_left):
    # Can't do anything in this little time, since you'd
    # have to move somewhere and open a valve.
    if time_left <= 2:
        return 0

    # Working on the first player.
    player = players[0]

    # The best pressure we can find.
    pressure = 0

    # Try all possible valves we can reach from here.
    for next_room, dist in dists[player].items():
        # Only go to open valves, and only to valves we can reach in time.
        if next_room not in opened and dist + 1 < time_left:
            # Open the valve.
            opened.add(next_room)
            # Add this valve's pressure for the remainder of the time.
            new_pressure = (time_left - dist - 1)*valves[next_room].flow
            # And decrease time for the distance and the opening of the valve.
            new_time_left = time_left - dist - 1
            # See how much time players[1] has left on their move *after* our move.
            new_other_left = other_left - dist - 1
            if new_other_left >= 0:
                # players[1] has time left, so we recurse normally and get players[0] to
                # move again.
                new_names = [next_room, players[1]]
            else:
                # players[1] will run out of time on their move before our move finishes,
                # so we have to move them first. Swap the players so that the cursion
                # moves players[1].
                new_names = [players[1], next_room]
                # Compute how much time will be left for players[0], since we're not
                # doing their entire move right now.
                new_other_left = -new_other_left
                # We decreased the time left too much and encroached into the other
                # player's time. Fix that.
                new_time_left += new_other_left

            p = new_pressure + get_pressure(new_names, opened, new_time_left, new_other_left)
            if p > pressure:
                pressure = p

            # Undo opening the valve.
            opened.remove(next_room)

    return pressure

#pressure = get_pressure([aa.name, aa.name], set(), 30, 100)
pressure = get_pressure([aa.name, aa.name], set(), 26, 0)
print(pressure)

