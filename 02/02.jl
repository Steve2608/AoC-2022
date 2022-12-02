function part1(data)::Int
    diff = 'X' - 'A'
    offset = 'W'

    score = 0
    for (opp, _, you) in data
        if (opp + diff == you)
            score += 3
        elseif ((opp == 'A' && you == 'Y') || (opp == 'B' && you == 'Z') ||
                (opp == 'C' && you == 'X'))
            score += 6
        end

        score += you - offset
    end

    return score
end


function part2(data)::Int
    score = 0
    for (opp, _, you) in data
        if (you == 'X') # loss
            if (opp == 'A')
                score += 3
            elseif (opp == 'B')
                score += 1
            else
                score += 2
            end
        elseif (you == 'Y') # draw
            score += 3 + (opp - 'A' + 1)
        else # win
            score += 6
            if (opp == 'A')
                score += 2
            elseif (opp == 'B')
                score += 3
            else
                score += 1
            end
        end
    end

    return score
end

data = open("02/input.txt") do in_file
    split(read(in_file, String), "\n")
end

println("part1: ", part1(data))
println("part2: ", part2(data))
