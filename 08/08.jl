timestamp_nano() = Int(round(time() * 1e9))

function part1(grid)::Int
    # no double counting in the corners
    i = size(grid, 1)*2 + size(grid, 2)*2 - 4
    for x in 2:(size(grid, 1) - 1)
        for y in 2:(size(grid, 2) - 1)
            tree = grid[x, y]
            if all(tree .> grid[x+1:end, y]) || all(tree .> grid[1:x-1, y]) || all(tree .> grid[x, y+1:end]) || all(tree .> grid[x, 1:y-1])
                i += 1
            end
        end
    end
    return i
end

function part2(grid)::Int
    best_scenic_score = 0
    w, h = size(grid, 1), size(grid, 2)

    for x in 2:(w - 1)
        for y in 2:(h - 1)
            tree = grid[x, y]
                   
            score_up = 1
            i, j = x, y
            while i > 2 && tree > grid[i - 1, j]
                score_up += 1
                i -= 1
            end
                   
            score_left = 1
            i, j = x, y
            while j > 2 && tree > grid[i, j - 1]
                score_left += 1
                j -= 1
            end

            score_down = 1
            i, j = x, y
            while i < w - 1 && tree > grid[i + 1, j]
                score_down += 1
                i += 1
            end
                   
            score_right = 1
            i, j = x, y
            while j < h - 1 && tree > grid[i, j + 1]
                score_right += 1
                j += 1
            end

            best_scenic_score = max(score_up * score_left * score_down * score_right, best_scenic_score)
        end
    end
    return best_scenic_score
end

start = timestamp_nano()

grid = open("08/input.txt") do file
    content = read(file, String)
    lines = split(content, "\n")
           
    reduce(hcat, parse.(Int, split(x, "")) for x in lines)'
end

println("part1: ", part1(grid))
println("part2: ", part2(grid))

end_ = timestamp_nano()
println("time: ", round((end_ - start) / 1e6, digits=3), "ms")
