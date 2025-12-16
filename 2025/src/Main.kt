import java.io.File
import java.util.PriorityQueue
import kotlin.math.abs
import kotlin.math.max
import kotlin.math.min
import kotlin.time.measureTimedValue

enum class Part { ONE, TWO }

fun myAssert(assertion: Boolean) {
    if (!assertion) {
        throw AssertionError()
    }
}

fun <T> MutableSet<T>.removeFirst(): T {
    val iterator = this.iterator()
    if (iterator.hasNext()) {
        return iterator.next().also { iterator.remove() }
    }
    throw NoSuchElementException("set is not empty")
}

data class ShortestPath<NODE>(val cost: Double, val path: List<NODE>)

// Dijkstra's shortest path.
fun <NODE> shortestPath(startNode: NODE,
                        isEndNode: (node: NODE) -> Boolean,
                        getNeighbors: (node: NODE) -> Collection<NODE>,
                        getCost: (node1: NODE, node2: NODE) -> Double): ShortestPath<NODE> {

    data class CostNode(val cost: Double, val node: NODE) : Comparable<CostNode> {
        override fun compareTo(other: CostNode): Int = cost.compareTo(other.cost)
    }

    val leftToVisit = PriorityQueue<CostNode>()
    val visitedNodes = mutableSetOf<NODE>()
    val costToStart = mutableMapOf<NODE, Double>()
    val back = mutableMapOf<NODE, NODE>()

    costToStart[startNode] = 0.0
    leftToVisit.add(CostNode(0.0, startNode))

    // Keep pulling from the priority queue until we get a node we've not processed.
    fun getNextCostNode(): CostNode {
        while (true) {
            if (leftToVisit.isEmpty()) {
                throw AssertionError("no path to end node")
            }
            val costNode = leftToVisit.remove()
            if (costNode.node !in visitedNodes) {
                return costNode
            }
        }
    }

    // Create a path from the start node to the end node (inclusive).
    fun makePath(endNode: NODE): List<NODE> {
        val path = mutableListOf<NODE>()
        var node = endNode
        path.add(node)
        while (node != startNode) {
            node = back.getValue(node)
            path.add(node)
        }
        return path.reversed()
    }

    while (true) {
        val (_, node) = getNextCostNode()
        if (isEndNode(node)) {
            return ShortestPath(costToStart.getValue(node), makePath(node))
        }

        val neighbors = getNeighbors(node)
        val costToUs = costToStart.getValue(node)
        for (neighbor in neighbors) {
            if (neighbor !in visitedNodes) {
                val costFromUsToNeighbor = getCost(node, neighbor)
                val costToNeighbor = costToStart[neighbor]
                val costToNeighborThroughUs = costToUs + costFromUsToNeighbor
                if (costToNeighbor == null || costToNeighborThroughUs < costToNeighbor) {
                    costToStart[neighbor] = costToNeighborThroughUs
                    leftToVisit.add(CostNode(costToNeighborThroughUs, neighbor))
                    back[neighbor] = node
                }
            }
        }
    }
}

