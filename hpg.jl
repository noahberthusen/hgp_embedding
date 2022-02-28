using Random
using LinearAlgebra
using DelimitedFiles
using SparseArrays

n = 16
deg_c = 4 # w_r. Every check has this many bits in it
deg_v = 3 # w_c. Every bit is in this many checks
num_checks = div(n*deg_v, deg_c)
k = n - num_checks

vs = vcat([[j for i in 1:deg_v] for j in 1:n]...)
cs = vcat([[j for i in 1:deg_c] for j in 1:num_checks]...)

H = zeros(Int8, num_checks, n)

while(length(vs) > 0 && length(cs) > 0)
    double_edge = true
    
    while(double_edge)
        shuffle!(vs)
        shuffle!(cs)

        if (H[cs[1], vs[1]] != 1)
            double_edge = false
            H[cs[1], vs[1]] = 1
            popfirst!(vs)
            popfirst!(cs)
        end
    end
end

H = readdlm("./good_ldpc_codes/16_4_3.txt", ' ', Int8, '\n')

hx1 = kron(H, Matrix{Int8}(I, size(H)[2], size(H)[2]));
hx2 = kron(Matrix{Int8}(I, size(H)[1], size(H)[1]), transpose(H))
Hx = sparse(hcat(hx1, hx2))

hz1 = kron(Matrix{Int8}(I, size(H)[2], size(H)[2]), H)
hz2 = kron(transpose(H), Matrix{Int8}(I, size(H)[1], size(H)[1]))
Hz = sparse(hcat(hz1, hz2))

function powerset(x::Vector{T}) where T
    result = Vector{T}[[]]
    for elem in x, j in eachindex(result)
        push!(result, [result[j] ; elem])
    end
    return result
end

function syn_from_F(F, H)
    result = Set()
    for i in 1:size(Hx)[1]
        row = Set(H[i, :].nzind)
        if length(intersect(row, F)) > 0
            push!(result, i)
        end
    end
    return result
end

Fx = vcat([powerset(findnz(sparse(Hx)[i, :])[1])[2:end] for i in 1:size(Hx)[1]]...)
Fx = map(x -> Set(x), Fx)
Fz = vcat([powerset(findnz(sparse(Hz)[i, :])[1])[2:end] for i in 1:size(Hz)[1]]...)
Fz = map(x -> Set(x), Fz)

sigma_Fx = [syn_from_F(x, Hx) for x in Fx]  # set of indices where syndrome is 1
sigma_Fz = [syn_from_F(g, Hz) for g in Fz]