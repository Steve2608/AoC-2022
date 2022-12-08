timestamp_nano() = Int(round(time() * 1e9))

get_data() = open("01/input.txt") do in_file
    content = read(in_file, String)
    sort(
        collect(
            sum(
                parse.(Int, eachsplit(elf, "\n"))
            ) for elf in eachsplit(content, "\n\n")),
        rev=true
    )[1:3]
end

start = timestamp_nano()

data = get_data()

println("part1: ", data[1])
println("part2: ", sum(data))

end_ = timestamp_nano()
println("time: ", round((end_ - start) / 1e6, digits=3), "ms")