// A* finds a path from start to goal.
// h is the heuristic function. h(n) estimates the cost to reach goal from node n.
// weight is actual distance between two nodes.
fun <NODE> aStarSearch(start: NODE,
                       goal: NODE,
                       getHeuristic: (node: NODE, goal: NODE) -> Double,
                       getNeighbors: (node: NODE) -> Collection<NODE>,
                       getCost: (node1: NODE, node2: NODE) -> Double): ShortestPath<NODE> {

    data class CostNode(val cost: Double, val node: NODE) : Comparable<CostNode> {
        override fun compareTo(other: CostNode): Int = cost.compareTo(other.cost)
    }

    // For node n, cameFrom[n] is the node immediately preceding it on the cheapest path from the start
    // to n currently known.
    val cameFrom = mutableMapOf<NODE,NODE>()

    // For node n, gScore[n] is the currently known cost of the cheapest path from start to n.
    val gScore = mutableMapOf<NODE,Double>().withDefault { Double.MAX_VALUE }
    gScore[start] = 0.0

    // For node n, fScore[n] = gScore[n] + h(n). fScore[n] represents our current best guess as to
    // how cheap a path could be from start to finish if it goes through n.
    val fScore = mutableMapOf<NODE,Double>().withDefault { Double.MAX_VALUE }
    fScore[start] = getHeuristic(start, goal)

    // The set of discovered nodes that may need to be (re-)expanded.
    // Initially, only the start node is known.
    // This is usually implemented as a min-heap or priority queue rather than a hash-set.
    val openSet = PriorityQueue<CostNode>()
    openSet.add(CostNode(fScore.getValue(start), start))

    val processed = mutableSetOf<NODE>()

    while (!openSet.isEmpty()) {
        var current = openSet.remove().node
        if (current == goal) {
            val totalPath = mutableListOf(current)
            var cost = 0.0
            while (current in cameFrom) {
                val from = cameFrom.getValue(current)
                cost += getCost(from, current)
                current = from
                totalPath.add(current)
            }
            return ShortestPath(cost, totalPath.reversed())
        }

        if (current in processed) {
            continue
        }
        processed.add(current)

        for (neighbor in getNeighbors(current)) {
            // weight(current,neighbor) is the weight of the edge from current to neighbor
            // tentative_gScore is the distance from start to the neighbor through current
            val tentativeGScore = gScore.getValue(current) + getCost(current, neighbor)
            if (tentativeGScore < gScore.getValue(neighbor)) {
                // This path to neighbor is better than any previous one. Record it!
                cameFrom[neighbor] = current
                gScore[neighbor] = tentativeGScore
                fScore[neighbor] = tentativeGScore + getHeuristic(neighbor, goal)
                openSet.add(CostNode(fScore.getValue(neighbor), neighbor))
            }
        }
    }

    // Open set is empty but goal was never reached.
    throw Error("goal not reachable")
}


fun day1(lines: List<String>, part: Part): Long {
    var pos = 50
    var count = 0L
    for (line in lines) {
        val direction = line[0]
        val distance = line.drop(1).toInt()
        val step = if (direction == 'R') 1 else -1

        when (part) {
            Part.ONE -> {
                pos = Math.floorMod(pos + step*distance, 100)
                if (pos == 0) {
                    count += 1
                }
            }

            Part.TWO -> {
                repeat (distance) {
                    pos = Math.floorMod(pos + step, 100)
                    if (pos == 0) {
                        count += 1
                    }
                }
            }
        }
    }

    return count
}

fun day2(lines: List<String>, part: Part): Long {
    var result = 0L

    val invalidIds = mutableSetOf<Long>()

    fun tryRange(first: String, last: String) {
        assert(first.length == last.length)
        if (part == Part.ONE && first.length % 2 != 0) {
            return
        }
        val firstValue = first.toLong()
        val lastValue = last.toLong()
        val halfLength = last.length / 2
        val lenRange = (if (part == Part.ONE) halfLength else 1)..halfLength
        for (len in lenRange) {
            var counter = first.take(len).toLong()
            val repeat = if (part == Part.ONE) 2 else first.length / len
            while (true) {
                val id = counter.toString().repeat(repeat).toLong()
                if (id > lastValue) {
                    break
                }
                if (id >= firstValue && !invalidIds.contains(id)) {
                    invalidIds.add(id)
                    result += id
                }
                counter += 1
            }
        }
    }

    lines[0].split(',').forEach { range ->
        val (first, last) = range.split('-')
        when (first.length) {
            last.length -> tryRange(first, last)
            last.length - 1 -> {
                tryRange(first, "9".repeat(first.length))
                tryRange("1" + "0".repeat(last.length - 1), last)
            }
            else -> throw Exception()
        }
    }

    return result
}

