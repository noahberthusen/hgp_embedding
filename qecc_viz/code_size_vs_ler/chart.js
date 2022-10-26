codes = [
    "24_20_5_6",
    "30_25_5_6",
    "36_30_5_6",
    // "42_35_5_6",
    "48_40_5_6",
    "60_50_5_6",
    "84_70_5_6"
]

code_sizes = new Array()
for (var i in codes) {
    var n = parseInt(codes[i].substring(0,2))
    var m = parseInt(codes[i].substring(3,5))
    code_sizes.push(n**2 + m**2)
}

masks = [
    0,
    0.1,
    0.2,
    0.3
]

var margin = {top: 50, right: 100, bottom: 100, left: 100},
    width = 700 - margin.left - margin.right,
    height = 700 - margin.top - margin.bottom;



d3.csv('full_iterative_masked_decoding.csv').then(function(data) {
    data = data.filter(function(d) { return parseFloat(d.p_error) > 0})

    var errorExtent = d3.extent(data, function(d) {
        return parseFloat(d.p_error)
    })

    // full_data = new Array()
    // for (var i in masks) {
    //     full_data.push([])
    //     for (var j = 0; j < iterExtent[1]; j++) {
    //         full_data[i][j] = {t: j, data: []}
    //     }
    // }

    // for (var i in codes) {
    //     var n = parseInt(codes[i].substring(0,2))
    //     var m = parseInt(codes[i].substring(3,5))

    //     code_data = data.filter(function(d) {
    //         return (+d.nv === n) && (+d.nc === m)
    //     })
    //     for (var j in masks) {
    //         mask_data = code_data.filter(function(d) {
    //             return (parseFloat(d.p_mask) === masks[j])
    //         })
    //         // console.log(mask_data)
    //         for (var k = 0; k < iterExtent[1]; k++) {
    //             row = mask_data.filter(function(d) {
    //                 return +d.algo === k
    //             })
    //             // console.log(row)
    //             if (row.length == 1) {
    //                 full_data[j][k].data.push(row[0])
    //             }
    //         }
    //     }
    
    // }

    // for (var i in masks) {
    //     full_data[i] = full_data[i].filter(function(d) {
    //         return (d.data.length)
    //     })
    // }

    // console.log(full_data)

    d3.select("#selectButton")
        .selectAll('myOptions')
        .data(masks)
        .enter()
        .append('option')
        .text(function (d) { return d; }) // text showed in the menu
        .attr("value", function (d) { return d; }) // corresponding value returned by the button

    var x = d3.scaleLog()
        .domain([code_sizes[0], code_sizes[code_sizes.length-1]])
        .range([ 0, width ]);
   
    var y = d3.scaleLog()
        .domain( errorExtent)
        .range([ height, 0 ]);


    var update = function() {

        var selectedOption = d3.select("#selectButton").property("value")
        var time = +d3.select("#timeStep").property("value")

        filtered_data = data.filter(function(d) { return parseFloat(d.p_mask) === parseFloat(selectedOption) })

        var iterExtent = d3.extent(data, function(d) {
            return +d.algo
        })

        ts = [... new Set(filtered_data.map(function(d) { return +d.algo })) ].sort(function(a, b) { return a - b })

        if (!ts.includes(time)) {
            return
        } else {
            d3.select('#my_dataviz').selectAll("*").remove()
            
            var colorScale = d3.scaleSequential()
                .domain(iterExtent)
                .interpolator(d3.interpolateViridis);

            var svg = d3.select("#my_dataviz")
                .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform",
                        "translate(" + margin.left + "," + margin.top + ")");

            var scatter = svg
                .append("g")
                .selectAll(".dataPoint")
                .data(filtered_data)
                .enter()
                .append("circle")
                // .transition()
                // .duration(1000)
                .attr("cx", function(d) { return x((+d.nv)**2 + (+d.nc)**2)   })
                .attr("cy", function(d) { return y(parseFloat(d.p_error)) })
                .attr("r", 4)
                .style("fill", function(d) { return colorScale(+d.algo) })
                .style("opacity", function(d) { return +d.algo === time ? 1 : 0.1})

            svg.append("g")
                .attr("transform", "translate(0," + height + ")")
                .call(d3.axisBottom(x));

            svg.append("g")
                .call(d3.axisLeft(y));
            }        
    }

    d3.select("#selectButton").on("change", function(d) {
        update()
    })

    d3.select("#timeStep").on("input", function() {
        current_ind = this.value
        update() 
      })

    update()
})
