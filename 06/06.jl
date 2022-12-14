timestamp_nano() = Int(round(time() * 1e9))

function solve(data, n_distinct, offset=0)::Int
    for i in (offset+n_distinct):length(data)
        s = data[i-n_distinct+1:i]
        if length(Set(s)) == n_distinct
            return i
        end
    end
    return -1
end

get_data(path::String) =
    open(path) do in_file
        read(in_file, String)
    end

start = timestamp_nano()

data = get_data("06/input.txt")
p1 = solve(data, 4)
println("part1: ", p1)
println("part2: ", solve(data, 14, p1 - 4))

end_ = timestamp_nano()
println("time: ", round((end_ - start) / 1e6, digits=3), "ms")
