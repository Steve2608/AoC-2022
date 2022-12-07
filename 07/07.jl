timestamp_nano() = Int(round(time() * 1e9))

mutable struct File
    name::String
    size::Int
    parent::Union{File,Missing}
    children::Dict{String,File}

    File(name::String) = new(name, -1)
    File(name::String, size::Int) = new(name, size)
    File(name::String, size::Int, parent::Union{File,Missing}) = new(name, size, parent, Dict{String,File}())
end

get_size(fn::File)::Int = ifelse(fn.size >= 0,
    fn.size,
    sum(get_size.(values(fn.children)); init=0)
)

function file_system(lines)::File
    root = File("/", -1, missing)
    cwd = root

    i = 2
    while i <= length(lines)
        line = lines[i]
        parts = split(line, " ")
        if parts == ["\$", "cd", "/"]
            cwd = root
            i += 1
        elseif parts == ["\$", "cd", ".."]
            cwd = cwd.parent
            i += 1
        elseif parts[1:2] == ["\$", "cd"]
            # assumption: We're only cd-ing to known targets
            cwd = cwd.children[String(parts[3])]
            i += 1
        elseif parts[1:2] == ["\$", "ls"]
            i += 1
            while i <= length(lines)
                line = lines[i]
                parts = split(line, " ")
                name = String(parts[2])
                if parts[1] == "dir"
                    cwd.children[name] = File(name, -1, cwd)
                elseif parts[1] != "\$"
                    cwd.children[name] = File(name, parse(Int, String(parts[1])), cwd)
                else
                    break
                end
                i += 1
            end
        end
    end
    return root
end

function part1(root, max_size)::Int
    rec_size(cwd) = ifelse(cwd.size == -1, # is dir
        ifelse((s = get_size(cwd)) <= max_size, # is small enough
            s,
            0
        ) + sum(rec_size.(values(cwd.children)); init=0),
        0
    )

    return rec_size(root)
end

function part2(root, disk_space_total, free_space_min)::Int
    function find_min(cwd)
        if cwd.size == -1
            if to_free <= (s = get_size(cwd)) < optim
                optim = s
            end
            
            for c in values(cwd.children)
                find_min(c)
            end
        end

        return optim
    end
    
    to_free = free_space_min - (disk_space_total - (s = get_size(root)))
    optim = s
    return find_min(root)
end

start = timestamp_nano()

lines = open("07/input.txt") do in_file
    split(read(in_file, String), "\n")
end

root = file_system(lines)
println("part1: ", part1(root, Int(100e3)))
println("part2: ", part2(root, Int(70e6), Int(30e6)))

end_ = timestamp_nano()
println("time: ", round((end_ - start) / 1000, digits=3), "µs")
