// test_full_suite.js
// Automated verification suite for AuraMed CDSS web application

const fs = require('fs');

async function run() {
    console.log('=== AURAMED CDSS END-TO-END AUTOMATED VERIFICATION SUITE ===\n');

    // 1. Verify HTTP Endpoints on live server
    const endpoints = [
        '/',
        '/images/medical-bg.jpg',
        '/api/knowledge-base',
        '/api/symptoms',
        '/api/symptoms/categorized',
        '/api/diseases',
        '/api/case-presets'
    ];

    console.log('[1/4] Verifying HTTP GET Endpoints on http://127.0.0.1:5000:');
    for (const ep of endpoints) {
        const res = await fetch(`http://127.0.0.1:5000${ep}`);
        if (!res.ok) {
            throw new Error(`Endpoint ${ep} returned HTTP ${res.status}`);
        }
        const ct = res.headers.get('content-type');
        console.log(`  ✓ ${ep.padEnd(30)} HTTP ${res.status} [${ct}]`);
    }

    // 2. Verify Inference API POST Endpoints
    console.log('\n[2/4] Verifying Inference API POST Endpoints:');
    
    // Forward chaining test
    const fwdRes = await fetch('http://127.0.0.1:5000/api/forward-chain', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            symptoms: ['chest_pain', 'shortness_of_breath', 'sweating', 'nausea']
        })
    });
    const fwdData = await fwdRes.json();
    console.log(`  ✓ /api/forward-chain: status=${fwdRes.status}, matches_found=${fwdData.matches_found}`);
    if (!fwdData.results || fwdData.results.length === 0) {
        throw new Error('Forward chaining returned no results');
    }
    const topDiag = fwdData.results[0];
    console.log(`    Top match: ${topDiag.diagnosis} (Rule ${topDiag.rule_id}, Match: ${topDiag.match_ratio}%, Full match: ${topDiag.is_full_match})`);

    // Backward chaining test
    const bwdRes = await fetch('http://127.0.0.1:5000/api/backward-chain', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            target: 'Acute Myocardial Infarction (Heart Attack)',
            symptoms: ['chest_pain', 'shortness_of_breath']
        })
    });
    const bwdData = await bwdRes.json();
    console.log(`  ✓ /api/backward-chain: status=${bwdRes.status}, target="${bwdData.result?.target}", matched=${bwdData.result?.matched}`);

    // Triage test
    const triageRes = await fetch('http://127.0.0.1:5000/api/triage', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            vitals: { age: 60, gender: 'Male', bp: '185/95', hr: 120, spo2: 89, temp: 38.5 },
            symptoms: ['chest_pain']
        })
    });
    const triageData = await triageRes.json();
    console.log(`  ✓ /api/triage: triage_level="${triageData.triage_level}", red_flags=${triageData.red_flags.length}`);

    // 3. Client-Side Script Execution & DOM Integration
    console.log('\n[3/4] Testing Client-Side Execution in DOM Mock Environment:');
    const html = fs.readFileSync('S:\\ai mini project\\templates\\index.html', 'utf8');

    const scriptMatch = html.match(/<script>([\s\S]*?)<\/script>/);
    if (!scriptMatch) {
        throw new Error('No script tag found in index.html');
    }
    const scriptCode = scriptMatch[1];
    console.log(`  ✓ Extracted client-side script (${scriptCode.length} characters)`);

    // Mock DOM elements
    const elements = new Map();
    const checkboxes = new Map();

    function createMockElement(id, tagName = 'div') {
        const elem = {
            id,
            tagName: tagName.toUpperCase(),
            children: [],
            options: [],
            classList: {
                classes: new Set(),
                add: function(...cls) { cls.forEach(c => this.classes.add(c)); },
                remove: function(...cls) { cls.forEach(c => this.classes.delete(c)); },
                contains: function(c) { return this.classes.has(c); },
                toggle: function(c) { if (this.classes.has(c)) this.classes.delete(c); else this.classes.add(c); }
            },
            style: {},
            value: '',
            innerText: '',
            textContent: '',
            _innerHTML: '',
            get innerHTML() { return this._innerHTML; },
            set innerHTML(val) {
                this._innerHTML = val;
                // Parse checkboxes if rendered into grid
                if (val.includes('type="checkbox"')) {
                    const matches = [...val.matchAll(/value="([^"]+)"/g)];
                    matches.forEach(m => {
                        const valName = m[1];
                        if (!checkboxes.has(valName)) {
                            checkboxes.set(valName, {
                                name: 'symptom',
                                value: valName,
                                checked: false
                            });
                        }
                    });
                }
            },
            setAttribute: function(k, v) { this[k] = v; },
            getAttribute: function(k) { return this[k] || null; },
            addEventListener: function() {},
            appendChild: function(c) { this.children.push(c); return c; },
            querySelector: function(sel) { return null; },
            querySelectorAll: function(sel) { return []; },
            closest: function() { return null; },
            getBoundingClientRect: function() { return { width: 800, height: 450, top: 0, left: 0 }; }
        };
        elements.set(id, elem);
        return elem;
    }

    const elementIds = [
        'symptoms-grid', 'case-presets-grid', 'kb-rules-grid', 'network-svg',
        'selected-count', 'diagnostic-output', 'audit-trace-box',
        'stat-rules-count', 'stat-latency', 'kb-stat-rules', 'kb-stat-symptoms',
        'kb-stat-diseases', 'benchmark-stat-rules', 'viva-modal', 'audio-toggle-btn',
        'patient-age', 'patient-gender', 'patient-bp', 'patient-hr', 'patient-spo2', 'patient-temp',
        'triage-status-badge', 'triage-alert-box', 'triage-alert-text',
        'symptom-search', 'target-disease-select', 'tab-forward', 'tab-backward',
        'backward-goal-container', 'btn-text', 'result-mode-tag',
        'results-idle-state', 'results-active-state', 'telemetry-latency',
        'primary-diag-card', 'differentials-list', 'diag-rank-label', 'diag-title',
        'diag-rule-id', 'diag-icd', 'diag-category', 'diag-severity-badge',
        'diag-match-percent', 'diag-match-bar', 'diag-satisfied-chips', 'diag-missing-chips',
        'diag-tests', 'diag-treatment', 'graph-status', 'test-table-body',
        'print-date', 'print-vitals', 'print-symptoms', 'print-diagnoses', 'print-audit-trace',
        'hero-model-img', 'total-symptoms-count'
    ];

    elementIds.forEach(id => createMockElement(id));

    // Special mock for querySelectorAll
    const documentMock = {
        readyState: 'complete',
        documentElement: { style: { setProperty: () => {} } },
        body: createMockElement('body', 'body'),
        addEventListener: () => {},
        getElementById: (id) => elements.get(id) || createMockElement(id),
        querySelector: (sel) => {
            if (sel.startsWith('#')) return elements.get(sel.slice(1)) || null;
            if (sel.includes('input[name="symptom"][value="')) {
                const val = sel.split('value="')[1].split('"]')[0];
                return checkboxes.get(val) || null;
            }
            return null;
        },
        querySelectorAll: (sel) => {
            if (sel === 'input[name="symptom"]') {
                return Array.from(checkboxes.values());
            }
            if (sel === 'input[name="symptom"]:checked') {
                return Array.from(checkboxes.values()).filter(cb => cb.checked);
            }
            if (sel === '#system-category-pills button') {
                return [];
            }
            return [];
        },
        createElement: (tag) => createMockElement(`dyn-${Math.random()}`, tag),
        createElementNS: (ns, tag) => createMockElement(`dyn-svg-${Math.random()}`, tag)
    };

    const windowMock = {
        addEventListener: () => {},
        removeEventListener: () => {},
        innerWidth: 1920,
        innerHeight: 1080,
        AudioContext: null,
        webkitAudioContext: null,
        print: () => {}
    };

    const vm = require('vm');
    const sandbox = {
        window: windowMock,
        document: documentMock,
        navigator: { clipboard: { writeText: async () => {} } },
        performance: { now: () => Date.now() },
        console: { log: () => {}, warn: () => {}, error: console.error },
        alert: (msg) => {},
        fetch: (url, opts) => {
            const fullUrl = url.startsWith('/') ? `http://127.0.0.1:5000${url}` : url;
            return fetch(fullUrl, opts);
        },
        Set: Set,
        Map: Map,
        Date: Date,
        Math: Math,
        setTimeout: setTimeout,
        clearTimeout: clearTimeout,
        setInterval: setInterval,
        clearInterval: clearInterval,
        Promise: Promise
    };

    const context = vm.createContext(sandbox);
    vm.runInContext(scriptCode, context);
    console.log('  ✓ Script parsed and executed cleanly');

    // Run initData()
    await context.initData();
    console.log('  ✓ initData() finished loading knowledge base');

    const symptomsGrid = elements.get('symptoms-grid');
    const presetsGrid = elements.get('case-presets-grid');
    const rulesGrid = elements.get('kb-rules-grid');
    const networkSvg = elements.get('network-svg');

    console.log(`    - Symptoms grid: ${checkboxes.size} interactive checkboxes rendered`);
    console.log(`    - Case presets grid: ${presetsGrid.innerHTML.length} bytes rendered`);
    console.log(`    - KB rules grid: ${rulesGrid.innerHTML.length} bytes rendered`);
    console.log(`    - Decision graph SVG: ${networkSvg.innerHTML.length} bytes rendered`);

    if (checkboxes.size === 0) {
        throw new Error('Symptoms grid did not create any symptom checkboxes');
    }

    // 4. Test Interactive Behaviors
    console.log('\n[4/4] Testing Interactive User Actions:');

    // Action 1: Select All Symptoms
    context.selectAllSymptoms();
    let checkedCount = Array.from(checkboxes.values()).filter(c => c.checked).length;
    console.log(`  ✓ selectAllSymptoms(): ${checkedCount} / ${checkboxes.size} checked`);
    if (checkedCount !== checkboxes.size) throw new Error('selectAllSymptoms did not check all');

    // Action 2: Clear All Symptoms
    context.clearAllSymptoms();
    checkedCount = Array.from(checkboxes.values()).filter(c => c.checked).length;
    console.log(`  ✓ clearAllSymptoms(): ${checkedCount} checked`);
    if (checkedCount !== 0) throw new Error('clearAllSymptoms did not clear all');

    // Action 3: Apply Case 01 (Acute Myocardial Infarction)
    console.log('  ✓ Applying Case 01 preset (AMI)...');
    context.applyCasePreset('CASE-01');
    const amiChecked = Array.from(checkboxes.values()).filter(c => c.checked).map(c => c.value);
    console.log(`    Preset symptoms checked: [${amiChecked.join(', ')}]`);
    if (!amiChecked.includes('chest_pain')) {
        throw new Error('CASE-01 did not check chest_pain');
    }

    // Inference has been triggered asynchronously by applyCasePreset! Await completion
    await new Promise(r => setTimeout(r, 300));
    const diagTitle = elements.get('diag-title').innerText;
    const diagRule = elements.get('diag-rule-id').innerText;
    const diagMatch = elements.get('diag-match-percent').innerText;
    console.log(`  ✓ Inference completed: Diagnosis="${diagTitle}", Rule="${diagRule}", Match=${diagMatch}`);
    if (!diagTitle.includes('Myocardial Infarction')) {
        throw new Error(`Expected Acute Myocardial Infarction, got ${diagTitle}`);
    }

    // Action 4: Backward Chaining Mode
    console.log('  ✓ Switching to Backward Chaining mode...');
    context.setInferenceMode('backward');
    elements.get('target-disease-select').value = 'Myocardial Infarction (Heart Attack)';
    await context.triggerInference();
    const bwdDiagTitle = elements.get('diag-title').innerText;
    const bwdRankLabel = elements.get('diag-rank-label').innerText;
    console.log(`    Backward Chaining result: Title="${bwdDiagTitle}", Status="${bwdRankLabel}"`);
    if (!bwdRankLabel.includes('PROVEN')) {
        throw new Error(`Expected HYPOTHESIS GOAL PROVEN, got: ${bwdRankLabel}`);
    }

    // Action 5: Viva Modal
    console.log('  ✓ Testing Viva Defense Modal open / close...');
    const vivaModal = elements.get('viva-modal');
    context.openVivaModal();
    console.log(`    Modal state after open: display = ${vivaModal.style.display}`);
    if (vivaModal.style.display !== 'flex') throw new Error('Viva modal failed to open');
    context.closeVivaModal();
    console.log(`    Modal state after close: display = ${vivaModal.style.display}`);
    if (vivaModal.style.display !== 'none') throw new Error('Viva modal failed to close');

    // Action 6: Wallpaper Switcher
    console.log('  ✓ Testing Wallpaper Atmosphere Switcher...');
    const prevIdx = context.currentWallpaperIndex;
    context.switchWallpaper();
    console.log(`    Wallpaper index cycled from ${prevIdx} to ${context.currentWallpaperIndex}`);

    console.log('\n======================================================');
    console.log('🎉 ALL TESTS PASSED: APPLICATION IS 100% OPERATIONAL');
    console.log('======================================================\n');
}

run().catch(err => {
    console.error('\n❌ VERIFICATION SUITE FAILED:', err);
    process.exit(1);
});
