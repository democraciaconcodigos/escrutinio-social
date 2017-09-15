var width = 300;
var height = 300;

nv.addGraph(function() {
    var chart = nv.models.pie()
            .x(function(d) { return d.key; })
            .y(function(d) { return d.y; })
            .width(width)
            .height(height)
            .labelsOutside(true)
            ;

    d3.select("#svg_reporte")
            .datum([rep_data])
            .transition().duration(1200)
            .attr('width', width)
            .attr('height', height)
            .call(chart);

    // LISTEN TO CLICK EVENTS ON THE SLICES OF THE PIE
    // chart.dispatch.on('elementClick', function() {
    //   code...
    // });

    // OTHER EVENTS DISPATCHED BY THE PIE INCLUDE: elementDblClick, elementMouseover, elementMouseout, elementMousemove, renderEnd
    // @see nv.models.pie
    return chart;
});

nv.addGraph(function() {
    var chart = nv.models.pie()
            .x(function(d) { return d.key; })
            .y(function(d) { return d.y; })
            .width(width)
            .height(height)
            .labelsOutside(true)
            ;

    d3.select("#svg_parte")
            .datum([par_data])
            .transition().duration(1200)
            .attr('width', width)
            .attr('height', height)
            .call(chart);

    // LISTEN TO CLICK EVENTS ON THE SLICES OF THE PIE
    // chart.dispatch.on('elementClick', function() {
    //   code...
    // });

    // OTHER EVENTS DISPATCHED BY THE PIE INCLUDE: elementDblClick, elementMouseover, elementMouseout, elementMousemove, renderEnd
    // @see nv.models.pie
    return chart;
});