fun day3(lines: List<String>, part: Part): Long {
    var result = 0L
    val batteryCount = if (part == Part.ONE) 2 else 12

    for (line in lines) {
        var joltage = 0L
        var batteries = line

        repeat (batteryCount) { batteryIndex ->
            val digitsAfterThis = batteryCount - batteryIndex - 1
            val digit = batteries.take(batteries.length - digitsAfterThis).max()
            val digitIndex = batteries.indexOf(digit)
            batteries = batteries.drop(digitIndex + 1)
            joltage = joltage*10 + (digit - '0')
        }

        result += joltage
    }

    return result
}

fun day4(lines: List<String>, part: Part): Long {
    var result = 0L

    val rows = lines.size
    val cols = lines[0].length
    val rowRange = 0 until rows
    val colRange = 0 until cols
    val accessibleRange = 0..3

    data class Pos(val row: Int, val col: Int) {
        fun hasRoll() =
            row in rowRange && col in colRange && lines[row][col] == '@'

        fun neighbors() = listOf(
            Pos(row - 1, col - 1),
            Pos(row, col - 1),
            Pos(row + 1, col - 1),
            Pos(row - 1, col),
            Pos(row + 1, col),
            Pos(row - 1, col + 1),
            Pos(row, col + 1),
            Pos(row + 1, col + 1)
        )
    }

    val posToNeighbors = mutableMapOf<Pos, MutableSet<Pos>>()
    val accessiblePositions = mutableSetOf<Pos>()

    for (row in rowRange) {
        for (col in colRange) {
            val pos = Pos(row, col)
            if (pos.hasRoll()) {
                val neighbors = pos.neighbors()
                    .filter(Pos::hasRoll)
                    .toMutableSet()
                posToNeighbors[pos] = neighbors
                if (neighbors.size in accessibleRange) {
                    accessiblePositions.add(pos)
                }
            }
        }
    }

    when (part) {
        Part.ONE -> result = accessiblePositions.size.toLong()
        Part.TWO -> {
            while (!accessiblePositions.isEmpty()) {
                val toProcess = accessiblePositions.toSet()
                accessiblePositions.clear()
                toProcess.forEach { posToRemove ->
                    posToNeighbors.getValue(posToRemove).forEach { neighbor ->
                        val neighborNeighbors = posToNeighbors.getValue(neighbor)
                        myAssert(neighborNeighbors.remove(posToRemove))
                        if (neighborNeighbors.size in accessibleRange && neighbor !in toProcess) {
                            accessiblePositions.add(neighbor)
                        }
                    }
                    posToNeighbors.remove(posToRemove)
                    result += 1
                }
            }
        }
    }

    return result
}

fun day5(lines: List<String>, part: Part): Long {
    var result: Long

    // Load ranges.
    val blankIndex = lines.indexOf("")
    val overlappingRanges = lines.take(blankIndex)
        .map { line ->
            val (low, high) = line.split('-').map { it.toLong() }
            low..high
        }
        .sortedBy { it.first }
        .toMutableList()

    // Make them non-overlapping.
    val ranges = mutableListOf<LongRange>()
    for (i in overlappingRanges.indices) {
        val current = overlappingRanges[i]
        val next = overlappingRanges.getOrNull(i + 1)
        if (next == null || current.last < next.first) {
            ranges.add(current)
        } else {
            overlappingRanges[i + 1] = current.first..max(current.last,next.last)
        }
    }

    when (part) {
        Part.ONE -> {
            result = lines.drop(blankIndex + 1)
                .map { it.toLong() }
                .count { id ->
                    val index = ranges.binarySearch { range ->
                        when {
                            range.last < id -> -1
                            range.first > id -> 1
                            else -> 0
                        }
                    }
                    index >= 0
                }
                .toLong()
        }

        Part.TWO -> result = ranges.sumOf { it.last - it.first + 1 }
    }

    return result
}

