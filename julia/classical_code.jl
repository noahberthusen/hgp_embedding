struct ClassicalCode
    n::Integer
    m::Integer    
    dv::Integer
    dc::Integer
    bit_nbhd::Array{Integer}
    check_nbhd::Array{Integer}
end

function read_code(f_name::String)
    # Reads in classical code f_name and returns a ClassicalCode struct
    open(f_name) do f
        n = parse(Int, readline(f))
        m = parse(Int, readline(f))
        dv = parse(Int, readline(f))
        dc = parse(Int, readline(f))
        readline(f)

        bit_nbhd = Array{Int, 2}(undef, n, dv)
        for i = 1:n
            line = split(strip(readline(f), ','), ',')
            for j = 1:dv
                bit_nbhd[i, j] = parse(Int, line[j])
            end    
        end

        readline(f)
        check_nbhd = Array{Int, 2}(undef, m, dc)
        for i = 1:m
            line = split(strip(readline(f), ','), ',')
            for j = 1:dc
                check_nbhd[i, j] = parse(Int, line[j])
            end
        end

        return ClassicalCode(n, m, dv, dc, bit_nbhd, check_nbhd)
    end
end


