/* LLM Bench 2026-11: charts, tables and tooltips.
   Reads window.__DATA (datasets) and window.__L (UI strings), both inlined by tools/build.py.
   All numbers are also present as static HTML, so the page stays readable without JavaScript. */
(function () {
  'use strict';
  var L = window.__L;
  var DATA = window.__DATA;
  if (!L || !DATA || !window.d3) return;

  // ---------- tiny runtime ----------
  var store = JSON.parse(JSON.stringify(DATA));
  var draws = {};
  var lastW = new WeakMap();
  var dash = {
    colors: ['#d97757', '#10a37f', '#4285f4', '#ec4899', '#8b5cf6', '#eab308', '#14b8a6', '#94a3b8'],
    data: function (id) {
      return id in store ? { status: 'ok', data: store[id] } : { status: 'missing', data: [] };
    },
    calc: function (id, o) { store[id] = o.fn.apply(null, o.inputs.map(function (i) { return store[i]; })); },
    draw: function (name, fn) { draws[name] = fn; },
    setLink: function (name) { try { history.replaceState(null, '', '#' + name); } catch (e) {} },
    start: function () {
      Object.keys(draws).forEach(function (name) {
        document.querySelectorAll('[data-draw="' + name + '"]').forEach(function (el) { run(name, el); });
      });
      if (!window.ResizeObserver) return;
      var ro = new ResizeObserver(function (entries) {
        entries.forEach(function (e) {
          var el = e.target, w = Math.round(el.clientWidth);
          if (lastW.get(el) === w) return;
          lastW.set(el, w);
          run(el.dataset.draw, el);
        });
      });
      document.querySelectorAll('.chart[data-draw]').forEach(function (el) {
        lastW.set(el, Math.round(el.clientWidth));
        ro.observe(el);
      });
    },
  };
  function run(name, el) {
    try { draws[name](el); } catch (e) { if (window.console) console.error('draw ' + name, e); }
  }

  // ---------- computed datasets ----------
  dash.calc('wins', {
    inputs: ['bench'],
    fn: function (bench) {
      var models = [
        ['opus', 'Claude Opus 5.5', 'Anthropic'],
        ['argon', 'Gemini 4 Argon', 'Google'],
        ['astra', 'GPT-6 Astra', 'OpenAI'],
        ['fable', 'Claude Fable 5.1', 'Anthropic'],
      ];
      var comp = bench.filter(function (r) { return models.filter(function (m) { return r[m[0]] != null; }).length >= 2; });
      return models.map(function (m) {
        var k = m[0];
        return {
          id: k, model: m[1], vendor: m[2], total: comp.length,
          wins: comp.filter(function (r) {
            return r[k] != null && models.every(function (j) { return r[j[0]] == null || r[k] >= r[j[0]]; });
          }).length,
        };
      });
    },
  });
  dash.calc('fvo_delta', {
    inputs: ['fable_vs_opus'],
    fn: function (rows) {
      return rows.map(function (r) {
        return { id: r.id, benchmark: r.benchmark, unit: r.unit, opus: r.opus, fable: r.fable, gap: Math.round((r.opus - r.fable) * 10) / 10 };
      });
    },
  });
  dash.calc('fvo_summary', {
    inputs: ['fable_vs_opus'],
    fn: function (rows) {
      return [{ ahead: rows.filter(function (r) { return r.opus > r.fable; }).length, total: rows.length }];
    },
  });
  dash.calc('tb4_delta', {
    inputs: ['tb4_gap'],
    fn: function (rows) {
      return rows.map(function (r) {
        return { id: r.id, model: r.model, vendor: r.vendor, claimed: r.claimed, independent: r.independent, gap: Math.round((r.claimed - r.independent) * 10) / 10 };
      });
    },
  });

  // ---------- helpers ----------
  var VENDORS = ['Anthropic', 'OpenAI', 'Google', 'xAI', 'Moonshot', 'Z.ai'];
  function vcol(v) { return dash.colors[Math.max(0, VENDORS.indexOf(v))]; }
  function rowsOf(id) { var g = dash.data(id); return g.status === 'ok' ? g.data : null; }
  var fmt = {
    int: function (v) { return String(Math.round(v)); },
    pct1: function (v) { return v.toFixed(1) + '%'; },
    usd: function (v) { return '$' + (Number.isInteger(v) ? v : v.toFixed(2)); },
    usd2: function (v) { return '$' + v.toFixed(2); },
    elo: function (v) { return String(Math.round(v)); },
    gap: function (g) { return (g > 0 ? '+' : g < 0 ? '−' : '') + Math.abs(g).toFixed(1); },
    text: function (v) { return String(v); },
  };

  function ready(el, ids) {
    var bad = ids.some(function (i) { return dash.data(i).status !== 'ok'; });
    if (!bad) return true;
    el.replaceChildren();
    var d = document.createElement('div');
    d.className = 'fail';
    var dot = document.createElement('span');
    dot.className = 'dot';
    d.append(dot, document.createTextNode(L.notLoaded));
    el.append(d);
    return false;
  }

  function mkTip(box) {
    var t = document.createElement('div');
    t.className = 'tip';
    t.hidden = true;
    box.append(t);
    return {
      show: function (ev, tip) {
        t.replaceChildren();
        var h = document.createElement('div');
        h.className = 'tt';
        h.textContent = tip.title;
        t.append(h);
        tip.lines.forEach(function (ln) {
          var l = document.createElement('div');
          l.className = 'tr';
          if (ln[2]) { var s = document.createElement('i'); s.style.background = ln[2]; l.append(s); }
          var n = document.createElement('span'); n.textContent = ln[0];
          var v = document.createElement('span'); v.className = 'v'; v.textContent = ln[1];
          l.append(n, v);
          t.append(l);
        });
        t.hidden = false;
        var r = box.getBoundingClientRect();
        var x = Math.max(0, Math.min(ev.clientX - r.left + 14, r.width - t.offsetWidth));
        var y = Math.max(0, Math.min(ev.clientY - r.top + 14, r.height - t.offsetHeight));
        t.style.left = x + 'px';
        t.style.top = y + 'px';
      },
      hide: function () { t.hidden = true; },
    };
  }

  function legend(el, items) {
    var d = document.createElement('div');
    d.className = 'legend';
    items.forEach(function (it) {
      var s = document.createElement('span');
      s.className = 'lg';
      var i = document.createElement('i');
      i.style.background = it.hollow ? 'transparent' : it.color;
      i.style.borderColor = it.color;
      s.append(i, document.createTextNode(it.name));
      d.append(s);
    });
    el.append(d);
  }

  function mkSvg(el, W, H) {
    return d3.select(el).append('svg').attr('viewBox', '0 0 ' + W + ' ' + H).attr('width', '100%').attr('role', 'img').style('display', 'block');
  }
  function measure(svg, strs, cls) {
    var t = svg.append('text').attr('class', cls), w = 0;
    strs.forEach(function (s) { t.text(s); w = Math.max(w, t.node().getComputedTextLength()); });
    t.remove();
    return Math.ceil(w);
  }
  function widthOf(el) { return Math.max(260, el.clientWidth || 520); }
  function uniqueVendors(rows) { return Array.from(new Set(rows.map(function (r) { return r.vendor; }))); }

  // ---------- horizontal bars ----------
  function hbar(el, rows, o) {
    el.replaceChildren();
    var W = widthOf(el), bh = 20, gap = 12, t = 6, b = 6;
    var svg = mkSvg(el, W, 100);
    var lw = measure(svg, rows.map(function (r) { return r.label; }), 'tick lbl');
    var vw = measure(svg, rows.map(function (r) { return o.fmt(r.value); }), 'tick val');
    var l = lw + 14, r = vw + 12;
    var H = t + b + rows.length * (bh + gap) - gap;
    svg.attr('viewBox', '0 0 ' + W + ' ' + H);
    var x = d3.scaleLinear().domain([0, o.max]).range([l, W - r]);
    var tip = mkTip(el);
    svg.append('line').attr('class', 'base').attr('x1', l).attr('x2', l).attr('y1', 0).attr('y2', H);
    rows.forEach(function (d, i) {
      var y = t + i * (bh + gap);
      svg.append('text').attr('class', 'tick lbl').attr('x', l - 8).attr('y', y + bh / 2).attr('dy', '0.35em').attr('text-anchor', 'end').text(d.label);
      svg.append('rect').attr('x', l).attr('y', y).attr('width', Math.max(2, x(d.value) - l)).attr('height', bh).attr('rx', 4).style('fill', d.color).style('opacity', d.dim ? 0.4 : 1);
      svg.append('text').attr('class', 'tick val').attr('x', x(d.value) + 6).attr('y', y + bh / 2).attr('dy', '0.35em').text(o.fmt(d.value));
      svg.append('rect').attr('x', 0).attr('y', y - gap / 2).attr('width', W).attr('height', bh + gap).attr('fill', 'transparent')
        .on('mousemove', function (ev) { tip.show(ev, d.tip); }).on('mouseleave', tip.hide);
    });
  }

  dash.draw('indexChart', function (el) {
    if (!ready(el, ['models'])) return;
    var rows = rowsOf('models').filter(function (r) { return r.aa_index != null; }).sort(function (a, b) { return b.aa_index - a.aa_index; });
    hbar(el, rows.map(function (r) {
      return {
        label: r.model + (r.restricted ? L.closedSuffix : ''), value: r.aa_index, color: vcol(r.vendor), dim: r.restricted,
        tip: { title: r.model, lines: [[L.indexAA, fmt.int(r.aa_index), vcol(r.vendor)], [L.vendor, r.vendor]] },
      };
    }), { max: 65, fmt: fmt.int });
    legend(el, uniqueVendors(rows).map(function (v) { return { name: v, color: vcol(v) }; }));
  });

  dash.draw('winsChart', function (el) {
    if (!ready(el, ['wins'])) return;
    var rows = rowsOf('wins').slice().sort(function (a, b) { return b.wins - a.wins; });
    var total = rows.length ? rows[0].total : 1;
    hbar(el, rows.map(function (r) {
      return {
        label: r.model, value: r.wins, color: vcol(r.vendor),
        tip: { title: r.model, lines: [[L.leads, fmt.int(r.wins) + L.of + fmt.int(r.total), vcol(r.vendor)]] },
      };
    }), { max: total, fmt: fmt.int });
    legend(el, ['Anthropic', 'OpenAI', 'Google'].map(function (v) { return { name: v, color: vcol(v) }; }));
  });

  // ---------- price vs quality ----------
  dash.draw('valueChart', function (el) {
    if (!ready(el, ['models'])) return;
    var pts = rowsOf('models').filter(function (r) { return r.aa_index != null && r.task_cost != null; });
    el.replaceChildren();
    var W = widthOf(el), H = Math.round(Math.max(260, Math.min(380, W * 0.8)));
    var m = { t: 20, r: 14, b: 46, l: 40 };
    var svg = mkSvg(el, W, H);
    var x = d3.scaleLog().domain([1, 16]).range([m.l, W - m.r]);
    var y = d3.scaleLinear().domain([40, 62]).range([H - m.b, m.t]);
    [40, 45, 50, 55, 60].forEach(function (v) {
      svg.append('line').attr('class', 'grid').attr('x1', m.l).attr('x2', W - m.r).attr('y1', y(v)).attr('y2', y(v));
      svg.append('text').attr('class', 'tick').attr('x', m.l - 8).attr('y', y(v)).attr('dy', '0.35em').attr('text-anchor', 'end').text(v);
    });
    [1, 2, 5, 10].forEach(function (v) {
      svg.append('line').attr('class', 'grid').attr('x1', x(v)).attr('x2', x(v)).attr('y1', m.t).attr('y2', H - m.b);
      svg.append('text').attr('class', 'tick').attr('x', x(v)).attr('y', H - m.b + 16).attr('text-anchor', 'middle').text('$' + v);
    });
    svg.append('text').attr('class', 'tick').attr('x', (m.l + W - m.r) / 2).attr('y', H - 6).attr('text-anchor', 'middle').text(L.valueX);
    svg.append('text').attr('class', 'tick').attr('x', m.l).attr('y', 10).text(L.valueY);
    svg.append('text').attr('class', 'tick').attr('x', m.l + 10).attr('y', m.t + 16).text(L.better);
    var span = W - m.l - m.r;
    var items = pts.map(function (r) { return { r: r, px: x(r.task_cost), py: y(r.aa_index), left: x(r.task_cost) > m.l + span * 0.6 }; });
    [true, false].forEach(function (side) {
      var arr = items.filter(function (d) { return d.left === side; });
      arr.forEach(function (d) { d.ly = d.py + (side ? -9 : 0); });
      arr.sort(function (a, b) { return a.ly - b.ly; });
      for (var i = 1; i < arr.length; i++) if (arr[i].ly - arr[i - 1].ly < 14) arr[i].ly = arr[i - 1].ly + 14;
    });
    var tip = mkTip(el);
    items.forEach(function (d) {
      svg.append('circle').attr('cx', d.px).attr('cy', d.py).attr('r', 7).style('fill', vcol(d.r.vendor)).style('stroke', 'var(--color-panel)').style('stroke-width', 2);
      svg.append('text').attr('class', 'tick lbl').attr('x', d.px + (d.left ? -12 : 12)).attr('y', d.ly).attr('dy', '0.35em').attr('text-anchor', d.left ? 'end' : 'start').text(d.r.model.replace('Claude ', ''));
      svg.append('circle').attr('cx', d.px).attr('cy', d.py).attr('r', 16).attr('fill', 'transparent')
        .on('mousemove', function (ev) {
          tip.show(ev, { title: d.r.model, lines: [[L.indexAA, fmt.int(d.r.aa_index), vcol(d.r.vendor)], [L.taskCost, fmt.usd2(d.r.task_cost)]] });
        }).on('mouseleave', tip.hide);
    });
    legend(el, uniqueVendors(pts).map(function (v) { return { name: v, color: vcol(v) }; }));
  });

  // ---------- speed ----------
  dash.draw('speedChart', function (el) {
    if (!ready(el, ['models'])) return;
    var rows = rowsOf('models').filter(function (r) { return r.speed_lo != null; }).sort(function (a, b) { return b.speed_hi - a.speed_hi; });
    el.replaceChildren();
    var W = widthOf(el), rh = 32, t = 6, b = 26;
    var label = function (r) { return r.speed_lo === r.speed_hi ? String(r.speed_lo) : r.speed_lo + '–' + r.speed_hi; };
    var svg = mkSvg(el, W, 100);
    var lw = measure(svg, rows.map(function (r) { return r.model; }), 'tick lbl');
    var vw = measure(svg, rows.map(label), 'tick val');
    var l = lw + 14, rr = vw + 16;
    var H = t + rows.length * rh + b;
    svg.attr('viewBox', '0 0 ' + W + ' ' + H);
    var x = d3.scaleLinear().domain([0, 120]).range([l + 6, W - rr]);
    [0, 40, 80, 120].forEach(function (v) {
      svg.append('line').attr('class', 'grid').attr('x1', x(v)).attr('x2', x(v)).attr('y1', t).attr('y2', H - b);
      svg.append('text').attr('class', 'tick').attr('x', x(v)).attr('y', H - b + 16).attr('text-anchor', 'middle').text(v);
    });
    var tip = mkTip(el);
    rows.forEach(function (d, i) {
      var cy = t + i * rh + rh / 2;
      svg.append('text').attr('class', 'tick lbl').attr('x', l - 8).attr('y', cy).attr('dy', '0.35em').attr('text-anchor', 'end').text(d.model);
      svg.append('line').attr('class', 'span').attr('x1', x(d.speed_lo)).attr('x2', x(d.speed_hi)).attr('y1', cy).attr('y2', cy).style('stroke', vcol(d.vendor));
      svg.append('text').attr('class', 'tick val').attr('x', x(d.speed_hi) + 12).attr('y', cy).attr('dy', '0.35em').text(label(d));
      svg.append('rect').attr('x', 0).attr('y', cy - rh / 2).attr('width', W).attr('height', rh).attr('fill', 'transparent')
        .on('mousemove', function (ev) { tip.show(ev, { title: d.model, lines: [[L.speedTps, label(d), vcol(d.vendor)]] }); })
        .on('mouseleave', tip.hide);
    });
    legend(el, uniqueVendors(rows).map(function (v) { return { name: v, color: vcol(v) }; }));
  });

  // ---------- dumbbells ----------
  function dot(svg, cx, cy, s) {
    svg.append('circle').attr('cx', cx).attr('cy', cy).attr('r', 6)
      .style('fill', s.hollow ? 'var(--color-panel)' : s.fill)
      .style('stroke', s.hollow ? s.stroke : 'var(--color-panel)')
      .style('stroke-width', 2);
  }
  function dumbbell(el, rows, o) {
    el.replaceChildren();
    var W = widthOf(el), rh = 30, t = 8, b = 28;
    var svg = mkSvg(el, W, 100);
    var lw = measure(svg, rows.map(function (r) { return r.label; }), 'tick lbl');
    var gw = measure(svg, rows.map(function (r) { return fmt.gap(r.gap); }), 'tick gl');
    var l = lw + 14, rr = gw + 18;
    var H = t + rows.length * rh + b;
    svg.attr('viewBox', '0 0 ' + W + ' ' + H);
    var x = d3.scaleLinear().domain(o.domain).range([l + 8, W - rr]);
    o.ticks.forEach(function (v) {
      svg.append('line').attr('class', 'grid').attr('x1', x(v)).attr('x2', x(v)).attr('y1', t).attr('y2', H - b);
      svg.append('text').attr('class', 'tick').attr('x', x(v)).attr('y', H - b + 16).attr('text-anchor', 'middle').text(v + '%');
    });
    var tip = mkTip(el);
    rows.forEach(function (d, i) {
      var cy = t + i * rh + rh / 2;
      svg.append('text').attr('class', 'tick lbl').attr('x', l - 8).attr('y', cy).attr('dy', '0.35em').attr('text-anchor', 'end').text(d.label);
      svg.append('line').attr('class', 'stem').attr('x1', x(d.a)).attr('x2', x(d.b)).attr('y1', cy).attr('y2', cy);
      dot(svg, x(d.b), cy, o.b);
      dot(svg, x(d.a), cy, o.a);
      svg.append('text').attr('class', 'tick gl' + (d.crit ? ' crit' : '')).attr('x', W - rr + 8).attr('y', cy).attr('dy', '0.35em').text(fmt.gap(d.gap));
      svg.append('rect').attr('x', 0).attr('y', cy - rh / 2).attr('width', W).attr('height', rh).attr('fill', 'transparent')
        .on('mousemove', function (ev) { tip.show(ev, d.tip); }).on('mouseleave', tip.hide);
    });
  }

  dash.draw('fvoChart', function (el) {
    if (!ready(el, ['fvo_delta'])) return;
    var rows = rowsOf('fvo_delta').filter(function (r) { return r.unit === '%'; }).sort(function (a, b) { return b.gap - a.gap; });
    var A = vcol('Anthropic'), B = 'var(--cds-chart-muted)';
    dumbbell(el, rows.map(function (r) {
      return {
        label: r.benchmark, a: r.opus, b: r.fable, gap: r.gap,
        tip: { title: r.benchmark, lines: [['Opus 5.5', fmt.pct1(r.opus), A], ['Fable 5.1', fmt.pct1(r.fable), B], [L.gapPp, fmt.gap(r.gap)]] },
      };
    }), { domain: [25, 95], ticks: [30, 50, 70, 90], a: { fill: A }, b: { fill: B } });
    legend(el, [{ name: 'Opus 5.5', color: A }, { name: 'Fable 5.1', color: B }]);
  });

  dash.draw('tb4Chart', function (el) {
    if (!ready(el, ['tb4_delta'])) return;
    var rows = rowsOf('tb4_delta').slice().sort(function (a, b) { return Math.abs(b.gap) - Math.abs(a.gap); });
    dumbbell(el, rows.map(function (r, i) {
      return {
        label: r.model, a: r.claimed, b: r.independent, gap: r.gap, crit: i === 0,
        tip: { title: r.model, lines: [[L.claimed, fmt.pct1(r.claimed)], [L.aaMeasure, fmt.pct1(r.independent)], [L.gapPp, fmt.gap(r.gap)]] },
      };
    }), { domain: [20, 72], ticks: [25, 40, 55, 70], a: { hollow: true, stroke: 'var(--color-fg-muted)' }, b: { fill: 'var(--color-fg)' } });
    legend(el, [{ name: L.claimed, color: 'var(--color-fg-muted)', hollow: true }, { name: L.aaMeasure, color: 'var(--color-fg)' }]);
  });

  // ---------- numbers inside text ----------
  dash.draw('val', function (el) {
    var g = dash.data(el.dataset.source);
    if (g.status !== 'ok') return;
    var row;
    if (el.dataset.row != null) row = g.data[+el.dataset.row];
    else {
      var where = Object.fromEntries(new URLSearchParams(el.dataset.where || ''));
      row = g.data.find(function (r) { return Object.keys(where).every(function (k) { return String(r[k]) === where[k]; }); });
    }
    var v = row ? row[el.dataset.field] : null;
    el.textContent = v == null ? '—' : (fmt[el.dataset.fmt] || String)(+v);
  });

  // ---------- tables ----------
  var MODEL_KEYS = ['opus', 'fable', 'astra', 'argon'];
  function renderTable(tbody, rows) {
    var table = tbody.closest('table');
    var ths = Array.from(table.querySelectorAll('thead th[data-field]'));
    tbody.replaceChildren.apply(tbody, rows.map(function (r) {
      var tr = document.createElement('tr');
      tr.dataset.key = r[table.dataset.rowKey];
      if (r.restricted) tr.classList.add('dim');
      var vals = MODEL_KEYS.map(function (k) { return r[k]; }).filter(function (v) { return v != null; });
      var best = vals.length >= 2 ? Math.max.apply(null, vals) : null;
      ths.forEach(function (th) {
        var td = document.createElement('td');
        td.className = th.className;
        var f = th.dataset.field, k = th.dataset.fmt || 'text', v = r[f], s;
        if (k === 'range') s = v == null ? '—' : (v === r[th.dataset.hi] ? String(v) : v + '–' + r[th.dataset.hi]);
        else if (k === 'val') {
          s = v == null ? '—' : (r.unit === 'Elo' ? fmt.elo(v) : fmt.pct1(v));
          if (best != null && v === best) td.classList.add('best');
        } else if (k === 'idx') {
          s = v == null ? '—' : fmt.int(v);
          if (v != null) { td.classList.add('bar'); td.style.setProperty('--w', (v / 65 * 100).toFixed(2) + '%'); }
        } else if (k === 'status') {
          s = String(v);
          td.classList.add('st-' + r.status_key);
        } else s = v == null ? '—' : (fmt[k] || String)(v);
        if (f === 'note' || f === 'detail') td.classList.add('sm');
        td.textContent = s;
        tr.append(td);
      });
      return tr;
    }));
  }
  dash.draw('modelsBody', function (tb) {
    var rows = rowsOf('models');
    if (!rows) return;
    renderTable(tb, rows.slice().sort(function (a, b) { return (b.aa_index == null ? -1 : b.aa_index) - (a.aa_index == null ? -1 : a.aa_index); }));
  });
  dash.draw('benchBody', function (tb) {
    var rows = rowsOf('bench');
    if (!rows) return;
    renderTable(tb, rows.filter(function (r) { return r.group === tb.dataset.group; }));
  });
  dash.draw('namingBody', function (tb) {
    var rows = rowsOf('naming');
    if (!rows) return;
    renderTable(tb, rows);
  });

  // ---------- navigation ----------
  function go(el) { el.scrollIntoView(); dash.setLink(el.id); }
  document.querySelectorAll('[data-go]').forEach(function (b) {
    b.addEventListener('click', function () { var t = document.getElementById(b.dataset.go); if (t) go(t); });
  });

  dash.start();
})();