fun day6(lines: List<String>, part: Part): Long {
    var result = 0L

    when (part) {
        Part.ONE -> {
            val spaces = " +".toRegex()
            val numbers = lines.take(lines.size - 1).map { it.trim().split(spaces).map { it.toLong() } }
            val ops = lines[lines.size - 1].trim().split(spaces)
            val problemCount = numbers[0].size

            result = (0 until problemCount).sumOf { index ->
                when (ops[index]) {
                    "+" -> numbers.sumOf { line -> line[index] }
                    "*" -> numbers.fold(1L) { product, line -> product * line[index] }
                    else -> throw Error()
                }
            }
        }

        Part.TWO -> {
            val columnCount = lines[0].length
            myAssert(lines.all { it.length == columnCount })
            val rowCount = lines.size - 1
            val ops = lines[lines.size - 1]
            val numbers = mutableListOf<Long>()
            for (i in columnCount - 1 downTo 0) {
                val s = (0 until rowCount)
                    .joinToString("") { j -> lines[j][i].toString() }
                    .trim()
                if (!s.isEmpty()) {
                    numbers.add(s.toLong())
                }
                if (ops[i] != ' ') {
                    result += when (ops[i]) {
                        '+' -> numbers.sum()
                        '*' -> numbers.reduce(Long::times)
                        else -> throw Error()
                    }
                    numbers.clear()
                }
            }
        }
    }

    return result
}

fun day7(lines: List<String>, part: Part): Long {
    val width = lines[0].length

    var tach = List(width) { index -> if (lines[0][index] == 'S') 1L else 0L }
    var splitCount = 0L

    for (line in lines) {
        val newTach = MutableList(width) { 0L }
        for (i in 0 until width) {
            if (tach[i] > 0) {
                if (line[i] == '^') {
                    splitCount += 1
                    if (i > 0) {
                        newTach[i - 1] += tach[i]
                    }
                    if (i < width - 1) {
                        newTach[i + 1] += tach[i]
                    }
                } else {
                    newTach[i] += tach[i]
                }
            }
        }
        tach = newTach
    }

    return when (part) {
        Part.ONE -> splitCount
        Part.TWO -> tach.sum()
    }
}

fun day8(lines: List<String>, part: Part): Long {
    data class Box(val x: Long, val y: Long, val z: Long, var parent: Box?, var size: Int)
    data class Pair(val b1: Box, val b2: Box, val dist: Long)

    val boxes = lines.map { line ->
        val (x, y, z) = line.split(',').map(String::toLong)
        Box(x, y, z, null, 1)
    }

    // https://en.wikipedia.org/wiki/Disjoint-set_data_structure
    fun rootOf(box: Box): Box {
        var root = box
        while (true) {
            val parent = root.parent ?: break
            root = parent
        }

        var walk = box
        while (true) {
            val parent = walk.parent ?: break
            walk.parent = root
            walk = parent
        }

        return root
    }

    fun merge(b1: Box, b2: Box) {
        // Find roots.
        var x = rootOf(b1)
        var y = rootOf(b2)
        if (x == y) {
            // x and y are already in the same set.
            return
        }

        // If necessary, swap variables to ensure that
        // x has at least as many descendants as y.
        if (x.size < y.size) {
            val tmp = x
            x = y
            y = tmp
        }

        y.parent = x
        x.size += y.size
    }

    val pairs = mutableListOf<Pair>()
    for (i in 0 until boxes.size - 1) {
        val bi = boxes[i]
        for (j in i + 1 until boxes.size) {
            val bj = boxes[j]
            val dx = bi.x - bj.x
            val dy = bi.y - bj.y
            val dz = bi.z - bj.z
            pairs.add(Pair(bi, bj, dx*dx + dy*dy + dz*dz))
        }
    }
    pairs.sortBy { pair -> pair.dist }

    when (part) {
        Part.ONE -> {
            val connectionCount = if (boxes.size < 100) 10 else 1000
            pairs.take(connectionCount).forEach { pair ->
                merge(pair.b1, pair.b2)
            }

            return boxes
                .map(::rootOf)
                .toSet()
                .sortedBy { box -> -box.size }
                .take(3)
                .fold(1) { product, box -> product*box.size }
                .toLong()
        }

        Part.TWO -> {
            pairs.forEach { pair ->
                merge(pair.b1, pair.b2)
                if (rootOf(pair.b1).size == boxes.size) {
                    return pair.b1.x*pair.b2.x
                }
            }
            val pair = pairs.last()
            return pair.b1.x*pair.b2.x
        }
    }
}

