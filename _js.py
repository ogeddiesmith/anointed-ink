# Front-end JS. Plain string. No backticks and no template literals anywhere, so this
# stays safe to embed in any generator.
JS = """
(function(){
 'use strict';
 var d=document;

 /* mobile nav */
 var burger=d.querySelector('.burger'), links=d.querySelector('.navlinks');
 if(burger&&links){
  burger.addEventListener('click',function(){
   var open=links.classList.toggle('open');
   burger.setAttribute('aria-expanded',open?'true':'false');
  });
  function closeNav(){ links.classList.remove('open'); burger.setAttribute('aria-expanded','false'); }
  links.addEventListener('click',function(e){ if(e.target.closest('a')) closeNav(); });
  d.addEventListener('keydown',function(e){
   if(e.key==='Escape'&&links.classList.contains('open')){ closeNav(); burger.focus(); }
  });
 }

 /* gallery filtering, with the active filter reflected in the URL hash so a
    filtered view can be linked and shared */
 var chips=[].slice.call(d.querySelectorAll('.chip'));
 var figs=[].slice.call(d.querySelectorAll('[data-styles]'));
 var countEl=d.querySelector('.count');

 function apply(tag,push){
  var shown=0;
  figs.forEach(function(f){
   var ok = tag==='all' || (' '+f.dataset.styles+' ').indexOf(' '+tag+' ')>-1;
   f.hidden=!ok; if(ok) shown++;
  });
  chips.forEach(function(c){ c.setAttribute('aria-pressed', c.dataset.filter===tag?'true':'false'); });
  if(countEl){
   var label=tag==='all'?'pieces':'pieces in this style';
   countEl.textContent='Showing '+shown+' '+label+'.';
  }
  if(push){
   if(tag==='all'){ history.replaceState(null,'',location.pathname); }
   else { history.replaceState(null,'','#'+tag); }
  }
  build();
 }
 chips.forEach(function(c){
  c.addEventListener('click',function(){ apply(c.dataset.filter,true); });
 });
 if(chips.length){
  var initial=(location.hash||'').replace('#','');
  var valid=chips.some(function(c){return c.dataset.filter===initial;});
  apply(valid?initial:'all',false);
 }

 /* lightbox */
 var lb=d.querySelector('.lb'); if(!lb) return;
 var lbImg=lb.querySelector('img'), lbCap=lb.querySelector('figcaption');
 var order=[], at=-1;

 function build(){ order=figs.filter(function(f){return !f.hidden;}); }
 build();

 function show(i){
  if(!order.length) return;
  at=(i+order.length)%order.length;
  var f=order[at];
  lbImg.src=f.dataset.full; lbImg.alt=f.dataset.alt||'';
  lbImg.width=f.dataset.fw||''; lbImg.height=f.dataset.fh||'';
  lbCap.textContent=f.dataset.caption||'';
  lb.classList.add('on'); d.body.style.overflow='hidden';
 }
 function close(){ lb.classList.remove('on'); d.body.style.overflow=''; lbImg.src=''; }

 figs.forEach(function(f){
  f.addEventListener('click',function(){ build(); show(order.indexOf(f)); });
  var btn=f.querySelector('img');
  if(btn){ btn.setAttribute('tabindex','0'); }
  f.addEventListener('keydown',function(e){
   if(e.key==='Enter'||e.key===' '){ e.preventDefault(); build(); show(order.indexOf(f)); }
  });
 });
 lb.addEventListener('click',function(e){ if(e.target===lb) close(); });
 lb.querySelector('.x').addEventListener('click',close);
 lb.querySelector('.prev').addEventListener('click',function(e){e.stopPropagation();show(at-1);});
 lb.querySelector('.next').addEventListener('click',function(e){e.stopPropagation();show(at+1);});
 d.addEventListener('keydown',function(e){
  if(!lb.classList.contains('on')) return;
  if(e.key==='Escape') close();
  if(e.key==='ArrowLeft') show(at-1);
  if(e.key==='ArrowRight') show(at+1);
 });

 /* swipe on touch */
 var x0=null;
 lb.addEventListener('touchstart',function(e){ x0=e.changedTouches[0].clientX; },{passive:true});
 lb.addEventListener('touchend',function(e){
  if(x0===null) return;
  var dx=e.changedTouches[0].clientX-x0;
  if(Math.abs(dx)>48) show(dx>0?at-1:at+1);
  x0=null;
 },{passive:true});
})();
"""
