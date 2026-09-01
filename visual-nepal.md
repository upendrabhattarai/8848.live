---
layout: default
title: Visual Nepal
permalink: /visual-nepal/
---

<div class="page-hero-head">
  <h1 class="page-hero-title">
    <span data-lang-en>Nepal in Visual</span>
    <span data-lang-np>दृश्यमा नेपाल</span>
  </h1>
  <p class="page-hero-subtitle">
    <span data-lang-en>Data on the map of Nepal.</span>
    <span data-lang-np>नेपालको नक्सामा तथ्याङ्क।</span>
  </p>
</div>

<div class="visual-nepal-grid">
  <a class="visual-card" href="{{ '/visual-nepal/rasuwa-bhotekoshi-flash-flood/' | relative_url }}">
    <div class="visual-card-body">
      <h2 class="visual-card-title">
        <span data-lang-en>Rasuwa–Bhotekoshi Flash Flood<br>Aug 2026</span>
        <span data-lang-np>रसुवा–भोटेकोशी पहिरो बाढी<br>अगस्ट २०२६</span>
      </h2>
    </div>
    <div class="visual-card-preview" data-native-w="1440" data-native-h="900" data-crop-x="380">
      <iframe src="{{ '/visual-nepal/aug2026-flash-flood.html' | relative_url }}" loading="lazy" tabindex="-1" title="Rasuwa–Bhotekoshi flash flood satellite map preview"></iframe>
    </div>
    <div class="visual-card-footer">
      <p class="visual-card-desc">
        <span data-lang-en>The flood's flow path, modelled inundation extent, and infrastructure damage — mapped on satellite imagery and extracted from various sources.</span>
        <span data-lang-np>बाढीको बहाव मार्ग, अनुमानित डुबान क्षेत्र, र पूर्वाधार क्षति — स्याटेलाइट तस्बिरमा नक्सांकन गरिएको र विभिन्न स्रोतबाट संकलन गरिएको।</span>
      </p>
      <span class="visual-card-cta">
        <span data-lang-en>Open the full map →</span>
        <span data-lang-np>पूरा नक्सा खोल्नुहोस् →</span>
      </span>
    </div>
  </a>

  <a class="visual-card" href="{{ '/visual-nepal/waters-of-nepal-map/' | relative_url }}">
    <div class="visual-card-body">
      <h2 class="visual-card-title">
        <span data-lang-en>The Waters of Nepal</span>
        <span data-lang-np>नेपालका जलस्रोतहरू</span>
      </h2>
    </div>
    <div class="visual-card-preview" data-native-w="1440" data-native-h="900" data-crop-x="0">
      <iframe src="{{ '/visual-nepal/waters-of-nepal.html' | relative_url }}" loading="lazy" tabindex="-1" title="Waters of Nepal satellite map preview"></iframe>
    </div>
    <div class="visual-card-footer">
      <p class="visual-card-desc">
        <span data-lang-en>A live satellite basemap of Nepal's glaciers, lakes, and rivers and more.</span>
        <span data-lang-np>नेपालका हिमनदी, ताल, नदी र थप जलस्रोतहरूको प्रत्यक्ष स्याटेलाइट आधार नक्सा।</span>
      </p>
      <span class="visual-card-cta">
        <span data-lang-en>Open the full map →</span>
        <span data-lang-np>पूरा नक्सा खोल्नुहोस् →</span>
      </span>
    </div>
  </a>
</div>

<script>
(function () {
  function fit(box) {
    var iframe = box.querySelector('iframe');
    if (!iframe) return;
    var nativeW = parseInt(box.dataset.nativeW, 10) || 1440;
    var nativeH = parseInt(box.dataset.nativeH, 10) || 900;
    var cropX = parseInt(box.dataset.cropX, 10) || 0;
    var visibleW = nativeW - cropX;
    var scale = box.clientWidth / visibleW;
    iframe.style.width = nativeW + 'px';
    iframe.style.height = nativeH + 'px';
    iframe.style.transform = 'scale(' + scale + ')';
    iframe.style.left = (-cropX * scale) + 'px';
  }
  function fitAll() {
    document.querySelectorAll('.visual-card-preview').forEach(fit);
  }
  fitAll();
  var t;
  window.addEventListener('resize', function () {
    clearTimeout(t);
    t = setTimeout(fitAll, 150);
  });
})();
</script>
