timestamp_nano() = Int(round(time() * 1e9))

function part1(data, instructions)::String
    containers = copy(data)
    for (cnt, src, dst) in instructions
        for _ in 1:cnt
            # string concat
            containers[dst] = containers[dst] * containers[src][end]
            containers[src] = containers[src][1:end-1]
        end
    end

    return join((cont[end] for cont in containers), "")
end

function part2(data, instructions)::String
    containers = copy(data)
    for (cnt, src, dst) in instructions
        # string concat
        containers[dst] = containers[dst] * containers[src][end-cnt+1:end]
        containers[src] = containers[src][1:end-cnt]
    end

    return join((cont[end] for cont in containers), "")
end

start = timestamp_nano()

data, instructions = open("05/input.txt") do in_file
    content = read(in_file, String)

    N_STACKS = 9
    initial, instructions = split(content, "\n\n")
    data = ["" for _ in 1:N_STACKS]
    # remove numbered line
    initial = split(initial, "\n")[1:end-1]
    for line in reverse(initial)
        for i in 1:N_STACKS
            c = line[i*4 - 2]
            if c != ' '
                # string concat
                data[i] = data[i] * c
            end
        end
    end

    instructions = [
        parse.(Int, match(r"move (\d+) from (\d+) to (\d+)", line).captures)
        for line in split(instructions, "\n")
    ]

    data, instructions
end

println("part1: ", part1(data, instructions))
println("part2: ", part2(data, instructions))

end_ = timestamp_nano()
println("time: ", round((end_ - start) / 1000, digits=3), "µs")
