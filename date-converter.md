---
layout: default
title: Date Converter
permalink: /date-converter/
image: /assets/shares/date-converter.png
description: Convert between the English (AD) and Nepali Bikram Sambat (BS) calendars, and browse both side by side.
---

<div class="page-hero-head">
  <h1 class="page-hero-title">
    <span data-lang-en>Date Converter</span>
    <span data-lang-np>मिति परिवर्तक</span>
  </h1>
  <p class="page-hero-subtitle">
    <span data-lang-en>Convert between the English (AD) and Nepali Bikram Sambat (BS) calendars, and browse both side by side.</span>
    <span data-lang-np>अंग्रेजी (AD) र नेपाली विक्रम संवत् (BS) पात्रोबीच मिति रूपान्तरण गर्नुहोस्, र दुवैलाई छेउछेउ हेर्नुहोस्।</span>
  </p>
</div>

<div class="converter-card" id="date-converter">
  <div class="converter-tabs">
    <button type="button" class="converter-tab active" data-mode="ad-to-bs">
      <span data-lang-en>English → Nepali</span>
      <span data-lang-np>अंग्रेजी → नेपाली</span>
    </button>
    <button type="button" class="converter-tab" data-mode="bs-to-ad">
      <span data-lang-en>Nepali → English</span>
      <span data-lang-np>नेपाली → अंग्रेजी</span>
    </button>
  </div>

  <div class="converter-panel" id="panel-ad-to-bs">
    <label class="converter-label" for="ad-date-input">
      <span data-lang-en>English date</span>
      <span data-lang-np>अंग्रेजी मिति</span>
    </label>
    <input type="date" id="ad-date-input" class="converter-input" min="1943-04-14" max="2034-04-13">
  </div>

  <div class="converter-panel" id="panel-bs-to-ad" hidden>
    <label class="converter-label">
      <span data-lang-en>Nepali date</span>
      <span data-lang-np>नेपाली मिति</span>
    </label>
    <div class="converter-select-row">
      <select id="bs-year-select" class="converter-select" aria-label="BS year"></select>
      <select id="bs-month-select" class="converter-select" aria-label="BS month"></select>
      <select id="bs-day-select" class="converter-select" aria-label="BS day"></select>
    </div>
  </div>

  <div class="converter-result" id="converter-result">
    <div class="converter-result-bs">
      <span class="converter-result-label">
        <span data-lang-en>Bikram Sambat</span>
        <span data-lang-np>विक्रम संवत्</span>
      </span>
      <span class="converter-result-value" id="result-bs-value">—</span>
    </div>
    <div class="converter-result-divider">⇄</div>
    <div class="converter-result-ad">
      <span class="converter-result-label">
        <span data-lang-en>English (AD)</span>
        <span data-lang-np>अंग्रेजी (AD)</span>
      </span>
      <span class="converter-result-value" id="result-ad-value">—</span>
    </div>
  </div>

  <button type="button" class="converter-today-btn" id="converter-today-btn">
    <span data-lang-en>Today</span>
    <span data-lang-np>आज</span>
  </button>
</div>

<div class="tool-share-row">
  <button type="button" class="share-btn" data-share="twitter" aria-label="Share on X">
    <svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.9 2H22l-7.6 8.7L23.3 22h-7l-5.5-6.8L4.5 22H1.4l8.2-9.3L1 2h7.2l5 6.3L18.9 2Zm-1.2 18h1.7L7.4 4H5.6L17.7 20Z"/></svg>
  </button>
  <button type="button" class="share-btn" data-share="facebook" aria-label="Share on Facebook">
    <svg viewBox="0 0 24 24" fill="currentColor"><path d="M22 12a10 10 0 1 0-11.6 9.9v-7H7.9V12h2.5V9.8c0-2.5 1.5-3.9 3.8-3.9 1.1 0 2.2.2 2.2.2v2.4h-1.3c-1.2 0-1.6.8-1.6 1.6V12h2.8l-.4 2.9h-2.4v7A10 10 0 0 0 22 12Z"/></svg>
  </button>
  <button type="button" class="share-btn" data-share="instagram" aria-label="Share on Instagram">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.2" cy="6.8" r="1"/></svg>
  </button>