fun day9(lines: List<String>, part: Part): Long {
    data class Tile(val x: Int, val y: Int)
    data class Axis(val b2s: Map<Int,Int>, val size: Int)

    fun remapAxis(x: List<Int>): Axis {
        val b2s = mutableMapOf<Int,Int>()

        val sx = x.toSet().sorted()
        var small = 0
        for (i in sx.indices) {
            small += when {
                i == 0 -> 0
                sx[i] == sx[i - 1] + 1 -> 1
                else -> 2
            }
            b2s[sx[i]] = small
        }

        return Axis(b2s, small + 1)
    }

    val tiles = lines
        .map { line ->
            val (x, y) = line.split(",").map { it.toInt() }
            Tile(x, y)
        }

    var largestArea = 0L

    when (part) {
        Part.ONE -> {
            for (i in 0 until tiles.size - 1) {
                val ti = tiles[i]
                for (j in i + 1 until tiles.size) {
                    val tj = tiles[j]

                    val area = (abs(ti.x - tj.x) + 1).toLong()*(abs(ti.y - tj.y) + 1)
                    largestArea = max(largestArea, area)
                }
            }
        }

        Part.TWO -> {
            // Remap to a small grid size.
            val xAxis = remapAxis(tiles.map { it.x })
            val yAxis = remapAxis(tiles.map { it.y })
            fun b2sTile(tile: Tile): Tile = Tile(
                xAxis.b2s.getValue(tile.x),
                yAxis.b2s.getValue(tile.y)
            )

            // Make an empty grid.
            val grid = Array(yAxis.size) { BooleanArray(xAxis.size) }
            val gridXRange = 0 until xAxis.size
            val gridYRange = 0 until yAxis.size
            // Draw the outline.
            for (i in tiles.indices) {
                val j = (i + 1) % tiles.size
                val ti = b2sTile(tiles[i])
                val tj = b2sTile(tiles[j])
                if (ti.x == tj.x) {
                    for (y in min(ti.y, tj.y)..max(ti.y, tj.y)) {
                        grid[y][ti.x] = true
                    }
                } else {
                    for (x in min(ti.x, tj.x)..max(ti.x, tj.x)) {
                        grid[ti.y][x] = true
                    }
                }
            }
            // Flood fill the inside.
            val startTile = if (tiles.size < 100) Tile(1, 3) else Tile(200, 200)
            val floodSet = mutableSetOf(startTile)
            fun exploreTile(x: Int, y: Int) {
                if (x in gridXRange && y in gridYRange && !grid[y][x]) {
                    grid[y][x] = true
                    floodSet.add(Tile(x, y))
                }
            }
            while (!floodSet.isEmpty()) {
                val tile = floodSet.removeFirst()
                exploreTile(tile.x - 1, tile.y)
                exploreTile(tile.x + 1, tile.y)
                exploreTile(tile.x, tile.y - 1)
                exploreTile(tile.x, tile.y + 1)
            }
            // Make a list of spans for each row.
            val spansList = grid.map { row ->
                val spans = mutableListOf<IntRange>()
                var x = 0
                while (true) {
                    // Skip outside.
                    while (x < row.size && !row[x]) {
                        x += 1
                    }
                    if (x == row.size) {
                        break
                    }
                    val first = x
                    // Skip inside.
                    while (x < row.size && row[x]) {
                        x += 1
                    }
                    spans.add(first until x)
                }
                spans
            }
            // Whether a rectangle is valid in the small space.
            fun validRectangle(ti: Tile, tj: Tile): Boolean {
                val x1 = min(ti.x, tj.x)
                val x2 = max(ti.x, tj.x)
                val y1 = min(ti.y, tj.y)
                val y2 = max(ti.y, tj.y)
                for (y in y1..y2) {
                    val spans = spansList[y]
                    for (span in spans) {
                        if (span.first > x1 || span.last < x2) {
                            return false
                        }
                    }
                }
                return true
            }
            // Try all rectangles, rejecting the invalid ones.
            for (i in 0 until tiles.size - 1) {
                val ti = tiles[i]
                for (j in i + 1 until tiles.size) {
                    val tj = tiles[j]

                    val area = (abs(ti.x - tj.x) + 1).toLong() * (abs(ti.y - tj.y) + 1)
                    if (area >= largestArea) {
                        if (validRectangle(b2sTile(ti), b2sTile(tj))) {
                            largestArea = area
                        }
                    }
                }
            }
        }
    }

    return largestArea
}

