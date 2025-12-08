import java.io.File
import kotlin.math.max
import kotlin.time.measureTimedValue

enum class Part { ONE, TWO }

fun myAssert(assertion: Boolean) {
    if (!assertion) {
        throw AssertionError()
    }
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

fun main() {
    val testDay = -1 // or -1 to disable
    arrayOf(::day1, ::day2, ::day3, ::day4, ::day5, ::day6, ::day7, ::day8).forEachIndexed { index, dayFunction ->
        val day = index + 1
        val filename = if (day == testDay) "day$day-test.txt" else "day$day.txt"
        val lines = File(filename).readLines()
        for (part in Part.entries) {
            val (result, timeTaken) = measureTimedValue {
                dayFunction(lines, part)
            }
            println("Day $day part $part: $result (${timeTaken.inWholeMilliseconds} ms)")
        }
    }
}
