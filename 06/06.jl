timestamp_nano() = Int(round(time() * 1e9))

function solve(data, n_distinct)::Int
    for i in n_distinct:length(data)
        s = data[i-n_distinct+1:i]
        if length(Set(s)) == n_distinct
            return i
        end
    end
    return -1
end

start = timestamp_nano()

data = open("06/input.txt") do in_file
    read(in_file, String)
end

println("part1: ", solve(data, 4))
println("part2: ", solve(data, 14))

end_ = timestamp_nano()
println("time: ", round((end_ - start) / 1000, digits=3), "µs")