@JvmInline
value class Joltages(val values: List<Int>) {
    val size get() = values.size
    operator fun plus(o: Joltages) = values.zip(o.values).map { (a, b) -> a + b }.toJoltages()
    operator fun minus(o: Joltages) = values.zip(o.values).map { (a, b) -> a - b }.toJoltages()
    operator fun div(o: Int) = values.map { it / o }.toJoltages()
}

fun List<Int>.toJoltages() = Joltages(this)

fun day10(lines: List<String>, part: Part): Long {
    data class Machine(
        val lights: Int,
        val buttonLights: List<Int>,
        val buttonJoltages: List<Joltages>,
        val joltages: Joltages
    )

    fun <E> List<E>.clipEnds() = drop(1).dropLast(1)
    fun String.clipEnds() = drop(1).dropLast(1)

    // [...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
    val machines = lines
        .map { line ->
            val parts = line.split(" ")
            val targetLights = parts[0]
                .clipEnds()
                .mapIndexed { index, ch -> if (ch == '#') 1 shl index else 0 }
                .sum()
            val joltage = parts.last()
                .clipEnds()
                .split(',')
                .map(String::toInt)
                .toJoltages()
            val buttonJoltage = parts
                .clipEnds()
                .map { button ->
                    val indices = button
                        .clipEnds()
                        .split(',')
                        .map(String::toInt)
                    List(joltage.size) { index -> if (index in indices) 1 else 0 }.toJoltages()
                }
            val buttonLights = buttonJoltage
                .map { button -> button.values
                    .mapIndexed { index, value -> value shl index }
                    .sum()
                }
            Machine(targetLights, buttonLights, buttonJoltage, joltage)
        }

    fun fewestButtonPressesForLights(machine: Machine): Long {
        val result = shortestPath(0,
            { lights -> lights == machine.lights },
            { lights -> machine.buttonLights.map { toggleLights -> lights xor toggleLights }},
            { _, _ -> 1.0 })
        return result.cost.toLong()
    }

    fun fewestButtonPressesForJoltages(machine: Machine): Long {
        val joltageCount = machine.joltages.size
        val buttonCount = machine.buttonLights.size
        val zeroJoltages = List(joltageCount) { 0 }.toJoltages()

        // Pre-compute map from desired least-significant bits to [Joltage,Button Press Count]
        // array (in the form of a map so we can look them up by Joltage easily).
        val lsbToJoltages = mutableMapOf<Int, MutableMap<Joltages, Int>>()
        val lsbCount = 1 shl buttonCount
        for (lsb in 0..<lsbCount) {
            var joltages = zeroJoltages
            var lights = 0
            var pressCount = 0
            for (buttonIndex in 0..<buttonCount) {
                if (((1 shl buttonIndex) and lsb) != 0) {
                    lights = lights xor machine.buttonLights[buttonIndex]
                    joltages += machine.buttonJoltages[buttonIndex]
                    pressCount += 1
                }
            }

            // Add to list of ways to get this LSB pattern.
            val list = lsbToJoltages.getOrPut(lights) { mutableMapOf() }
            // If the same joltages can be used to get this LSB, keep the one with the fewest button presses.
            val existingPressCount = list[joltages]
            if (existingPressCount == null || pressCount < existingPressCount) {
                list[joltages] = pressCount
            }
        }

        // Memoize f().
        val fCache = mutableMapOf<Joltages, Double>()
        lateinit var f: (Joltages) -> Double
        fun fImpl(targetJoltages: Joltages): Double {
            if (targetJoltages.values.all { it == 0 }) {
                return 0.0
            }
            val lsb = targetJoltages.values
                .mapIndexed { index, value -> (value and 1) shl index }
                .sum()

            var minPresses = Double.POSITIVE_INFINITY
            if (lsb in lsbToJoltages) {
                for ((joltages, pressCount) in lsbToJoltages.getValue(lsb)) {
                    val remainingJoltages = targetJoltages - joltages
                    if (remainingJoltages.values.all { it >= 0 }) {
                        minPresses = min(minPresses, 2 * f(remainingJoltages / 2) + pressCount)
                    }
                }
            }

            return minPresses
        }
        f = { targetJoltages -> fCache.getOrPut(targetJoltages) { fImpl(targetJoltages) } }

        return f(machine.joltages).toLong()
    }

    return when (part) {
        Part.ONE -> machines.sumOf { fewestButtonPressesForLights(it) }
        Part.TWO -> machines.sumOf { fewestButtonPressesForJoltages(it) }
    }
}

