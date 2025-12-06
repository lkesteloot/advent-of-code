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
        1 -> {
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

        2 -> result = ranges.sumOf { it.last - it.first + 1 }
    }

    return result
}

fun day6(lines: List<String>, part: Int): Long {
    var result = 0L

    when (part) {
        1 -> {
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

        2 -> {
            val columnCount = lines[0].length
            myAssert(lines.all { it.length == columnCount })
            val rowCount = lines.size - 1
            val ops = lines[lines.size - 1]
            var subResult = 0L
            var op = ' '
            for (i in 0 until columnCount) {
                if (ops[i] != ' ') {
                    myAssert(op == ' ')
                    op = ops[i]
                    subResult = when (op) {
                        '+' -> 0
                        '*' -> 1
                        else -> throw Error()
                    }
                }
                var value = 0
                var foundAny = false
                for (j in 0 until rowCount) {
                    val ch = lines[j][i]
                    if (ch != ' ') {
                        value = value * 10 + ch.digitToInt()
                        foundAny = true
                    }
                }
                if (foundAny) {
                    when (op) {
                        '+' -> subResult += value
                        '*' -> subResult *= value
                        else -> throw Error()
                    }
                } else {
                    // Blank column.
                    myAssert(ops[i] == ' ')
                    result += subResult
                    subResult = 0
                    op = ' '
                }
            }
            result += subResult
        }
    }

    return result
}

fun main() {
    val testDay = -6 // or -1 to disable
    arrayOf(::day1, ::day2, ::day3, ::day4, ::day5, ::day6).forEachIndexed { index, dayFunction ->
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
