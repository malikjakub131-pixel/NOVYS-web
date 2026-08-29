/* =========================================================
   NOVYS s.r.o. — hlavný JS
   ========================================================= */
(function(){
  "use strict";

  document.addEventListener("DOMContentLoaded", init);

  function init(){
    initHeader();
    initMobileNav();
    initHeroSlider();
    initReveal();
    initCounters();
    initBeforeAfter();
    initCalculator();
    initProjectFilter();
    initPillGroups();
    initFooterYear();
    initLightbox();
    initFileInput();
    initAccordion();
  }

  /* ---------------- FAQ accordion ---------------- */
  function initAccordion(){
    var items = document.querySelectorAll(".faq-item");
    if(!items.length) return;
    items.forEach(function(item){
      var q = item.querySelector(".faq-q");
      q.addEventListener("click", function(){
        var wasOpen = item.classList.contains("is-open");
        items.forEach(function(i){ i.classList.remove("is-open"); });
        if(!wasOpen) item.classList.add("is-open");
      });
    });
  }

  /* ---------------- Lightbox ---------------- */
  function initLightbox(){
    var all = document.querySelectorAll("[data-lightbox]");
    if(!all.length) return;

    // navigujeme v ramci galerie (ak existuje), inak medzi vsetkymi obrazkami na stranke
    var gallery = document.querySelector(".gallery-strip");
    var groupEls = gallery ? gallery.querySelectorAll("[data-lightbox]") : all;
    var group = Array.prototype.slice.call(groupEls).map(function(el){
      return { src: el.getAttribute("data-lightbox") || el.src, alt: el.alt || "" };
    });

    var overlay = document.createElement("div");
    overlay.className = "lightbox-overlay";
    overlay.innerHTML =
      '<button class="lightbox-close" aria-label="Zavrieť"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg></button>' +
      '<button class="lightbox-nav lightbox-prev" aria-label="Predchádzajúca fotka"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg></button>' +
      '<button class="lightbox-nav lightbox-next" aria-label="Ďalšia fotka"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg></button>' +
      '<img alt="">' +
      '<div class="lightbox-count"></div>';
    document.body.appendChild(overlay);
    var img = overlay.querySelector("img");
    var countEl = overlay.querySelector(".lightbox-count");
    var prevBtn = overlay.querySelector(".lightbox-prev");
    var nextBtn = overlay.querySelector(".lightbox-next");

    var current = 0;
    var activeGroup = group;

    function show(idx){
      if(!activeGroup.length) return;
      current = (idx + activeGroup.length) % activeGroup.length;
      var item = activeGroup[current];
      img.src = item.src;
      img.alt = item.alt;
      var multi = activeGroup.length > 1;
      prevBtn.style.display = multi ? "" : "none";
      nextBtn.style.display = multi ? "" : "none";
      countEl.style.display = multi ? "" : "none";
      countEl.textContent = (current + 1) + " / " + activeGroup.length;
    }

    function open(src, alt, list){
      activeGroup = (list && list.length) ? list : [{ src: src, alt: alt || "" }];
      var idx = 0;
      for(var i = 0; i < activeGroup.length; i++){
        if(activeGroup[i].src === src){ idx = i; break; }
      }
      show(idx);
      overlay.classList.add("is-open");
      document.body.style.overflow = "hidden";
    }
    function close(){
      overlay.classList.remove("is-open");
      document.body.style.overflow = "";
    }

    all.forEach(function(el){
      el.addEventListener("click", function(){
        var full = el.getAttribute("data-lightbox") || el.src;
        var inGroup = group.some(function(g){ return g.src === full; });
        open(full, el.alt, inGroup ? group : null);
      });
    });
    prevBtn.addEventListener("click", function(e){ e.stopPropagation(); show(current - 1); });
    nextBtn.addEventListener("click", function(e){ e.stopPropagation(); show(current + 1); });
    overlay.addEventListener("click", function(e){ if(e.target === overlay) close(); });
    overlay.querySelector(".lightbox-close").addEventListener("click", close);
    window.addEventListener("keydown", function(e){
      if(!overlay.classList.contains("is-open")) return;
      if(e.key === "Escape") close();
      else if(e.key === "ArrowLeft") show(current - 1);
      else if(e.key === "ArrowRight") show(current + 1);
    });

    // swipe na mobile
    var touchX = null;
    overlay.addEventListener("touchstart", function(e){ touchX = e.touches[0].clientX; }, {passive:true});
    overlay.addEventListener("touchend", function(e){
      if(touchX === null) return;
      var dx = e.changedTouches[0].clientX - touchX;
      if(Math.abs(dx) > 40){ dx < 0 ? show(current + 1) : show(current - 1); }
      touchX = null;
    }, {passive:true});
  }

  /* ---------------- File input label ---------------- */
  function initFileInput(){
    document.querySelectorAll(".file-drop input[type=file]").forEach(function(input){
      var hint = input.parentElement.querySelector("[data-file-hint]");
      if(!hint) return;
      input.addEventListener("change", function(){
        if(input.files && input.files.length){
          hint.textContent = input.files[0].name;
        }
      });
    });
  }

  /* ---------------- Header scroll state ---------------- */
  function initHeader(){
    var header = document.querySelector(".site-header");
    if(!header) return;
    function onScroll(){
      if(window.scrollY > 40){ header.classList.add("is-scrolled"); }
      else{ header.classList.remove("is-scrolled"); }
    }
    onScroll();
    window.addEventListener("scroll", onScroll, {passive:true});
  }

  /* ---------------- Mobile nav ---------------- */
  function initMobileNav(){
    var toggle = document.querySelector(".nav-toggle");
    var nav = document.querySelector(".main-nav");
    var closeBtn = document.querySelector(".nav-close");
    var header = document.querySelector(".site-header");
    if(!toggle || !nav) return;

    function open(){
      nav.classList.add("is-open");
      document.body.style.overflow = "hidden";
      if(header) header.classList.add("menu-open");
    }
    function close(){
      nav.classList.remove("is-open");
      document.body.style.overflow = "";
      if(header) header.classList.remove("menu-open");
    }

    toggle.addEventListener("click", function(){
      nav.classList.contains("is-open") ? close() : open();
    });
    if(closeBtn) closeBtn.addEventListener("click", close);

    document.querySelectorAll(".main-nav a:not(.has-drop > a)").forEach(function(link){
      link.addEventListener("click", close);
    });

    window.addEventListener("keydown", function(e){
      if(e.key === "Escape") close();
    });

    var isMobile = function(){ return window.innerWidth <= 980; };
    document.querySelectorAll(".has-drop > a").forEach(function(link){
      link.addEventListener("click", function(e){
        if(!isMobile()) return;
        e.preventDefault();
        link.parentElement.classList.toggle("open");
      });
    });
  }

  /* ---------------- Hero slider ---------------- */
  function initHeroSlider(){
    var slides = document.querySelectorAll(".hero-slide");
    var dots = document.querySelectorAll(".hero-dots button");
    if(!slides.length) return;
    var i = 0;
    function show(idx){
      slides.forEach(function(s,n){ s.classList.toggle("is-active", n===idx); });
      dots.forEach(function(d,n){ d.classList.toggle("is-active", n===idx); });
      i = idx;
    }
    dots.forEach(function(d,n){
      d.addEventListener("click", function(){ show(n); restart(); });
    });
    var timer;
    function restart(){
      clearInterval(timer);
      timer = setInterval(function(){ show((i+1) % slides.length); }, 5500);
    }
    restart();
  }

  /* ---------------- Reveal on scroll ---------------- */
  function initReveal(){
    var els = document.querySelectorAll(".reveal");
    if(!els.length) return;
    if(!("IntersectionObserver" in window)){
      els.forEach(function(el){ el.classList.add("is-visible"); });
      return;
    }
    var obs = new IntersectionObserver(function(entries){
      entries.forEach(function(entry){
        if(entry.isIntersecting){
          entry.target.classList.add("is-visible");
          obs.unobserve(entry.target);
        }
      });
    }, {threshold:.15, rootMargin:"0px 0px -60px 0px"});
    els.forEach(function(el){ obs.observe(el); });
  }

  /* ---------------- Counters ---------------- */
  function initCounters(){
    var els = document.querySelectorAll("[data-count]");
    if(!els.length) return;
    var run = function(el){
      var target = parseFloat(el.getAttribute("data-count"));
      var dur = 1400, start = null;
      function step(ts){
        if(!start) start = ts;
        var p = Math.min((ts-start)/dur, 1);
        var eased = 1 - Math.pow(1-p, 3);
        var val = target * eased;
        el.textContent = target % 1 !== 0 ? val.toFixed(1) : Math.round(val);
        if(p < 1) requestAnimationFrame(step);
        else el.textContent = target % 1 !== 0 ? target.toFixed(1) : target;
      }
      requestAnimationFrame(step);
    };
    if(!("IntersectionObserver" in window)){ els.forEach(run); return; }
    var obs = new IntersectionObserver(function(entries){
      entries.forEach(function(entry){
        if(entry.isIntersecting){ run(entry.target); obs.unobserve(entry.target); }
      });
    }, {threshold:.6});
    els.forEach(function(el){ obs.observe(el); });
  }

  /* ---------------- Before / after slider ---------------- */
  function initBeforeAfter(){
    var groups = document.querySelectorAll("[data-ba-group]");
    groups.forEach(function(group){
      var tabs = group.querySelectorAll(".ba-tab");
      var sliders = group.querySelectorAll(".ba-slider");
      tabs.forEach(function(tab){
        tab.addEventListener("click", function(){
          var target = tab.getAttribute("data-target");
          tabs.forEach(function(t){ t.classList.toggle("is-active", t===tab); });
          sliders.forEach(function(s){ s.classList.toggle("is-active", s.getAttribute("data-pair")===target); });
        });
      });
    });

    document.querySelectorAll(".ba-slider").forEach(setupSlider);

    function setupSlider(slider){
      var dragging = false;

      function setPos(pct){
        pct = Math.max(2, Math.min(98, pct));
        slider.style.setProperty("--pos", pct + "%");
      }

      function fromEvent(clientX){
        var rect = slider.getBoundingClientRect();
        var pct = ((clientX - rect.left) / rect.width) * 100;
        setPos(pct);
      }

      slider.addEventListener("mousedown", function(e){ dragging = true; fromEvent(e.clientX); e.preventDefault(); });
      window.addEventListener("mousemove", function(e){ if(dragging) fromEvent(e.clientX); });
      window.addEventListener("mouseup", function(){ dragging = false; });

      slider.addEventListener("touchstart", function(e){ dragging = true; fromEvent(e.touches[0].clientX); }, {passive:true});
      slider.addEventListener("touchmove", function(e){ if(dragging) fromEvent(e.touches[0].clientX); }, {passive:true});
      slider.addEventListener("touchend", function(){ dragging = false; });

      setPos(50);
    }
  }

  /* ---------------- Price calculator ---------------- */
  function initCalculator(){
    var calc = document.querySelector("[data-calculator]");
    if(!calc) return;

    var areaInput = calc.querySelector("[data-area]");
    var areaVal = calc.querySelector("[data-area-val]");
    var typeBtns = calc.querySelectorAll("[data-type]");
    var roofBtns = calc.querySelectorAll("[data-roof]");
    var priceEl = calc.querySelector("[data-price]");
    var rowArea = calc.querySelector("[data-row-area]");
    var rowType = calc.querySelector("[data-row-type]");
    var rowRoof = calc.querySelector("[data-row-roof]");

    var basePerM2 = { murovana: 780, monolit: 900, kombinacia: 840 };
    var typeLabel = { murovana: "Murovaná", monolit: "Monolitická", kombinacia: "Kombinovaná" };
    var roofLabel = { ano: "Vrátane strechy", nie: "Bez strechy" };

    var state = { area: parseInt(areaInput.value, 10), type: "murovana", roof: "ano" };

    function fmt(n){ return n.toLocaleString("sk-SK"); }

    function update(){
      areaVal.textContent = state.area + " m²";
      var perM2 = basePerM2[state.type];
      var subtotal = perM2 * state.area;
      var roofFactor = state.roof === "ano" ? 1 : 0.78;
      var total = subtotal * roofFactor;
      var low = Math.round((total*0.92)/100)*100;
      var high = Math.round((total*1.1)/100)*100;

      priceEl.textContent = fmt(low) + " € – " + fmt(high) + " €";
      if(rowArea) rowArea.textContent = state.area + " m²";
      if(rowType) rowType.textContent = typeLabel[state.type];
      if(rowRoof) rowRoof.textContent = roofLabel[state.roof];
    }

    areaInput.addEventListener("input", function(){
      state.area = parseInt(areaInput.value, 10);
      update();
    });
    typeBtns.forEach(function(btn){
      btn.addEventListener("click", function(){
        typeBtns.forEach(function(b){ b.classList.remove("is-active"); });
        btn.classList.add("is-active");
        state.type = btn.getAttribute("data-type");
        update();
      });
    });
    roofBtns.forEach(function(btn){
      btn.addEventListener("click", function(){
        roofBtns.forEach(function(b){ b.classList.remove("is-active"); });
        btn.classList.add("is-active");
        state.roof = btn.getAttribute("data-roof");
        update();
      });
    });

    update();
  }

  /* ---------------- Projects filter ---------------- */
  function initProjectFilter(){
    var bar = document.querySelector("[data-filter-bar]");
    if(!bar) return;
    var buttons = bar.querySelectorAll(".filter-btn");
    var cards = document.querySelectorAll("[data-cats]");

    buttons.forEach(function(btn){
      btn.addEventListener("click", function(){
        buttons.forEach(function(b){ b.classList.remove("is-active"); });
        btn.classList.add("is-active");
        var filter = btn.getAttribute("data-filter");
        cards.forEach(function(card){
          var cats = card.getAttribute("data-cats") || "";
          var show = filter === "all" || cats.indexOf(filter) !== -1;
          card.classList.toggle("hide", !show);
        });
      });
    });

    var params = new URLSearchParams(window.location.search);
    var pre = params.get("kategoria");
    if(pre){
      var match = bar.querySelector('[data-filter="'+pre+'"]');
      if(match) match.click();
    }
  }

  /* ---------------- Pill radio groups (form) ---------------- */
  function initPillGroups(){
    document.querySelectorAll(".pill-group").forEach(function(group){
      var pills = group.querySelectorAll(".pill");
      pills.forEach(function(pill){
        var input = pill.querySelector("input");
        if(!input) return;
        var sync = function(){ pill.classList.toggle("is-checked", input.checked); };
        input.addEventListener("change", function(){
          if(input.type === "radio"){
            pills.forEach(function(p){ p.classList.remove("is-checked"); });
          }
          sync();
        });
        sync();
      });
    });
  }

  function initFooterYear(){
    document.querySelectorAll("[data-year]").forEach(function(el){
      el.textContent = new Date().getFullYear();
    });
  }

})();