fun day11(lines: List<String>, part: Part): Long {
    data class Device(val name: String, val outputs: List<String>)
    data class Counts(val all: Long, val dac: Long, val fft: Long, val both: Long) {
        operator fun plus(other: Counts): Counts =
            Counts(all + other.all, dac + other.dac, fft + other.fft, both + other.both)
    }

    val devices = lines
        .map { line ->
            // ccc: ddd eee fff
            val (name, outputString) = line.split(": ")
            val outputs = outputString.split(" ")
            Device(name, outputs)
        }
    val nameToDevice = devices.associateBy { it.name }
    val nameToCounts = mutableMapOf<String,Counts>()

    fun getCountsToOut(name: String): Counts {
        if (name == "out") {
            return Counts(1, 0, 0, 0)
        }
        var counts = nameToCounts[name]
        if (counts != null) {
            return counts
        }
        val device = nameToDevice.getValue(name)
        counts = device.outputs.map(::getCountsToOut).reduce { a, b -> a + b }
        counts = Counts(counts.all,
            if (name == "dac") counts.all else counts.dac,
            if (name == "fft") counts.all else counts.fft,
            when (name) {
                "dac" -> counts.fft
                "fft" -> counts.dac
                else -> counts.both
            })
        nameToCounts[name] = counts
        return counts
    }

    return when (part) {
        Part.ONE -> getCountsToOut("you").all
        Part.TWO -> getCountsToOut("svr").both
    }
}

fun main() {
    val testDay = -1 // or -1 to disable
    arrayOf(::day1, ::day2, ::day3, ::day4, ::day5, ::day6,
        ::day7, ::day8, ::day9, ::day10, ::day11).forEachIndexed { index, dayFunction ->
        val day = index + 1
        val filename = if (day == testDay) "day$day-test.txt" else "day$day.txt"
        val lines = File(filename).readLines()
        println("Day $day:")
        for (part in Part.entries) {
            val (result, timeTaken) = measureTimedValue {
                dayFunction(lines, part)
            }
            println("    Part ${part.toString().lowercase()}: $result (${timeTaken.inWholeMilliseconds} ms)")
        }
    }
}
