timestamp_nano() = Int(round(time() * 1e9))

part1(data)::Int = sum(
    (start1 <= start2 <= end2 <= end1) || (start2 <= start1 <= end1 <= end2)
    for (start1, end1, start2, end2) in data
)

part2(data)::Int = sum(
    (start1 <= start2 <= end1) || (start2 <= start1 <= end2)
    for (start1, end1, start2, end2) in data
)

get_data(path::String) =
    open(path) do in_file
        [
            parse.(Int, match(r"(\d+)-(\d+),(\d+)-(\d+)", line).captures)
            for line in split(read(in_file, String), "\n")
        ]
    end

start = timestamp_nano()

data = get_data("04/input.txt")

println("part1: ", part1(data))
println("part2: ", part2(data))

end_ = timestamp_nano()
println("time: ", round((end_ - start) / 1e6, digits=3), "ms")
