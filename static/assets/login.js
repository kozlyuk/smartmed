// window.onload = function() {
//     document.querySelector(".cont_modal").className = "cont_modal";
//   };
//   var c = 0;
//   function open_close() {
//     if (c % 2 == 0) {
//       document.querySelector(".cont_modal").className =
//         "cont_modal cont_modal_active";
//       c++;
//     } else {
//       document.querySelector(".cont_modal").className = "cont_modal";
//       c++;
//     }
//   }
  

// "use strict";
// webix.ui({
// rows:[
//   { view:"template", 
//     type:"header", template:"My App!" },
//   { view:"datatable", 
//     autoConfig:true, 
//     data:{
//       title:"My Fair Lady", year:1964, votes:533848, rating:8.9, rank:5
//     }
//   }
// ]
// });

window.onload=function(){
var current = null;
document.querySelector('#email').addEventListener('focus', function(e) {
  if (current) current.pause();
  current = anime({
    targets: 'path',
    strokeDashoffset: {
      value: 0,
      duration: 700,
      easing: 'easeOutQuart'
    },
    strokeDasharray: {
      value: '240 1386',
      duration: 700,
      easing: 'easeOutQuart'
    }
  });
});
document.querySelector('#password').addEventListener('focus', function(e) {
if (current) current.pause();
  current = anime({
    targets: 'path',
    strokeDashoffset: {
      value: -336,
      duration: 700,
      easing: 'easeOutQuart'
    },
    strokeDasharray: {
      value: '240 1386',
      duration: 700,
      easing: 'easeOutQuart'
    }
  });
});
document.querySelector('#submit').addEventListener('focus', function(e) {
  if (current) current.pause();
  current = anime({
    targets: 'path',
    strokeDashoffset: {
      value: -730,
      duration: 700,
      easing: 'easeOutQuart'
    },
    strokeDasharray: {
      value: '530 1386',
      duration: 700,
      easing: 'easeOutQuart'
    }
  });
});
document.querySelector('#registration').addEventListener('focus', function(e) {
  if (current) current.pause();
  current = anime({
    targets: 'path',
    strokeDashoffset: {
      value: -730,
      duration: 700,
      easing: 'easeOutQuart'
    },
    strokeDasharray: {
      value: '530 1386',
      duration: 700,
      easing: 'easeOutQuart'
    }
  });
});
}