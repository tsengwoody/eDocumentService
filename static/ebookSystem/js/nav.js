$( document ).ready(function() {
  $('ul[class="dropdown-menu"]').find('li').each(function(){
    let li=$(this);
    let a=li.children();
    if(a.attr('href')===''){
        li.remove();
    }
  })
});
