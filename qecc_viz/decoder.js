WEIGHT_FLAG = false

var computeGrayCode = function(dv) {
    res = []
    for (var i = 0; i < dv; i++) {
        res = res + [i] + res
    }
    return res
}

class LookupTable { // single timestep in decoding
    constructor(vv, cc, z_gens, x_gens, dv, dc) {
        this.vv = vv
        this.cc = cc
        this.z_gens = z_gens
        this.x_gens = x_gens
        this.n = vv.length
        this.m = cc.length
        this.dv = dv
        this.dc = dc
        this.gray_code = computeGrayCode(dv)

        // this.decoding
        this.update_score_generators()
    }

    hor_subset_score = function(hor_synd_diff, hor_weight, ver_synd_diff){
        var synd_diff = hor_synd_diff
        var ver_flips = new Array()
        var sorted_ver_synd_diff = ver_synd_diff.map(function(s, i) { return {s, i} })
        sorted_ver_synd_diff.sort((a, b) => a.s - b.s).reverse()
    
        var weight = hor_weight
        sorted_ver_synd_diff.forEach(function(s) {
            if (s.s * weight >= ( WEIGHT_FLAG ? this.dv : 1 ) * synd_diff) {
                synd_diff = synd_diff + s.s
                ver_flips.push(s.i)
                weight = WEIGHT_FLAG ? weight + this.dv : weight + 1
            } 
        });
        return { synd_diff: synd_diff, ver_flips: ver_flips }
    }

    score_gen = function(synd_gen, synd_gen_mask) {
        var hor_weight = 0
        var hor_flips_array = new Array(this.dv).fill(false)
        var hor_synd_diff = 0
        var ver_synd_diff = new Array(this.dc).fill(0)
        for (var i = 0; i < dc; i++) {
            for (var j = 0; j < dv; j++) {
                if (!synd_gen_mask[i][j]) {
                    ver_synd_diff[i] = ver_synd_diff[i] + 2*synd_gen[i][j] - 1
                }
            }
        }
    
        var _ = this.hor_subset_score(hor_synd_diff, hor_weight, ver_synd_diff)
        var best_synd_diff = _.synd_diff
        var ver_flips = _.ver_flips
    
        var best_weight = WEIGHT_FLAG ? ver_flips.length * this.dv : ver_flips.length
        var best_flips = { ver_flips: ver_flips, hor_flips: [] }
    
        for (var g = 0; g < this.gray_code.length; g++) {
            j = parseInt(this.gray_code[g])
            if (hor_flips_array[j]) {
                hor_weight = WEIGHT_FLAG ? hor_weight - this.dc : hor_weight - 1
                hor_flips_array[j] = false
                for (var i = 0; i < this.dc; i++) {
                    if (!synd_gen_mask[i][j]) {
                        ver_synd_diff[i] = ver_synd_diff[i] + 4*synd_gen[i][j] - 2
                        hor_synd_diff = hor_synd_diff - 2*synd_gen[i][j] + 1
                    }
                }
            } else {
                hor_weight = WEIGHT_FLAG ? hor_weight + this.dc : hor_weight + 1
                hor_flips_array[j] = true
                for (var i = 0; i < this.dc; i++) {
                    if (!synd_gen_mask[i][j]) {
                        ver_synd_diff[i] = ver_synd_diff[i] - 4*synd_gen[i][j] + 2
                        hor_synd_diff = hor_synd_diff + 2*synd_gen[i][j] - 1
                    }
                }
            }
    
            _ = this.hor_subset_score(hor_synd_diff, hor_weight, ver_synd_diff)
            var synd_diff = _.synd_diff
            ver_flips = _.ver_flips
    
            var weight = WEIGHT_FLAG ? hor_weight + this.dv * ver_flips.length : hor_weight + ver_flips.length
            if (synd_diff * best_weight > best_synd_diff * weight) {
                best_synd_diff = synd_diff
                best_weight = weight
                best_flips = { ver_flips: ver_flips, hor_flips: [...Array(this.dv).keys()].filter(j => hor_flips_array[j]) }
            }
        }
        return { best_synd_diff: best_synd_diff, best_weight: best_weight, best_flips: best_flips }
    }


    update_score_generators = function() {
        for (var k = 0; k < this.m; k++) {
    		for (var l = 0; l < this.n; l++) {
    			var gen = this.x_gens[k][l]
    
    			var synd_gen = new Array()
    			var synd_mask = new Array()
    			for (var i = 0; i < dc; i++) {
    				synd_gen.push(new Array())
    				synd_mask.push(new Array())
    				for (var j = 0; j < dv; j++) {
    					synd_gen[i].push(this.z_gens[gen.vv_nbhd[i]][gen.cc_nbhd[j]].in_synd)
    					synd_mask[i].push(this.z_gens[gen.vv_nbhd[i]][gen.cc_nbhd[j]].in_mask)
    				}
    			}
    			gen.score = this.score_gen(synd_gen, synd_mask)
    		}
    	}
    }

    find_best_gen = function() {
        var best_gen = null
        var synd_diff = 0
        var best_synd_diff = 0
        var weight = 0
        var best_weight = 1
    
        for (var i = 0; i < this.x_gens.length; i++) {
            for (var j = 0; j < this.x_gens[0].length; j++) {
                var _ = this.x_gens[i][j].score
                synd_diff = _.best_synd_diff
                weight = _.best_weight
    
                if (synd_diff * best_weight > best_synd_diff * weight) {
                    best_gen = this.x_gens[i][j]
                }
            }
        }
        return best_gen
    }


    compute_syndrome = function() {
        this.z_gens.flat().map(function(gen) { gen.in_synd = false })
        var _this = this
        this.cc.flat().map(function(qbt) {
            if (qbt.in_error) {
                qbt.z_gen_nbhd.map(yind => {
                    _this.z_gens[yind][qbt.xind].in_synd = !_this.z_gens[yind][qbt.xind].in_synd
                })
            }
        })
        this.vv.flat().map(function(qbt) {
            if (qbt.in_error) {
                qbt.z_gen_nbhd.map(xind => {
                    _this.z_gens[qbt.yind][xind].in_synd = !_this.z_gens[qbt.yind][xind].in_synd
                })
            }
        })
    }


    randomError = function(p) {
        this.vv.flat().map(function(qbt) {
            qbt.in_error = (Math.random() < p)
        })
        this.cc.flat().map(function(qbt) {
            qbt.in_error = (Math.random() < p)
        })
    }

    randomMask = function(p) {
        this.z_gens.flat().map(function(gen) {
            gen.in_mask = (Math.random() < p)
        })
    }

    apply_gen = function(gen) {
        var { ver_flips, hor_flips } = gen.score.best_flips
        console.log(ver_flips, hor_flips)        
        for (var i = 0; i < ver_flips.length; i++) {
            var qbt = this.vv[gen.vv_nbhd[ver_flips[i]]][gen.xind]
            qbt.in_error = !qbt.in_error
        }
        for (var j = 0; j < hor_flips.length; j++) {
            var qbt = this.cc[gen.yind][gen.cc_nbhd[hor_flips[j]]]
            qbt.in_error = !qbt.in_error
        }
        // self.synd_weight = self.synd_weight - synd_diff        
    }

}


