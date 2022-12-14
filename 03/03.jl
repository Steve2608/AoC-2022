timestamp_nano() = Int(round(time() * 1e9))

score(char)::Int = ifelse(char <= 'Z',
    char - 'A' + 27,
    char - 'a' + 1
)

part1(data)::Int = sum(map(
    score,
    # should only be one intersection anyways
    first(
        line[1:length(line)÷2] ∩ line[length(line)÷2+1:end]
    ) for line in data
))

part2(data)::Int = sum(map(
    score,
    first(
        data[i] ∩ data[i+1] ∩ data[i+2]
    ) for i in 1:3:length(data)
))

get_data(path::String) =
    open(path) do in_file
        split(read(in_file, String), "\n")
    end

start = timestamp_nano()

data = get_data("03/input.txt")

println("part1: ", part1(data))
println("part2: ", part2(data))

end_ = timestamp_nano()
println("time: ", round((end_ - start) / 1e6, digits=3), "ms")
