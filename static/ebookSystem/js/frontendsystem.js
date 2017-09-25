'use strict';

let dffesc = $.Deferred();
$(document).ready(function(){
    let url='/static/ebookSystem/js/frontendsystem-core.js';
    let timetag='?'+Date.now();
    $.getScript(url+timetag)
    .done(function(){
        dffesc.resolve();
    });
})

