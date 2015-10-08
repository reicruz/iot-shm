$(document).ready(function() {
    if (!$("#xcollapse").hasClass('collapsed')) {
        $('#real-time-chart-x').highcharts({
          chart: {
              type: 'spline',
              events: {
                load: executeRealTimeQueryX
              }
          },
          title: {
              text: 'X Magnitude vs Frequency'
          },
          subtitle: {
              text: 'Most recent readings for this building'
          },
          xAxis: {
          },
          yAxis: {
              title: {
                  text: 'Magnitude'
              },
              min: 0,
              max: 64
          },
          tooltip: {
              headerFormat: '<b>Freq, Mag</b><br>',
              pointFormat: '({point.x:.2f}, {point.y:.2f})'
          },
          plotOptions: {
              spline: {
                  marker: {
                      enabled: true
                  }
              }
          },
            series: []
      });
        real_interval_x = setInterval(executeRealTimeQueryX, 1010);
    }
    else {
        clearInterval(real_interval_x);
    }
    if (!$("#ycollapse").hasClass('collapsed')) {
        $('#real-time-chart-y').highcharts({
          chart: {
              type: 'spline',
              events: {
                load: executeRealTimeQueryY
              }
          },
          title: {
              text: 'Y Magnitude vs Frequency'
          },
          subtitle: {
              text: 'Most recent readings for this building'
          },
          xAxis: {
          },
          yAxis: {
              title: {
                  text: 'Magnitude'
              },
              min: 0,
              max: 64
          },
          tooltip: {
              headerFormat: '<b>Freq, Mag</b><br>',
              pointFormat: '({point.x:.2f}, {point.y:.2f})'
          },
          plotOptions: {
              spline: {
                  marker: {
                      enabled: true
                  }
              }
          },
            series: []
      });
        real_interval_y = setInterval(executeRealTimeQueryY, 1020);
    }
    else {
        clearInterval(real_interval_y);
    }
    if (!$("#zcollapse").hasClass('collapsed')) {
        $('#real-time-chart-z').highcharts({
          chart: {
              type: 'spline',
              events: {
                load: executeRealTimeQueryY
              }
          },
          title: {
              text: 'Z Magnitude vs Frequency'
          },
          subtitle: {
              text: 'Most recent readings for this buildnig'
          },
          xAxis: {
          },
          yAxis: {
              title: {
                  text: 'Magnitude'
              },
              min: 0,
              max: 64
          },
          tooltip: {
              headerFormat: '<b>Freq, Mag</b><br>',
              pointFormat: '({point.x:.2f}, {point.y:.2f})'
          },
          plotOptions: {
              spline: {
                  marker: {
                      enabled: true
                  }
              }
          },
            series: []
      });
        real_interval_z = setInterval(executeRealTimeQueryZ, 1030);
    }
    else {
        clearInterval(real_interval_z);
    }
});

function executeRealTimeQueryX() {
  $.ajax({
      url: '/iotshm/real_time_ajax_x/'+$('a[id=active_building]').attr("value"),
      type: 'get',
      dataType: 'json',
      success: function(data){
          updateRealTimeChartX(data);
        },
      error: function(data){
          $("#debugging").append("<h2>error: "+data.responseText+"</h2>");
        }
    });
}

function updateRealTimeChartX(json) {
    var index = 0;
    var colors = ['#FF00FF','#33CCFF','#33CC33','#33CC33'];
    var chart = $('#real-time-chart-x').highcharts();
    $.each(json, function (sensor, data) {
        if(index == 0){
            while(chart.series.length > 0) {
                //colors.append(chart.series[0].color);
                chart.series[0].remove(true);
            }
        }
        chart.addSeries({
            name: data["time"],
            data: data['x_data'],
            color: colors[index]
        });
        index++;
    });
}

function executeRealTimeQueryY() {
  $.ajax({
      url: '/iotshm/real_time_ajax_y/'+$('a[id=active_building]').attr("value"),
      type: 'get',
      dataType: 'json',
      success: function(data){
          updateRealTimeChartY(data);
        },
      error: function(data){
          $("#debugging").append("<h2>error: "+data.responseText+"</h2>");
        }
    });
}
function updateRealTimeChartY(json) {
    var index = 0;
    var colors = ['#FF00FF','#33CCFF','#33CC33','#33CC33'];
    var chart = $('#real-time-chart-y').highcharts();
    $.each(json, function (sensor, data) {
        if(index == 0){
            while(chart.series.length > 0){
                //colors.append(chart.series[0].color);
                chart.series[0].remove(true);
            }
        }
        chart.addSeries({
            name: data["time"],
            data: data['y_data'],
            color: colors[index]
        });
        index++;
    });
}

function executeRealTimeQueryZ() {
  $.ajax({
      url: '/iotshm/real_time_ajax_z/'+$('a[id=active_building]').attr("value"),
      type: 'get',
      dataType: 'json',
      success: function(data){
          updateRealTimeChartZ(data);
        },
      error: function(data){
          $("#debugging").append("<h2>error: "+data.responseText+"</h2>");
        }
    });
}
function updateRealTimeChartZ(json) {
    var index = 0;
    var colors = ['#FF00FF','#33CCFF','#33CC33','#33CC33'];
    var chart = $('#real-time-chart-z').highcharts();
    $.each(json, function (sensor, data) {
        if(index == 0){
            while(chart.series.length > 0) {
                //colors.append(chart.series[0].color);
                chart.series[0].remove(true);
            }
        }
        chart.addSeries({
            name: data["time"],
            data: data['z_data'],
            color: colors[index]
        });
        index++;
    });
}