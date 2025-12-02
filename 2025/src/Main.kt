import java.io.File

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

fun main() {
    arrayOf(::day1).forEachIndexed { index, dayFunction ->
        val day = index + 1
        val lines = File("day$day.txt").readLines()
        for (part in 1..2) {
            val result = dayFunction(lines, part)
            println("Day $day part $part: $result")
        }
    }
}
