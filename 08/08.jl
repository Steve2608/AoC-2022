timestamp_nano() = Int(round(time() * 1e9))

function part1(grid)::Int
    # no double counting in the corners
    n = size(grid, 1) * 2 + size(grid, 2) * 2 - 4
    for x in 2:(size(grid, 1)-1)
        for y in 2:(size(grid, 2)-1)
            tree = grid[x, y]
            n += all(tree .> grid[x+1:end, y]) || all(tree .> grid[1:x-1, y]) || all(tree .> grid[x, y+1:end]) || all(tree .> grid[x, 1:y-1])
        end
    end
    return n
end

function part2(grid)::Int
    scenic_score = 0
    h, w = size(grid, 1) - 1, size(grid, 2) - 1

    for i in 2:h
        for j in 2:w
            tree = grid[i, j]

            score_up = 1
            x = i
            while x > 2 && tree > grid[x-=1, j]
                score_up += 1
            end

            score_left = 1
            y = j
            while y > 2 && tree > grid[i, y-=1]
                score_left += 1
            end

            score_down = 1
            x = i
            while x < w - 1 && tree > grid[x+=1, j]
                score_down += 1
            end

            score_right = 1
            y = j
            while y < h - 1 && tree > grid[i, y+=1]
                score_right += 1
            end

            scenic_score = max(score_up * score_left * score_down * score_right, scenic_score)
        end
    end
    return scenic_score
end

get_data(path::String) =
    open(path) do file
        content = read(file, String)
        lines = split(content, "\n")

        reduce(hcat, parse.(Int, split(x, "")) for x in lines)'
    end

start = timestamp_nano()

grid = get_data("08/input.txt")

println("part1: ", part1(grid))
println("part2: ", part2(grid))

end_ = timestamp_nano()
println("time: ", round((end_ - start) / 1e6, digits=3), "ms")
