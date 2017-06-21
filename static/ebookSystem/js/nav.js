$( document ).ready(function() {
  $('ul[class="dropdown-menu"]').each(function(){
    let ul=$(this);
    let cd=ul.children();
    if(cd.length===0){
        ul.parent().remove();
    }
  })
});
