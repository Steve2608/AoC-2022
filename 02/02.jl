timestamp_nano() = Int(round(time() * 1e9))

part1(data)::Int = sum(
    (you - 'W') + # ASCII hax
    ifelse(opp + ('X' - 'A') == you,
        3,
        ifelse((opp == 'A' && you == 'Y') || (opp == 'B' && you == 'Z') || (opp == 'C' && you == 'X'),
            6,
            0 # empty case
        )
    ) for (opp, _, you) in data
)

part2(data)::Int = sum(
    ifelse(you == 'X', # loss
        ifelse(opp == 'A',
            3,
            ifelse(opp == 'B', 1, 2)
        ),
        ifelse(you == 'Y', # draw
            3 + (opp - 'A' + 1),
            6 + ifelse(opp == 'A', # win
                2,
                ifelse(opp == 'B',
                    3,
                    1
                )
            )
        )
    ) for (opp, _, you) in data
)

get_data() = open("02/input.txt") do in_file
    split(read(in_file, String), "\n")
end

start = timestamp_nano()

data = get_data()

println("part1: ", part1(data))
println("part2: ", part2(data))

end_ = timestamp_nano()
println("time: ", round((end_ - start) / 1e6, digits=3), "ms")
