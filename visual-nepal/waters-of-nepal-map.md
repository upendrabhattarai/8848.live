---
layout: default
title: "The Waters of Nepal · Visual Nepal"
permalink: /visual-nepal/waters-of-nepal-map/
---

<div class="page-hero-head map-page-head">
  <h1 class="page-hero-title">
    <span data-lang-en>The Waters of Nepal</span>
    <span data-lang-np>नेपालका जलस्रोतहरू</span>
  </h1>
</div>

<div class="map-embed-wrap">
  <iframe src="{{ '/visual-nepal/waters-of-nepal.html' | relative_url }}" loading="lazy" title="Waters of Nepal satellite map"></iframe>
</div>

<script>
(function () {
  var iframe = document.currentScript.previousElementSibling.querySelector('iframe');
  var wrap = iframe.closest('.map-embed-wrap');
  wrap.style.height = '80vh';
  function resize() {
    try {
      var doc = iframe.contentWindow.document;
      var h = Math.max(doc.documentElement.scrollHeight, doc.body.scrollHeight);
      if (h > 200) { wrap.style.height = h + 'px'; }
    } catch (e) {}
  }
  iframe.addEventListener('load', function () {
    resize();
    setTimeout(resize, 500);
    setTimeout(resize, 1500);
  });
})();
</script>

<p class="page-content-lead map-page-desc">
  <span data-lang-en>A live satellite basemap of Nepal's glaciers, lakes, and rivers and more.</span>
  <span data-lang-np>नेपालका हिमनदी, ताल, नदी र थप जलस्रोतहरूको प्रत्यक्ष स्याटेलाइट आधार नक्सा।</span>
</p>

