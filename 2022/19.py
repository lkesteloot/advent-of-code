
import re

lines = [line.strip() for line in open("input-19-test.txt")]
lines = [line.strip() for line in open("input-19.txt")]

part1 = False

total = 0 if part1 else 1
for line in lines:
    blueprint_id, ore_robot_ore_cost, clay_robot_ore_cost, obs_robot_ore_cost, obs_robot_clay_cost, geode_robot_ore_cost, geode_robot_obs_cost = map(int, re.findall(r'([0-9]+)', line))

    max_ore = max(ore_robot_ore_cost, clay_robot_ore_cost, obs_robot_ore_cost, geode_robot_ore_cost)

    cache = {}

    # Returns number of geodes.
    def f(minute, ore, clay, obs, geode, ore_robot, clay_robot, obs_robot, geode_robot):
        global cache

        if minute == 0:
            #print(ore, clay, obs, geode, "/", ore_robot, clay_robot, obs_robot, geode_robot)
            return geode

        if minute == 1:
            return geode + geode_robot

        key = (minute, ore, clay, obs, geode, ore_robot, clay_robot, obs_robot, geode_robot)
        p = cache.get(key)
        if p is not None:
            return p

        best_geode = 0

        # This "if" is in general a bad heuristic, but happens to work for part 2.
        if part1 or ore < max_ore:
            g = f(minute - 1,
                  ore + ore_robot,
                  clay + clay_robot,
                  obs + obs_robot,
                  geode + geode_robot,
                  ore_robot,
                  clay_robot,
                  obs_robot,
                  geode_robot)
            best_geode = max(best_geode, g)

        if ore >= ore_robot_ore_cost:
            g = f(minute - 1,
                  ore - ore_robot_ore_cost + ore_robot,
                  clay + clay_robot,
                  obs + obs_robot,
                  geode + geode_robot,
                  ore_robot + 1,
                  clay_robot,
                  obs_robot,
                  geode_robot)
            best_geode = max(best_geode, g)

        if ore >= clay_robot_ore_cost:
            g = f(minute - 1,
                  ore - clay_robot_ore_cost + ore_robot,
                  clay + clay_robot,
                  obs + obs_robot,
                  geode + geode_robot,
                  ore_robot,
                  clay_robot + 1,
                  obs_robot,
                  geode_robot)
            best_geode = max(best_geode, g)

        if ore >= obs_robot_ore_cost and clay >= obs_robot_clay_cost:
            g = f(minute - 1,
                  ore - obs_robot_ore_cost + ore_robot,
                  clay - obs_robot_clay_cost + clay_robot,
                  obs + obs_robot,
                  geode + geode_robot,
                  ore_robot,
                  clay_robot,
                  obs_robot + 1,
                  geode_robot)
            best_geode = max(best_geode, g)

        if ore >= geode_robot_ore_cost and obs >= geode_robot_obs_cost:
            g = f(minute - 1,
                  ore - geode_robot_ore_cost + ore_robot,
                  clay + clay_robot,
                  obs - geode_robot_obs_cost + obs_robot,
                  geode + geode_robot,
                  ore_robot,
                  clay_robot,
                  obs_robot,
                  geode_robot + 1)
            best_geode = max(best_geode, g)

        cache[key] = best_geode
        return best_geode

    ore = 0
    clay = 0
    obs = 0
    geode = 0
    ore_robot = 1
    clay_robot = 0
    obs_robot = 0
    geode_robot = 0

    minutes = 24 if part1 else 32
    geode = f(minutes, ore, clay, obs, geode, ore_robot, clay_robot, obs_robot, geode_robot)
    print(blueprint_id, geode)

    if part1:
        total += geode*blueprint_id
    else:
        total *= geode
    if not part1 and blueprint_id == 3:
        break

print(total)