</div>

<script>
(function () {
  var shareUrl = 'https://8848.live/share/date-converter/';
  var text = 'Date Converter (AD ↔ BS) — via 8848.live';
  var row = document.currentScript.previousElementSibling;
  if (!row || !row.classList.contains('tool-share-row')) {
    row = document.querySelector('.tool-share-row');
  }
  if (!row) return;
  row.addEventListener('click', function (e) {
    var btn = e.target.closest('.share-btn');
    if (!btn) return;
    var kind = btn.getAttribute('data-share');
    if (kind === 'twitter') {
      window.open('https://twitter.com/intent/tweet?text=' + encodeURIComponent(text) + '&url=' + encodeURIComponent(shareUrl), '_blank', 'noopener,width=600,height=520');
    } else if (kind === 'facebook') {
      window.open('https://www.facebook.com/sharer/sharer.php?u=' + encodeURIComponent(shareUrl), '_blank', 'noopener,width=600,height=520');
    } else if (kind === 'instagram') {
      window.open('https://8848.live/assets/shares/date-converter.png', '_blank', 'noopener');
    }
  });
})();
</script>

<div class="calendars-grid">
  <div class="mini-calendar" id="calendar-ad">
    <div class="mini-calendar-head">
      <button type="button" class="cal-nav" data-cal="ad" data-dir="-1" aria-label="Previous month">‹</button>
      <span class="mini-calendar-title" id="cal-ad-title"></span>
      <button type="button" class="cal-nav" data-cal="ad" data-dir="1" aria-label="Next month">›</button>
    </div>
    <div class="mini-calendar-weekdays" id="cal-ad-weekdays"></div>
    <div class="mini-calendar-grid" id="cal-ad-grid"></div>
  </div>
  <div class="mini-calendar" id="calendar-bs">
    <div class="mini-calendar-head">
      <button type="button" class="cal-nav" data-cal="bs" data-dir="-1" aria-label="Previous month">‹</button>
      <span class="mini-calendar-title" id="cal-bs-title"></span>
      <button type="button" class="cal-nav" data-cal="bs" data-dir="1" aria-label="Next month">›</button>
    </div>
    <div class="mini-calendar-weekdays" id="cal-bs-weekdays"></div>
    <div class="mini-calendar-grid" id="cal-bs-grid"></div>
  </div>
</div>


