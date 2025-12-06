import java.io.File
import kotlin.math.max
import kotlin.time.measureTimedValue

fun myAssert(assertion: Boolean) {
    if (!assertion) {
        throw AssertionError()
    }
}

fun day1(lines: List<String>, part: Int): Long {
    var pos = 50
    var count = 0L
    for (line in lines) {
        val direction = line[0]
        val distance = line.drop(1).toInt()
        val step = if (direction == 'R') 1 else -1

        if (part == 1) {
            pos = Math.floorMod(pos + step*distance, 100)
            if (pos == 0) {
                count += 1
            }
        } else {
            repeat (distance) {
                pos = Math.floorMod(pos + step, 100)
                if (pos == 0) {
                    count += 1
                }
            }
        }
    }

    return count
}

fun day2(lines: List<String>, part: Int): Long {
    var result = 0L

    val invalidIds = mutableSetOf<Long>()

    fun tryRange(first: String, last: String) {
        assert(first.length == last.length)
        if (part == 1 && first.length % 2 != 0) {
            return
        }
        val firstValue = first.toLong()
        val lastValue = last.toLong()
        val halfLength = last.length / 2
        val lenRange = (if (part == 1) halfLength else 1)..halfLength
        for (len in lenRange) {
            var counter = first.take(len).toLong()
            val repeat = if (part == 1) 2 else first.length / len
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

fun day3(lines: List<String>, part: Int): Long {
    var result = 0L
    val batteryCount = if (part == 1) 2 else 12

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

fun day4(lines: List<String>, part: Int): Long {
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
        1 -> result = accessiblePositions.size.toLong()
        2 -> {
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

fun day5(lines: List<String>, part: Int): Long {
    var result = 0L

    val blankIndex = lines.indexOf("")
    val freshRanges = lines.take(blankIndex)
        .map { line ->
            val (low, high) = line.split('-').map { it.toLong() }
            low..high
        }

    when (part) {
        1 -> {
            result = lines.drop(blankIndex + 1)
                .map { it.toLong() }
                .count { id -> freshRanges.any { range -> range.contains(id) } }
                .toLong()
        }

        2 -> {
            // Sort our ranges.
            val ranges = freshRanges.sortedBy { it.first }.toMutableList()
            for (i in ranges.indices) {
                val current = ranges[i]
                val next = ranges.getOrNull(i + 1)
                if (next == null || current.last < next.first) {
                    result += current.last - current.first + 1
                } else {
                    ranges[i + 1] = current.first..max(current.last,next.last)
                }
            }
        }
    }

    return result
}

fun main() {
    val testDay = -1 // or -1 to disable
    arrayOf(::day1, ::day2, ::day3, ::day4, ::day5).forEachIndexed { index, dayFunction ->
        val day = index + 1
        val filename = if (day == testDay) "day$day-test.txt" else "day$day.txt"
        val lines = File(filename).readLines()
        for (part in 1..2) {
            val (result, timeTaken) = measureTimedValue {
                dayFunction(lines, part)
            }
            println("Day $day part $part: $result (${timeTaken.inWholeMilliseconds} ms)")
        }
    }
}
