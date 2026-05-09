/* Pixelschneiderei – shared JS */
(function(){
  // year
  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();

  // sticky nav shadow
  var nav = document.getElementById('nav');
  if (nav){
    var onScroll = function(){ nav.classList.toggle('is-scrolled', window.scrollY > 8); };
    window.addEventListener('scroll', onScroll, {passive:true});
    onScroll();

    // mobile nav
    var toggle = document.getElementById('navToggle');
    if (toggle){
      toggle.addEventListener('click', function(){
        var open = nav.classList.toggle('is-open');
        toggle.setAttribute('aria-expanded', String(open));
      });
    }
    var navLinks = nav.querySelectorAll('.nav-links a');
    navLinks.forEach(function(a){ a.addEventListener('click', function(){ nav.classList.remove('is-open'); }); });
  }

  // reveal on scroll
  var io = new IntersectionObserver(function(entries){
    for (var i=0;i<entries.length;i++){
      var e = entries[i];
      if (e.isIntersecting){ e.target.classList.add('is-visible'); io.unobserve(e.target); }
    }
  }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
  document.querySelectorAll('.reveal').forEach(function(el){ io.observe(el); });
})();