<script>
(function () {
  // ---------------------------------------------------------------------
  // Bikram Sambat <-> Gregorian conversion. Day-count-per-month table for
  // BS 2000-2090 adapted from the nepali-date-converter project (MIT
  // licensed) -- https://github.com/remotemerge/nepali-date-converter.
  // Epoch: BS 2000/01/01 (Baisakh 1) = AD 1943-04-14.
  // ---------------------------------------------------------------------
  var BS_DAYS = [[30,32,31,32,31,30,30,30,29,30,29,31],[31,31,32,31,31,31,30,29,30,29,30,30],[31,31,32,32,31,30,30,29,30,29,30,30],[31,32,31,32,31,30,30,30,29,29,30,31],[30,32,31,32,31,30,30,30,29,30,29,31],[31,31,32,31,31,31,30,29,30,29,30,30],[31,31,32,32,31,30,30,29,30,29,30,30],[31,32,31,32,31,30,30,30,29,29,30,31],[31,31,31,32,31,31,29,30,30,29,29,31],[31,31,32,31,31,31,30,29,30,29,30,30],[31,31,32,32,31,30,30,29,30,29,30,30],[31,32,31,32,31,30,30,30,29,29,30,31],[31,31,31,32,31,31,29,30,30,29,30,30],[31,31,32,31,31,31,30,29,30,29,30,30],[31,31,32,32,31,30,30,29,30,29,30,30],[31,32,31,32,31,30,30,30,29,29,30,31],[31,31,31,32,31,31,29,30,30,29,30,30],[31,31,32,31,31,31,30,29,30,29,30,30],[31,32,31,32,31,30,30,29,30,29,30,30],[31,32,31,32,31,30,30,30,29,30,29,31],[31,31,31,32,31,31,30,29,30,29,30,30],[31,31,32,31,31,31,30,29,30,29,30,30],[31,32,31,32,31,30,30,30,29,29,30,30],[31,32,31,32,31,30,30,30,29,30,29,31],[31,31,31,32,31,31,30,29,30,29,30,30],[31,31,32,31,31,31,30,29,30,29,30,30],[31,32,31,32,31,30,30,30,29,29,30,31],[30,32,31,32,31,30,30,30,29,30,29,31],[31,31,32,31,31,31,30,29,30,29,30,30],[31,31,32,31,32,30,30,29,30,29,30,30],[31,32,31,32,31,30,30,30,29,29,30,31],[30,32,31,32,31,30,30,30,29,30,29,31],[31,31,32,31,31,31,30,29,30,29,30,30],[31,31,32,32,31,30,30,29,30,29,30,30],[31,32,31,32,31,30,30,30,29,29,30,31],[30,32,31,32,31,31,29,30,30,29,29,31],[31,31,32,31,31,31,30,29,30,29,30,30],[31,31,32,32,31,30,30,29,30,29,30,30],[31,32,31,32,31,30,30,30,29,29,30,31],[31,31,31,32,31,31,29,30,30,29,30,30],[31,31,32,31,31,31,30,29,30,29,30,30],[31,31,32,32,31,30,30,29,30,29,30,30],[31,32,31,32,31,30,30,30,29,29,30,31],[31,31,31,32,31,31,29,30,30,29,30,30],[31,31,32,31,31,31,30,29,30,29,30,30],[31,32,31,32,31,30,30,29,30,29,30,30],[31,32,31,32,31,30,30,30,29,29,30,31],[31,31,31,32,31,31,30,29,30,29,30,30],[31,31,32,31,31,31,30,29,30,29,30,30],[31,32,31,32,31,30,30,30,29,29,30,30],[31,32,31,32,31,30,30,30,29,30,29,31],[31,31,31,32,31,31,30,29,30,29,30,30],[31,31,32,31,31,31,30,29,30,29,30,30],[31,32,31,32,31,30,30,30,29,29,30,30],[31,32,31,32,31,30,30,30,29,30,29,31],[31,31,32,31,31,31,30,29,30,29,30,30],[31,31,32,31,32,30,30,29,30,29,30,30],[31,32,31,32,31,30,30,30,29,29,30,31],[30,32,31,32,31,30,30,30,29,30,29,31],[31,31,32,31,31,31,30,29,30,29,30,30],[31,31,32,32,31,30,30,29,30,29,30,30],[31,32,31,32,31,30,30,30,29,29,30,31],[30,32,31,32,31,31,29,30,29,30,29,31],[31,31,32,31,31,31,30,29,30,29,30,30],[31,31,32,32,31,30,30,29,30,29,30,30],[31,32,31,32,31,30,30,30,29,29,30,31],[31,31,31,32,31,31,29,30,30,29,29,31],[31,31,32,31,31,31,30,29,30,29,30,30],[31,31,32,32,31,30,30,29,30,29,30,30],[31,32,31,32,31,30,30,30,29,29,30,31],[31,31,31,32,31,31,29,30,30,29,30,30],[31,31,32,31,31,31,30,29,30,29,30,30],[31,32,31,32,31,30,30,29,30,29,30,30],[31,32,31,32,31,30,30,30,29,29,30,31],[31,31,31,32,31,31,30,29,30,29,30,30],[31,31,32,31,31,31,30,29,30,29,30,30],[31,32,31,32,31,30,30,30,29,29,30,30],[31,32,31,32,31,30,30,30,29,30,29,31],[31,31,31,32,31,31,30,29,30,29,30,30],[31,31,32,31,31,31,30,29,30,29,30,30],[31,32,31,32,31,30,30,30,29,29,30,30],[31,32,31,32,31,30,30,30,29,30,29,31],[31,31,32,31,31,31,30,29,30,29,30,30],[31,31,32,31,31,31,30,29,30,29,30,30],[31,32,31,32,31,30,30,30,29,29,30,31],[30,32,31,32,31,30,30,30,29,30,29,31],[31,31,32,31,31,31,30,29,30,29,30,30],[31,31,32,31,31,31,30,30,29,30,30,30],[30,31,32,32,30,31,30,30,29,30,30,30],[30,32,31,32,31,30,30,30,29,30,30,30],[30,32,31,32,31,30,30,30,29,30,30,30]];
  var BS_EPOCH_YEAR = 2000;
  var BS_MIN_YEAR = 2000, BS_MAX_YEAR = 2090;
  var AD_EPOCH_MS = Date.UTC(1943, 3, 13);

  var yearTotals = BS_DAYS.map(function (y) { return y.reduce(function (a, b) { return a + b; }, 0); });
  var yearCumBefore = [];
  (function () { var acc = 0; for (var i = 0; i < yearTotals.length; i++) { yearCumBefore.push(acc); acc += yearTotals[i]; } })();
  var monthCumBefore = BS_DAYS.map(function (months) {
    var acc = 0, out = [];
    for (var i = 0; i < months.length; i++) { out.push(acc); acc += months[i]; }
    return out;
  });

  function bsToDaysPassed(year, month, date) {
    var yi = year - BS_EPOCH_YEAR;
    return yearCumBefore[yi] + monthCumBefore[yi][month] + date;
  }
  function daysPassedToBS(daysPassed) {
    var yi = 0;
    for (var i = 0; i < yearCumBefore.length; i++) {
      if (daysPassed > yearCumBefore[i] && daysPassed <= yearCumBefore[i] + yearTotals[i]) { yi = i; break; }
    }
    var rem = daysPassed - yearCumBefore[yi];
    var mi = 0, months = BS_DAYS[yi];
    for (var j = 0; j < months.length; j++) {
      if (rem > monthCumBefore[yi][j] && rem <= monthCumBefore[yi][j] + months[j]) { mi = j; break; }
    }
    return { year: yi + BS_EPOCH_YEAR, month: mi, date: rem - monthCumBefore[yi][mi] };
  }
  function daysPassedToAD(daysPassed) {
    var d = new Date(AD_EPOCH_MS + daysPassed * 86400000);
    return { year: d.getUTCFullYear(), month: d.getUTCMonth(), date: d.getUTCDate(), day: d.getUTCDay() };
  }
  function adToDaysPassed(year, month, date) {
    return Math.round((Date.UTC(year, month, date) - AD_EPOCH_MS) / 86400000);
  }
  function bsToAD(y, m, d) { return daysPassedToAD(bsToDaysPassed(y, m, d)); }
  function adToBS(y, m, d) { return daysPassedToBS(adToDaysPassed(y, m, d)); }
  function bsDaysInMonth(y, m) { return BS_DAYS[y - BS_EPOCH_YEAR][m]; }
  function bsWeekday(y, m, d) { return daysPassedToAD(bsToDaysPassed(y, m, d)).day; }
  function adWeekday(y, m, d) { return new Date(Date.UTC(y, m, d)).getUTCDay(); }

  var MONTH_EN = ['Baisakh', 'Jestha', 'Asar', 'Shrawan', 'Bhadra', 'Aswin', 'Kartik', 'Mangsir', 'Poush', 'Magh', 'Falgun', 'Chaitra'];
  var MONTH_NP = ['बैशाख', 'जेठ', 'असार', 'श्रावण', 'भाद्र', 'आश्विन', 'कार्तिक', 'मंसिर', 'पौष', 'माघ', 'फाल्गुण', 'चैत्र'];
  var GMONTH_EN = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  var GMONTH_NP = ['जनवरी', 'फेब्रुअरी', 'मार्च', 'अप्रिल', 'मे', 'जुन', 'जुलाई', 'अगस्ट', 'सेप्टेम्बर', 'अक्टोबर', 'नोभेम्बर', 'डिसेम्बर'];
  var WD_EN = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  var WD_NP = ['आइत', 'सोम', 'मंगल', 'बुध', 'बिहि', 'शुक्र', 'शनि'];
  var DIGIT_NP = ['०', '१', '२', '३', '४', '५', '६', '७', '८', '९'];

  function lang() { return document.documentElement.getAttribute('data-lang') === 'np' ? 'np' : 'en'; }
  function numStr(n) {
    var s = String(n);
    if (lang() !== 'np') return s;
    var out = '';
    for (var i = 0; i < s.length; i++) { out += DIGIT_NP[+s[i]] !== undefined ? DIGIT_NP[+s[i]] : s[i]; }
    return out;
  }

  // ---- DOM refs ----
  var tabs = document.querySelectorAll('.converter-tab');
  var panelAD = document.getElementById('panel-ad-to-bs');
  var panelBS = document.getElementById('panel-bs-to-ad');
  var adInput = document.getElementById('ad-date-input');
  var bsYearSel = document.getElementById('bs-year-select');
  var bsMonthSel = document.getElementById('bs-month-select');
  var bsDaySel = document.getElementById('bs-day-select');
  var resultBS = document.getElementById('result-bs-value');
  var resultAD = document.getElementById('result-ad-value');
  var todayBtn = document.getElementById('converter-today-btn');
  var calAdTitle = document.getElementById('cal-ad-title');
  var calAdWeekdays = document.getElementById('cal-ad-weekdays');
  var calAdGrid = document.getElementById('cal-ad-grid');
  var calBsTitle = document.getElementById('cal-bs-title');
  var calBsWeekdays = document.getElementById('cal-bs-weekdays');
  var calBsGrid = document.getElementById('cal-bs-grid');

  if (!adInput) return;

  // ---- state ----
  var now = new Date();
  var todayAD = { year: now.getFullYear(), month: now.getMonth(), date: now.getDate() };
  if (todayAD.year < 1943 || todayAD.year > 2034) { todayAD = { year: 2026, month: 7, date: 31 }; }
  var todayBS = adToBS(todayAD.year, todayAD.month, todayAD.date);

  var selected = { ad: todayAD, bs: todayBS };
  var viewAD = { year: todayAD.year, month: todayAD.month };
  var viewBS = { year: todayBS.year, month: todayBS.month };
  var mode = 'ad-to-bs';

  function pad2(n) { return n < 10 ? '0' + n : '' + n; }

  function setSelectedFromAD(y, m, d) {
    selected.ad = { year: y, month: m, date: d };
    selected.bs = adToBS(y, m, d);
    viewAD = { year: y, month: m };
    viewBS = { year: selected.bs.year, month: selected.bs.month };
    syncAll();
  }
  function setSelectedFromBS(y, m, d) {
    var maxD = bsDaysInMonth(y, m);
    if (d > maxD) d = maxD;
    selected.bs = { year: y, month: m, date: d };
    var ad = bsToAD(y, m, d);
    selected.ad = { year: ad.year, month: ad.month, date: ad.date };
    viewAD = { year: ad.year, month: ad.month };
    viewBS = { year: y, month: m };
    syncAll();
  }

  function populateBsMonthSelect() {
    var cur = bsMonthSel.value;
    var names = lang() === 'np' ? MONTH_NP : MONTH_EN;
    bsMonthSel.innerHTML = names.map(function (n, i) { return '<option value="' + i + '">' + n + '</option>'; }).join('');
    bsMonthSel.value = cur !== '' ? cur : String(selected.bs.month);
  }
  function populateBsYearSelect() {
    var opts = [];
    for (var y = BS_MIN_YEAR; y <= BS_MAX_YEAR; y++) { opts.push('<option value="' + y + '">' + y + '</option>'); }
    bsYearSel.innerHTML = opts.join('');
  }
  function populateBsDaySelect(year, month, keepDay) {
    var max = bsDaysInMonth(year, month);
    var opts = [];
    for (var d = 1; d <= max; d++) { opts.push('<option value="' + d + '">' + d + '</option>'); }
    bsDaySel.innerHTML = opts.join('');
    bsDaySel.value = String(Math.min(keepDay || 1, max));
  }

  function updateInputsFromSelected() {
    adInput.value = selected.ad.year + '-' + pad2(selected.ad.month + 1) + '-' + pad2(selected.ad.date);
    bsYearSel.value = String(selected.bs.year);
    populateBsMonthSelect();
    bsMonthSel.value = String(selected.bs.month);
    populateBsDaySelect(selected.bs.year, selected.bs.month, selected.bs.date);
  }

  function renderResult() {
    var bs = selected.bs, ad = selected.ad;
    var bsMonths = lang() === 'np' ? MONTH_NP : MONTH_EN;
    var gMonths = lang() === 'np' ? GMONTH_NP : GMONTH_EN;
    resultBS.textContent = bsMonths[bs.month] + ' ' + numStr(bs.date) + ', ' + numStr(bs.year) + ' BS';
    resultAD.textContent = gMonths[ad.month] + ' ' + numStr(ad.date) + ', ' + numStr(ad.year) + ' AD';
  }

  function renderCalendarAD() {
    var y = viewAD.year, m = viewAD.month;
    var gMonths = lang() === 'np' ? GMONTH_NP : GMONTH_EN;
    calAdTitle.textContent = gMonths[m] + ' ' + numStr(y);
    var wdNames = lang() === 'np' ? WD_NP : WD_EN;
    calAdWeekdays.innerHTML = wdNames.map(function (w) { return '<span>' + w + '</span>'; }).join('');
    var startWd = adWeekday(y, m, 1);
    var daysInMonth = new Date(Date.UTC(y, m + 1, 0)).getUTCDate();
    var cells = [];
    for (var i = 0; i < startWd; i++) { cells.push('<span class="cal-day empty"></span>'); }
    for (var d = 1; d <= daysInMonth; d++) {
      var isToday = (y === todayAD.year && m === todayAD.month && d === todayAD.date);
      var isSelected = (y === selected.ad.year && m === selected.ad.month && d === selected.ad.date);
      var cls = 'cal-day' + (isToday ? ' today' : '') + (isSelected ? ' selected' : '');
      cells.push('<span class="' + cls + '" data-day="' + d + '">' + numStr(d) + '</span>');
    }
    calAdGrid.innerHTML = cells.join('');
    Array.prototype.forEach.call(calAdGrid.querySelectorAll('.cal-day:not(.empty)'), function (el) {
      el.addEventListener('click', function () { setSelectedFromAD(viewAD.year, viewAD.month, parseInt(el.getAttribute('data-day'), 10)); });
    });
  }

  function renderCalendarBS() {
    var y = viewBS.year, m = viewBS.month;
    var bsMonths = lang() === 'np' ? MONTH_NP : MONTH_EN;
    calBsTitle.textContent = bsMonths[m] + ' ' + numStr(y);
    var wdNames = lang() === 'np' ? WD_NP : WD_EN;
    calBsWeekdays.innerHTML = wdNames.map(function (w) { return '<span>' + w + '</span>'; }).join('');
    var startWd = bsWeekday(y, m, 1);
    var daysInMonth = bsDaysInMonth(y, m);
    var cells = [];
    for (var i = 0; i < startWd; i++) { cells.push('<span class="cal-day empty"></span>'); }
    for (var d = 1; d <= daysInMonth; d++) {
      var isToday = (y === todayBS.year && m === todayBS.month && d === todayBS.date);
      var isSelected = (y === selected.bs.year && m === selected.bs.month && d === selected.bs.date);
      var cls = 'cal-day' + (isToday ? ' today' : '') + (isSelected ? ' selected' : '');
      cells.push('<span class="' + cls + '" data-day="' + d + '">' + numStr(d) + '</span>');
    }
    calBsGrid.innerHTML = cells.join('');
    Array.prototype.forEach.call(calBsGrid.querySelectorAll('.cal-day:not(.empty)'), function (el) {
      el.addEventListener('click', function () { setSelectedFromBS(viewBS.year, viewBS.month, parseInt(el.getAttribute('data-day'), 10)); });
    });
  }

  function syncAll() {
    renderResult();
    renderCalendarAD();
    renderCalendarBS();
    updateInputsFromSelected();
  }

  // ---- tabs ----
  Array.prototype.forEach.call(tabs, function (tab) {
    tab.addEventListener('click', function () {
      Array.prototype.forEach.call(tabs, function (t) { t.classList.remove('active'); });
      tab.classList.add('active');
      mode = tab.getAttribute('data-mode');
      panelAD.hidden = mode !== 'ad-to-bs';
      panelBS.hidden = mode !== 'bs-to-ad';
    });
  });

  // ---- AD input ----
  adInput.addEventListener('change', function () {
    var parts = adInput.value.split('-');
    if (parts.length !== 3) return;
    var y = parseInt(parts[0], 10), m = parseInt(parts[1], 10) - 1, d = parseInt(parts[2], 10);
    if (y < 1943 || y > 2034) return;
    setSelectedFromAD(y, m, d);
  });

  // ---- BS selects ----
  function readBsSelectsAndApply() {
    var y = parseInt(bsYearSel.value, 10);
    var m = parseInt(bsMonthSel.value, 10);
    var d = parseInt(bsDaySel.value, 10);
    setSelectedFromBS(y, m, d);
  }
  bsYearSel.addEventListener('change', function () {
    populateBsDaySelect(parseInt(bsYearSel.value, 10), parseInt(bsMonthSel.value, 10), parseInt(bsDaySel.value, 10));
    readBsSelectsAndApply();
  });
  bsMonthSel.addEventListener('change', function () {
    populateBsDaySelect(parseInt(bsYearSel.value, 10), parseInt(bsMonthSel.value, 10), parseInt(bsDaySel.value, 10));
    readBsSelectsAndApply();
  });
  bsDaySel.addEventListener('change', readBsSelectsAndApply);

  // ---- today button ----
  todayBtn.addEventListener('click', function () { setSelectedFromAD(todayAD.year, todayAD.month, todayAD.date); });

  // ---- calendar month navigation (browse independently) ----
  Array.prototype.forEach.call(document.querySelectorAll('.cal-nav'), function (btn) {
    btn.addEventListener('click', function () {
      var cal = btn.getAttribute('data-cal');
      var dir = parseInt(btn.getAttribute('data-dir'), 10);
      if (cal === 'ad') {
        var m = viewAD.month + dir, y = viewAD.year;
        if (m < 0) { m = 11; y--; }
        if (m > 11) { m = 0; y++; }
        if (y < 1943 || y > 2034) return;
        viewAD = { year: y, month: m };
        renderCalendarAD();
      } else {
        var bm = viewBS.month + dir, by = viewBS.year;
        if (bm < 0) { bm = 11; by--; }
        if (bm > 11) { bm = 0; by++; }
        if (by < BS_MIN_YEAR || by > BS_MAX_YEAR) return;
        viewBS = { year: by, month: bm };
        renderCalendarBS();
      }
    });
  });

  // ---- re-render on language toggle ----
  var langBtn = document.getElementById('lang-toggle');
  if (langBtn) { langBtn.addEventListener('click', function () { setTimeout(syncAll, 0); }); }

  // ---- init ----
  populateBsYearSelect();
  bsYearSel.value = String(selected.bs.year);
  syncAll();
})();
</script>
