import java.io.File
import kotlin.time.measureTime
import kotlin.time.measureTimedValue

fun day1(lines: List<String>, part: Int): Long {
    var pos = 50
    var count = 0L
    for (line in lines) {
        val direction = line[0]
        val distance = line.substring(1).toInt()
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
            return;
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
                    break;
                }
                if (id >= firstValue && !invalidIds.contains(id)) {
                    invalidIds.add(id);
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

fun main() {
    arrayOf(::day1, ::day2).forEachIndexed { index, dayFunction ->
        val day = index + 1
        val lines = File("day$day.txt").readLines()
        for (part in 1..2) {
            val (result, timeTaken) = measureTimedValue {
                dayFunction(lines, part)
            }
            println("Day $day part $part: $result (${timeTaken.inWholeMilliseconds} ms)")
        }
    }
}
