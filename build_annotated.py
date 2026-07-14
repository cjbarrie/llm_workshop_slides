#!/usr/bin/env python3
"""
Builds llm_workshop_slides_annotated.html from llm_workshop_slides.html.

Takes the self-contained Quarto reveal.js export and adds a persistent
right-hand narration column (reusing each slide's existing `::: {.notes}`
speaker notes) plus a click-to-jump outline, in the style of
https://www.cs.princeton.edu/~arvindn/talks/icml-2026-annotated-slides/.

Does not touch the source .qmd or the primary .html output — this is a
purely additive post-processing step. Re-run after re-rendering the main
deck to refresh this variant.
"""
import re

SRC = "llm_workshop_slides.html"
OUT = "llm_workshop_slides_annotated.html"

INJECTION = """
<style>
  html, body { height: 100%; margin: 0; overflow: hidden; }

  #annotated-layout {
    display: flex;
    height: 100vh;
    width: 100vw;
    overflow: hidden;
  }

  #slide-col {
    flex: 0 0 62%;
    max-width: 62%;
    height: 100vh;
    position: relative !important;
  }

  /* .slide-logo / .slide-number / the menu button are position:fixed by
     default, i.e. relative to the browser viewport. Once the deck only
     occupies the left 62%, that would place them inside the narration
     column. Rescope them to the slide column instead (.reveal already
     has position:relative as its base style, so absolute here anchors
     correctly to the slide edge, not the full window). */
  #slide-col .slide-logo,
  #slide-col .slide-number,
  #slide-col .reveal.has-logo .slide-number {
    position: absolute !important;
  }
  #slide-col .slide-menu-button { display: none !important; }

  #narr-col {
    flex: 1 1 38%;
    height: 100vh;
    overflow-y: auto;
    box-sizing: border-box;
    padding: 44px 44px 100px;
    background: #faf8f3;
    border-left: 1px solid #e3e0d8;
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 17px;
    line-height: 1.7;
    color: #2b2b2b;
  }

  #narr-col .narr-eyebrow {
    font-family: 'Source Sans Pro', 'Helvetica Neue', sans-serif;
    font-size: .78em;
    letter-spacing: .06em;
    text-transform: uppercase;
    color: #8a8a8a;
    margin: 0 0 .3em;
  }

  #narr-col h2 {
    font-family: 'Source Sans Pro', 'Helvetica Neue', sans-serif;
    font-weight: 600;
    font-size: 1.35em;
    color: #1c1c1e;
    margin: 0 0 .8em;
    padding-bottom: .4em;
    border-bottom: 2px solid #e3e0d8;
  }

  #narr-col p { margin: 0 0 1em; }
  #narr-col .no-notes { color: #999; font-style: italic; }

  #narr-col .narr-nav {
    display: flex;
    justify-content: space-between;
    margin: 1.6em 0 2em;
    font-family: 'Source Sans Pro', 'Helvetica Neue', sans-serif;
    font-size: .85em;
  }
  #narr-col .narr-nav button {
    background: none;
    border: 1px solid #ccc;
    border-radius: 6px;
    padding: .4em .9em;
    cursor: pointer;
    color: #46586b;
    font: inherit;
  }
  #narr-col .narr-nav button:hover { background: #eee; }
  #narr-col .narr-nav button:disabled { opacity: .35; cursor: default; }

  #narr-col details.narr-toc {
    margin-top: 2.2em;
    padding-top: 1.2em;
    border-top: 1px solid #e3e0d8;
    font-family: 'Source Sans Pro', 'Helvetica Neue', sans-serif;
    font-size: .85em;
  }
  #narr-col details.narr-toc summary {
    cursor: pointer;
    color: #8a8a8a;
    text-transform: uppercase;
    letter-spacing: .05em;
    font-size: .85em;
    margin-bottom: .6em;
  }
  #narr-col .narr-toc ol { margin: 0; padding-left: 1.3em; }
  #narr-col .narr-toc li { margin-bottom: .35em; }
  #narr-col .narr-toc a { color: #46586b; text-decoration: none; cursor: pointer; }
  #narr-col .narr-toc a:hover { text-decoration: underline; }
  #narr-col .narr-toc li.current > a { font-weight: 700; color: #1c1c1e; }
</style>

<div id="narr-panel-source" style="display:none"></div>

<script>
(function () {
  function buildToc() {
    var sections = Array.prototype.slice.call(document.querySelectorAll('#slide-col .slides > section'));
    return sections.map(function (sec, i) {
      var h = sec.querySelector('h1, h2');
      var title = h ? h.textContent.trim() : ('Slide ' + (i + 1));
      return { index: i, title: title };
    });
  }

  function setup() {
    var revealEl = document.querySelector('.reveal');
    if (!revealEl || !window.Reveal) { setTimeout(setup, 100); return; }

    var wrapper = document.createElement('div');
    wrapper.id = 'annotated-layout';
    revealEl.parentNode.insertBefore(wrapper, revealEl);
    wrapper.appendChild(revealEl);
    revealEl.id = 'slide-col';

    var narrCol = document.createElement('div');
    narrCol.id = 'narr-col';
    narrCol.innerHTML =
      '<p class="narr-eyebrow">Speaker notes</p>' +
      '<div id="narr-content"></div>' +
      '<div class="narr-nav">' +
        '<button id="narr-prev">\\u2190 Previous</button>' +
        '<button id="narr-next">Next \\u2192</button>' +
      '</div>' +
      '<details class="narr-toc"><summary>In this talk</summary><ol id="narr-toc-list"></ol></details>';
    wrapper.appendChild(narrCol);

    var toc = buildToc();
    var tocList = document.getElementById('narr-toc-list');
    toc.forEach(function (item) {
      var li = document.createElement('li');
      li.dataset.index = item.index;
      var a = document.createElement('a');
      a.textContent = item.title;
      a.href = '#/' + item.index;
      a.addEventListener('click', function (e) {
        e.preventDefault();
        Reveal.slide(item.index);
      });
      li.appendChild(a);
      tocList.appendChild(li);
    });

    document.getElementById('narr-prev').addEventListener('click', function () { Reveal.prev(); });
    document.getElementById('narr-next').addEventListener('click', function () { Reveal.next(); });

    function updateNarration() {
      var slide = Reveal.getCurrentSlide();
      if (!slide) return;
      var notes = slide.querySelector('aside.notes');
      var title = slide.querySelector('h1, h2');
      var html = '';
      if (title) html += '<h2>' + title.innerHTML + '</h2>';
      html += notes ? notes.innerHTML : '<p class="no-notes">(No speaker notes for this slide.)</p>';
      document.getElementById('narr-content').innerHTML = html;
      narrCol.scrollTop = 0;

      var idx = Reveal.getIndices().h;
      document.getElementById('narr-prev').disabled = idx === 0;
      document.getElementById('narr-next').disabled = idx === toc.length - 1;
      Array.prototype.forEach.call(tocList.children, function (li) {
        li.classList.toggle('current', Number(li.dataset.index) === idx);
      });
      var currentLi = tocList.querySelector('li.current');
      if (currentLi) currentLi.scrollIntoView({ block: 'nearest' });
    }

    Reveal.on('ready', updateNarration);
    Reveal.on('slidechanged', updateNarration);
    if (Reveal.isReady && Reveal.isReady()) updateNarration();

    function relayout() { Reveal.layout(); }
    window.addEventListener('resize', relayout);
    relayout();
  }

  if (document.readyState === 'complete') setTimeout(setup, 50);
  else window.addEventListener('load', function () { setTimeout(setup, 50); });
})();
</script>
"""

with open(SRC, encoding="utf-8") as f:
    html = f.read()

if "id=\"annotated-layout\"" in html:
    raise SystemExit(f"{SRC} already looks annotated — check the source file")

# Insert only at the TRUE end of the document. A naive html.replace() here is
# unsafe: self-contained Quarto/reveal.js exports can bundle third-party JS
# (e.g. Mermaid's SVG-export code) that contains the literal string
# "</body></html>" inside its own JS string literals, earlier in the file.
# replace() would corrupt that library's syntax and break the whole page.
# rfind() anchors to the actual last occurrence instead.
marker = "</body></html>"
idx = html.rfind(marker)
if idx == -1:
    raise SystemExit(f"{SRC}: couldn't find the closing {marker!r} to inject before")
html = html[:idx] + INJECTION + html[idx:]

with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Wrote {OUT} ({len(html):,} bytes)")
