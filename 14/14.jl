timestamp_nano() = Int(round(time() * 1e9))

function init_grid(barriers)
    min_lr = 1000
    max_lr = 0
    max_ud = 0
    for line in barriers
        for (lr, ud) in line
            min_lr = min(lr, min_lr)
            max_lr = max(lr, max_lr)

            max_ud = max(ud, max_ud)
        end
    end

    grid = fill('.', (max_ud + 1, max_lr - min_lr + 1 + 2))
    off_lr = min_lr - 2

    for line in barriers
        x, y = -1, -1
        for (lr, ud) in line
            if x == -1
                x, y = ud, lr
            else
                grid[min(x, ud)-1:max(x, ud)-1, min(y, lr)-off_lr:max(y, lr)-off_lr] .= '#'
                x, y = ud, lr
            end
        end
    end

    # set spawn
    spawn = 1, 500 - off_lr
    return grid, spawn
end

function part1(barriers)::Int
    function dfs(ud::Int, lr::Int)::Bool
        if ud == size(grid, 1) && grid[ud, lr] != '#'
            return false
        end

        if grid[ud, lr] != '.'
            return true
        end

        if !dfs(ud + 1, lr) || !dfs(ud + 1, lr - 1) || !dfs(ud + 1, lr + 1)
            return false
        end

        grid[ud, lr] = 'O'
        n_sand += 1
        return true
    end

    grid, spawn = init_grid(barriers)
    n_sand = 0
    dfs(spawn[1], spawn[2])
    n_sand
end

function part2(barriers)::Int
    function dfs(ud::Int, lr::Int)
        if ud >= size(grid, 1) || grid[ud, lr] != '.'
            return
        end

        dfs(ud + 1, lr)
        dfs(ud + 1, lr - 1)
        dfs(ud + 1, lr + 1)

        grid[ud, lr] = 'O'
        n_sand += 1
    end

    grid, spawn = init_grid(barriers)

    grid_new = fill('.', (size(grid, 1) + 2, (size(grid, 1) + 2) * 2 + 1))
    grid_new[end, 1:end] .= '#'
    grid_new[1:size(grid, 1), size(grid_new, 1)-spawn[2]:size(grid_new, 1)+(size(grid, 2)-spawn[2]-1)] = grid
    grid = grid_new

    n_sand = 0
    dfs(spawn[1], size(grid, 1))
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
