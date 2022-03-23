include("classical_code.jl")

struct LookupTable
    ccode::ClassicalCode
    synd_matrix
    synd_weight::Integer
    lookup_table
    last_update
    round::Integer
end


function compute_gray_code(table::LookupTable)
    res = []
    for i = 1:table.ccode.dv
        res = [res; i; res]
    end
    return res
end


function hor_subset_score(hor_syn_diff, hor_weight::Integer, ver_synd_diff)
    synd_diff = hor_syn_diff

    ver_flips = Int[]
    # sorted_ver_synd_diff = [(x, i) for (i, x) in enumerate(ver_synd_diff)]
    sorted_ver_synd_diff = [(ver_synd_diff[i], i) for i = 1:length(ver_synd_diff)]
    sort!(sorted_ver_synd_diff, by=x -> x[1], rev=true)

    weight = hor_weight
    for (s, i) in sorted_ver_synd_diff
        if (s * weight >= synd_diff)
            synd_diff += s
            push!(ver_flips, i)
            weight += 1
        end
    end

    return (synd_diff, ver_flips)
end


function score_gen(table::LookupTable, synd_gen::BitMatrix)
    dv = table.ccode.dv
    dc = table.ccode.dc

    hor_weight::Integer = 0
    hor_synd_diff::Integer = 0

    hor_flips_array = falses(dv)
    ver_synd_diff = zeros(Int8, dc)

    for j = 1:dv
        for i = 1:dc
            if (synd_gen[i, j])
                ver_synd_diff[i] += 1
            else
                ver_synd_diff[i] -= 1
            end
        end
    end

    best_synd_diff, ver_flips = hor_subset_score(hor_synd_diff, hor_weight, ver_synd_diff)
    best_weight = length(ver_flips)
    best_flips = (ver_flips, [])

    for j in compute_gray_code(table)
        if (hor_flips_array[j])
            hor_weight -= 1
            hor_flips_array[j] = false

            for i = 1:dc
                if (synd_gen[i, j])
                    ver_synd_diff[i] += 2
                    hor_synd_diff -= 1
                else
                    ver_synd_diff[i] -= 2
                    hor_synd_diff += 1
                end
            end
        else
            hor_weight += 1
            hor_flips_array[j] = true

            for i = 1:dc
                if (synd_gen[i, j])
                    ver_synd_diff[i] -= 2
                    hor_synd_diff += 1
                else
                    ver_synd_diff[i] += 2
                    hor_synd_diff -= 1
                end
            end
        end

        synd_diff, ver_flips = hor_subset_score(hor_synd_diff, hor_weight, ver_synd_diff)
        weight = hor_weight + length(ver_flips)

        if (synd_diff * best_weight > best_synd_diff * weight)
            best_synd_diff = synd_diff
            best_weight = weight
            best_flips = (ver_flips, [j for j = 1:dv if hor_flips_array[j]])
        end
    end

    return (best_synd_diff, best_weight, best_flips)
end


function update_score_generator(table, gen)
    """
    Computes the best column and row flips for a given generator gen
    """
    c1, v2 = gen
    ver = table.ccode.check_nbhd[c1]
    hor = table.ccode.bit_nbhd[v2]

    synd_gen = [[table.synd_matrix[ver[i], hor[j]] for j = 1:table.ccode.dv] for i = 1:table.ccode.dc]
    table.lookup_table[c1, v2] = score_gen(table, synd_gen)
end


function compute_synd(table::LookupTable, gen, flips)
    c1, v2 = gen
    ver_flips, hor_flips = flips
    dv = table.ccode.dv
    dc = table.ccode.dc

    synd_matrix = falses(dc, dv)
    for i in ver_flips
        for j = 1:dv
            synd_matrix[i, j] = !synd_matrix[i, j]
        end
    end
    for j in hor_flips
        for i = 1:dc
            synd_matrix[i, j] = !synd_matrix[i, j]
        end
    end

    synd = []
    for i = 1:dc
        for j = 1:dv
            if (synd_matrix[i,j])
                v1 = table.ccode.check_nbhd[c1, i]
                c2 = table.ccode.bit_nbhd[v2, j]
                push!(synd, (v1, c2))
            end
        end
    end
    return synd
end


function comput_qbits(table::LookupTable, gen, flips)
    c1, v2 = gen
    ver_flips, hor_flips = flips

    vv_qbits = []
    for i in ver_flips
        push!(vv_qbits, (table.ccode.check_nbhd[c1, i], v2))
    end
    cc_qbits = []
    for j in hor_flips
        push!(cc_qbits, (c1, table.ccode.bit_nbhd[v2, j]))
    end

    return (vv_qbits, cc_qbits)
end


function find_best_gen(table::LookupTable)
    """
    Returns the best generator to flip for the current syndrome
    """
    best_gen = nothing
    best_synd_diff = 0
    best_weight = 0

    for c1 = 1:table.ccode.m
        for v2 = 1:table.ccode.n
            synd_diff, weight, _ = table.lookup_table[c1, v2]
            if (best_synd_diff * weight < synd_diff * best_weight)
                best_gen = (c1, v2)
                best_synd_diff = synd_diff
                best_weight = weight
            end
        end
    end

    return best_gen
end


function update(table::LookupTable, gen)
    """
    Update the lookup table under the assumption that we flip the best subset of the generator gen
    """
    table.round += 1
    c1, v2 = gen
    synd_diff, _, flips = table.lookup_table[c1, v2]
    synd = compute_synd(table, gen, flips)

    table.synd_weight -= synd_diff

    for (v1, c2) in synd
        table.synd_matrix[v1, c2] = !table.synd_matrix[v1, c2]
    end

    for (v1, c2) in synd
        for v2 in table.ccode.check_nbhd[c2]
            for c1 in table.ccode.bit_nbhd[v1]
                if (table.last_update[c1, v2] != table.round)
                    update_score_generator(table, (c1, v2))
                    table.last_update[c1, v2] = table.round
                end
            end
        end
    end
    
    return comput_qbits(table, gen, flips)
end


