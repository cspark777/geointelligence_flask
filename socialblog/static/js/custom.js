(function($) {
  "use strict"; // Start of use strict

    var data_json = $("#chart1_data").val();
    var data_obj = JSON.parse(data_json);

    var ctx = document.getElementById('chart1').getContext('2d');
    //ctx.canvas.width = 1000;
    ctx.canvas.height = 250;

    var color = Chart.helpers.color;
    var cfg = {

      data: {
        
        datasets: [
        {
          label: 'Negative',
          backgroundColor: color(window.chartColors.red).alpha(0.5).rgbString(),
          borderColor: window.chartColors.red,
          data: data_obj.y_negative,
          type: 'line',
          pointRadius: 0,
          fill: false,
          lineTension: 0,
          borderWidth: 2
        },
        
        
        {
          label: 'Netural',
          backgroundColor: color(window.chartColors.yellow).alpha(0.5).rgbString(),
          borderColor: window.chartColors.yellow,
          data: data_obj.y_neutral,
          type: 'line',
          pointRadius: 0,
          fill: false,
          lineTension: 0,
          borderWidth: 2
        },
        
        {
          label: 'Positive',
          backgroundColor: color(window.chartColors.green).alpha(0.5).rgbString(),
          borderColor: window.chartColors.green,
          data: data_obj.y_positive,
          type: 'line',
          pointRadius: 0,
          fill: false,
          lineTension: 0,
          borderWidth: 2
        }
        ]
        
      },
      options: {
        responsive: true,
          maintainAspectRatio: false,

        animation: {
          duration: 0
        },
        scales: {
          xAxes: [{
            type: 'time',
            distribution: 'series',
            offset: true,
            ticks: {
              major: {
                enabled: true,
                fontStyle: 'bold'
              },
              source: 'data',
              autoSkip: true,
              autoSkipPadding: 75,
              maxRotation: 0,
              sampleSize: 100
            },
            afterBuildTicks: function(scale, ticks) {
              var majorUnit = scale._majorUnit;
              var firstTick = ticks[0];
              var i, ilen, val, tick, currMajor, lastMajor;

              val = moment(ticks[0].value);
              if ((majorUnit === 'minute' && val.second() === 0)
                  || (majorUnit === 'hour' && val.minute() === 0)
                  || (majorUnit === 'day' && val.hour() === 9)
                  || (majorUnit === 'month' && val.date() <= 3 && val.isoWeekday() === 1)
                  || (majorUnit === 'year' && val.month() === 0)) {
                firstTick.major = true;
              } else {
                firstTick.major = false;
              }
              lastMajor = val.get(majorUnit);

              for (i = 1, ilen = ticks.length; i < ilen; i++) {
                tick = ticks[i];
                val = moment(tick.value);
                currMajor = val.get(majorUnit);
                tick.major = currMajor !== lastMajor;
                lastMajor = currMajor;
              }
              return ticks;
            }
          }],
          yAxes: [{
            gridLines: {
              drawBorder: false
            },
            scaleLabel: {
              display: true,
              labelString: 'Covid-19 Twitter Trend'
            }
          }]
        },
        tooltips: {
          intersect: false,
          mode: 'index',
          callbacks: {
            label: function(tooltipItem, myData) {
              var label = myData.datasets[tooltipItem.datasetIndex].label || '';
              if (label) {
                label += ': ';
              }
              label += parseFloat(tooltipItem.value).toFixed(2);
              return label;
            }
          }
        }
      }
    };

    var chart = new Chart(ctx, cfg);

    var ctx_pie = document.getElementById('chart1_pie').getContext('2d');
    var cfg_pie = {
      type: 'pie',
      data: {
        datasets: [{
          data: [
            -data_obj.y_negative[data_obj.y_negative.length - 1]["y"],
            data_obj.y_neutral[data_obj.y_neutral.length - 1]["y"],
            data_obj.y_positive[data_obj.y_positive.length - 1]["y"],
          ],
          backgroundColor: [
            window.chartColors.red,
            window.chartColors.yellow,            
            window.chartColors.green,            
          ],
          label: 'Dataset 1'
        }],
        labels: [
          'Negative',
          'Netural',
          'Positive'
        ]
      },
      options: {
        responsive: true
      }
    };


    var chart_pie = new Chart(ctx_pie, cfg_pie);

    function update_chart(){
      $.ajax({
          method: "GET",
          url: "./get_chart1_data",                    
      })
      .done(function(msg) {      
        chart.config.data.datasets[0].data = msg.y_negative;
        chart.config.data.datasets[1].data = msg.y_neutral;
        chart.config.data.datasets[2].data = msg.y_positive;
        chart.update();

        chart_pie.config.data.datasets[0].data = [
              -msg.y_negative[msg.y_negative.length - 1]["y"],
              msg.y_neutral[msg.y_neutral.length - 1]["y"],
              msg.y_positive[msg.y_positive.length - 1]["y"]
              ]
        chart_pie.update();
      })
      .fail(function(msg){
          console.log(msg);          
      });
    }

    setInterval(update_chart, 10*1000)
 
})(jQuery); // End of use strict