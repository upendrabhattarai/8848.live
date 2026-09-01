---
layout: default
title: "Rasuwa–Bhotekoshi Flash Flood, Aug 2026 · Visual Nepal"
permalink: /visual-nepal/rasuwa-bhotekoshi-flash-flood/
---

<div class="page-hero-head map-page-head">
  <h1 class="page-hero-title">
    <span data-lang-en>Rasuwa–Bhotekoshi Flash Flood<br>Aug 2026</span>
    <span data-lang-np>रसुवा–भोटेकोशी पहिरो बाढी<br>अगस्ट २०२६</span>
  </h1>
</div>

<div class="map-embed-wrap">
  <iframe src="{{ '/visual-nepal/aug2026-flash-flood.html' | relative_url }}" loading="lazy" title="Rasuwa–Bhotekoshi flash flood satellite map"></iframe>
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
  <span data-lang-en>The flood's flow path, modelled inundation extent, and infrastructure damage — mapped on satellite imagery and extracted from various sources.</span>
  <span data-lang-np>बाढीको बहाव मार्ग, अनुमानित डुबान क्षेत्र, र पूर्वाधार क्षति — स्याटेलाइट तस्बिरमा नक्सांकन गरिएको र विभिन्न स्रोतबाट संकलन गरिएको।</span>
</p>

