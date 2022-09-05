let computeGrayCode = function(dv) {
    res = []
    for (let i = 0; i < dv; i++) {
        res = res + [i] + res
    }
    return res
}


let hor_subset_score = function(hor_synd_diff, hor_wweight, ver_synd_diff, dv, dc){
    synd_diff = hor_synd_diff
    ver_flips = new Array()
    sorted_ver_synd_diff = ver_synd_diff.map(function(s, i) { return {s, i} })
    sorted_ver_synd_diff.sort((a, b) => a.s - b.s).reverse()

    wweight = hor_wweight
    sorted_ver_synd_diff.forEach(function(s) {
        if (s.s * wweight >= dv * synd_diff) {
            synd_diff = synd_diff + s.s
            ver_flips.push(s.i)
            wweight = wweight + dv
        } 
    });
    return { synd_diff: synd_diff, ver_flips: ver_flips }
}

let score_gen = function(synd_gen, synd_gen_mask) {
    let dc = synd_gen.length
    let dv = synd_gen[0].length
    let gray_code = computeGrayCode(dv)

    let hor_wweight = 0
    let hor_flips_array = new Array(dv).fill(false)
    let hor_synd_diff = 0
    let ver_synd_diff = new Array(dc).fill(0)
    for (let i = 0; i < dc; i++) {
        for (let j = 0; j < dv; j++) {
            if (!synd_gen_mask[i][j]) {
                ver_synd_diff[i] = ver_synd_diff[i] + 2*synd_gen[i][j] - 1
            }
        }
    }

    let _ = hor_subset_score(hor_synd_diff, hor_wweight, ver_synd_diff, dv, dc)
    best_synd_diff = _.synd_diff
    ver_flips = _.ver_flips

    let best_wweight = ver_flips.length * dv
    let best_flips = { ver_flips: ver_flips, hor_flips: [] }

    for (let g = 0; g < gray_code.length; g++) {
        j = parseInt(gray_code[g])
        if (hor_flips_array[j]) {
            hor_wweight = hor_wweight - dc
            hor_flips_array[j] = false
            for (let i = 0; i < dc; i++) {
                if (!synd_gen_mask[i][j]) {
                    ver_synd_diff[i] = ver_synd_diff[i] + 4*synd_gen[i][j] - 2
                    hor_synd_diff = hor_synd_diff - 2*synd_gen[i][j] + 1
                }
            }
        } else {
            hor_wweight = hor_wweight + dc
            hor_flips_array[j] = true
            for (let i = 0; i < dc; i++) {
                if (!synd_gen_mask[i][j]) {
                    ver_synd_diff[i] = ver_synd_diff[i] - 4*synd_gen[i][j] + 2
                    hor_synd_diff = hor_synd_diff + 2*synd_gen[i][j] - 1
                }
            }
        }

        _ = hor_subset_score(hor_synd_diff, hor_wweight, ver_synd_diff, dv, dc)
        synd_diff = _.synd_diff
        ver_flips = _.ver_flips

        wweight = hor_wweight + dv * ver_flips.length
        if (synd_diff * best_wweight > best_synd_diff * wweight) {
            best_synd_diff = synd_diff
            best_wweight = wweight
            best_flips = { ver_flips: ver_flips, hor_flips: [...Array(dv).keys()].filter(j => hor_flips_array[j]) }
        }
    }
    return { best_synd_diff: best_synd_diff, best_wweight: best_wweight, best_flips: best_flips }
}