timestamp_nano() = Int(round(time() * 1e9))

function init_grid(barriers)
    min_lr = 1000
    max_lr = 0
    min_ud = 0
    max_ud = 0
    for line in barriers
        for (lr, ud) in line
            min_lr = min(lr, min_lr)
            max_lr = max(lr, max_lr)

            max_ud = max(ud, max_ud)
        end
    end

    grid = fill('.', (max_ud - min_ud + 1, max_lr - min_lr + 1 + 2))
    off_ud = min_ud - 1
    off_lr = min_lr - 2

    for line in barriers
        x, y = -1, -1
        for (lr, ud) in line
            if x == -1
                x, y = ud, lr
            else
                grid[min(x, ud)-off_ud:max(x, ud)-off_ud, min(y, lr)-off_lr:max(y, lr)-off_lr] .= '#'
                x, y = ud, lr
            end
        end
    end
    # set spawn
    spawn = 1, 500 - off_lr
    grid[spawn[1], spawn[2]] = '+'

    return grid, spawn
end

function part1(barriers)::Int
    grid, spawn = init_grid(barriers)

    n_sand = 0
    while true
        s_ud, s_lr = spawn
        while s_ud < size(grid, 1) &&
            (grid[s_ud+1, s_lr] == '.' || grid[s_ud+1, s_lr-1] == '.' || grid[s_ud+1, s_lr+1] == '.')
            if grid[s_ud+1, s_lr] == '.'
                s_ud += 1
            elseif grid[s_ud+1, s_lr-1] == '.'
                s_ud += 1
                s_lr -= 1
            else
                s_ud += 1
                s_lr += 1
            end
        end

        # fell off the map
        if s_ud == size(grid, 1)
            break
        else
            grid[s_ud, s_lr] = 'O'
            n_sand += 1
        end
    end
    n_sand
end

function part2(barriers)::Int
    grid, spawn = init_grid(barriers)
    # one row at the bottom
    grid = vcat(grid, fill('.', (1, size(grid, 2))))

    while size(grid, 1) + 1 > size(grid, 2) / 2
        if spawn[2] < size(grid, 2) / 2
            # column to the left of spawn
            grid = hcat(fill('.', (size(grid, 1), 1)), grid)
            spawn = spawn[1], spawn[2] + 1
        else
            # column to the right of spawn
            grid = hcat(grid, fill('.', (size(grid, 1), 1)))
        end
    end

    # bottomless pit now has a bottom
    grid = vcat(grid, fill('#', (1, size(grid, 2))))

    n_sand = 0
    while true
        s_ud, s_lr = spawn
        while s_ud + 1 < size(grid, 1) &&
            (grid[s_ud+1, s_lr] == '.' || grid[s_ud+1, s_lr-1] == '.' || grid[s_ud+1, s_lr+1] == '.')
            if grid[s_ud+1, s_lr] == '.'
                s_ud += 1
            elseif grid[s_ud+1, s_lr-1] == '.'
                s_ud += 1
                s_lr -= 1
            else
                s_ud += 1
                s_lr += 1
            end
        end

        grid[s_ud, s_lr] = 'O'
        n_sand += 1

        # filled up all the way to spawn
        if spawn == (s_ud, s_lr)
            break
        end
    end
    n_sand
end

get_data(path::String) =
    open(path) do file
        content = read(file, String)
        lines = split(content, "\n")

        [[parse.(Int, split(c, ",")) for c in split(l, " -> ")] for l in lines]
    end

start = timestamp_nano()

barriers = get_data("14/input.txt")

println("part1: ", part1(barriers))
println("part2: ", part2(barriers))

end_ = timestamp_nano()
println("time: ", round((end_ - start) / 1e6, digits=3), "ms")
