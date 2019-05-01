// charts
gradientChartOptionsConfiguration =  {
  maintainAspectRatio: false,
  legend: {
        display: false
   },

   tooltips: {
     backgroundColor: '#fff',
     titleFontColor: '#333',
     bodyFontColor: '#666',
     bodySpacing: 4,
     xPadding: 12,
     mode: "nearest",
     intersect: 0,
     position: "nearest"
   },
   responsive: true,
   scales:{
     yAxes: [{
       barPercentage: 1.6,
           gridLines: {
             drawBorder: false,
               color: 'rgba(29,140,248,0.0)',
               zeroLineColor: "transparent",
           },
           ticks: {
             suggestedMin:50,
             suggestedMax: 110,
               padding: 20,
               fontColor: "#9a9a9a"
           }
         }],

     xAxes: [{
       barPercentage: 1.6,
           gridLines: {
             drawBorder: false,
               color: 'rgba(220,53,69,0.1)',
               zeroLineColor: "transparent",
           },
           ticks: {
               padding: 20,
               fontColor: "#9a9a9a"
           }
         }]
     }
};

gradientChartOptionsConfigurationBar =  {
  maintainAspectRatio: false,
  legend: {
        display: false
   },

   tooltips: {
     backgroundColor: '#fff',
     titleFontColor: '#333',
     bodyFontColor: '#666',
     bodySpacing: 4,
     xPadding: 12,
     mode: "nearest",
     intersect: 0,
     position: "nearest"
   },
   responsive: true,
   scales:{
     yAxes: [{
       barPercentage: 1.6,
           gridLines: {
             drawBorder: false,
               color: 'rgba(29,140,248,0.0)',
               zeroLineColor: "transparent",
           },
           ticks: {
             suggestedMin:50,
             suggestedMax: 110,
               padding: 20,
               fontColor: "#9a9a9a"
           }
         }],

     xAxes: [{
       barPercentage: 0.1,
           gridLines: {
             drawBorder: true,
               color: 'rgba(220,53,69,0.1)',
               zeroLineColor: "transparent",
           },
           ticks: {
               padding: 20,
               fontColor: "#9a9a9a"
           }
         }]
     }
};

var ctx = document.getElementById("lineChartExample").getContext("2d");
var ctxbar = document.getElementById("barChartExample").getContext("2d");
var gradientStroke = ctx.createLinearGradient(0,230,0,50);
var gradientStrokebar = ctxbar.createLinearGradient(0,230,0,50);
gradientStroke.addColorStop(1, 'rgba(2, 144, 162,0.2)');
gradientStroke.addColorStop(0.2, 'rgba(2, 144, 162,0.0)');
gradientStroke.addColorStop(0, 'rgba(2, 144, 162,0)'); //purple colors

var data = {
  labels: ['СІЧ','ЛЮТ','БЕР','КВІ','ТРА','ЧЕР','ЛИП','СЕР','ВЕР','ЖОВ','ЛИС','ГРУ'],
  datasets: [{
    label: "Кількість проданих товарів",
    fill: true,
    backgroundColor: gradientStroke,
    borderColor: '#0290a2',
    borderWidth: 2,
    borderDash: [],
    borderDashOffset: 0.0,
    pointBackgroundColor: '#0290a2',
    pointBorderColor:'rgba(255,255,255,0)',
    pointHoverBackgroundColor: '#0290a2',
    pointBorderWidth: 25,
    pointHoverRadius: 4,
    pointHoverBorderWidth: 15,
    pointRadius: 4,
    data: [ 60,110,70,100, 75, 90, 80, 100, 70, 80, 120, 80],
  }]
};

var myChart = new Chart(ctx, {
  type: 'line',
  data: data,
  options: gradientChartOptionsConfiguration
});

var myBarChart = new Chart(ctxbar, {
    type: 'bar',
    data: data,
    options: gradientChartOptionsConfigurationBar
});