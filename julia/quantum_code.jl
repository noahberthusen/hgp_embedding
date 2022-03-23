include("classical_code.jl")

function compute_synd_matrix(ccode::ClassicalCode, error)
    """
    Returns the syndrome of the list of errors
    """
    vv_error, cc_error = error
    synd_matrix = falses(ccode.n, ccode.m)

    for (v1, v2) in vv_error
        for c2 in ccode.bit_nbhd[v2]
            synd_matrix[v1, c2] = !synd_matrix[v1, c2]
        end
    end

    for (c1, c2) in cc_error
        for v1 in ccode.check_nbhd[c1]
            synd_matrix[v1, c2] = !synd_matrix[v1, c2]
        end
    end

    return synd_matrix
end


function random_error(ccode::ClassicalCode, p::Float64)
    """
    Returns a random iid error with probability p
    """
    vv_error = [(v1, v2) for v1 = 1:ccode.n, v2 = 1:ccode.n if p > rand()]
    cc_error = [(c1, c2) for c1 = 1:ccode.m, c2 = 1:ccode.m if p > rand()]

    return (vv_error, cc_error)
end

# ccode = read_code("./ccodes/16_12_3_4.txt")
# error = random_error(ccode, 0.1)
# display(compute_synd_matrix(ccode, error))