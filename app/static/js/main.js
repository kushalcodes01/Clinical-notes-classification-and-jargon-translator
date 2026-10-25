/**
 * Clinical Note Summariser & Jargon Translator
 * Interactive Frontend Controller
 */

(function () {
  'use strict';

  // State Management
  const state = {
    notes: [],
    currentCaseId: 'case-1',
    activeTab: 'tab-summary',
    jargonData: [],
    selectedCategory: 'all',
    isLoading: false,
    csvRecords: [],
    currentCsvFileName: '',
    lastProcessedResult: null
  };

  // DOM Elements
  const DOM = {
    disclaimerBar: document.getElementById('disclaimer-bar'),
    disclaimerDismissBtn: document.getElementById('disclaimer-dismiss-btn'),
    providerLabel: document.getElementById('provider-label'),
    providerPill: document.getElementById('provider-pill'),
    clinicalNoteInput: document.getElementById('clinical-note-input'),
    wordCount: document.getElementById('word-count'),
    charCount: document.getElementById('char-count'),
    patientTag: document.getElementById('patient-tag'),
    btnProcessAll: document.getElementById('btn-process-all'),
    btnComparePrompts: document.getElementById('btn-compare-prompts'),
    caseChips: document.querySelectorAll('.case-chip'),
    btnClearNote: document.getElementById('clear-note-btn'),
    btnResetSample: document.getElementById('reset-sample-btn'),
    csvFileInput: document.getElementById('csv-file-input'),
    uploadCsvBtn: document.getElementById('upload-csv-btn'),
    csvRowSelect: document.getElementById('csv-row-select'),
    exportCsvBtn: document.getElementById('export-csv-btn'),
    tabButtons: document.querySelectorAll('.tab-btn'),
    tabContents: document.querySelectorAll('.tab-content'),
    loadingSpinner: document.getElementById('loading-spinner'),
    loadingMsg: document.getElementById('loading-msg'),
    emptyState: document.getElementById('empty-state'),
    summaryContainer: document.getElementById('summary-render-container'),
    copySummaryBtn: document.getElementById('copy-summary-btn'),
    jargonCardsContainer: document.getElementById('jargon-cards-container'),
    jargonFilterInput: document.getElementById('jargon-filter-input'),
    categoryChips: document.querySelectorAll('.cat-chip'),
    jargonCountBadge: document.getElementById('jargon-count'),
    entitiesDiagnoses: document.getElementById('entities-diagnoses-list'),
    entitiesMedications: document.getElementById('entities-medications-list'),
    entitiesSymptoms: document.getElementById('entities-symptoms-list'),
    entitiesTests: document.getElementById('entities-tests-list'),
    entitiesFollowup: document.getElementById('entities-followup-list'),
    entitiesMissing: document.getElementById('entities-missing-list'),
    naiveOutputBox: document.getElementById('naive-output-box'),
    naiveFlawsList: document.getElementById('naive-flaws-list'),
    structuredOutputBox: document.getElementById('structured-output-box'),
    structuredStrengthsList: document.getElementById('structured-strengths-list'),
    rubricTableBody: document.getElementById('rubric-table-body'),
    methodologyModal: document.getElementById('methodology-modal'),
    openMethodologyBtn: document.getElementById('open-methodology-btn'),
    closeMethodologyBtn: document.getElementById('close-methodology-btn')
  };

  // Safe fallback Markdown formatter (in case marked.js CDN is unavailable offline)
  function renderMarkdown(rawText) {
    if (!rawText) return '';
    if (window.marked && typeof window.marked.parse === 'function') {
      return window.marked.parse(rawText);
    }
    // Simple offline markdown parser
    let html = rawText
      .replace(/^### (.*$)/gim, '<h3>$1</h3>')
      .replace(/^## (.*$)/gim, '<h2>$1</h2>')
      .replace(/^# (.*$)/gim, '<h1>$1</h1>')
      .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/gim, '<em>$1</em>')
      .replace(/^\s*-\s+(.*$)/gim, '<li>$1</li>')
      .replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>')
      .replace(/\n$/gim, '<br />');
    return html;
  }

  // Update text counter
  function updateCounters() {
    const text = DOM.clinicalNoteInput.value.trim();
    const chars = text.length;
    const words = text ? text.split(/\s+/).length : 0;
    DOM.wordCount.textContent = `${words} words`;
    DOM.charCount.textContent = `${chars} chars`;
  }

  // Set Loading State
  function setLoading(loading, message = 'Processing Prompt Pipeline...') {
    state.isLoading = loading;
    if (loading) {
      DOM.loadingSpinner.classList.remove('hidden');
      DOM.loadingMsg.textContent = message;
      DOM.emptyState.classList.add('hidden');
      DOM.tabContents.forEach(tab => tab.classList.add('hidden'));
    } else {
      DOM.loadingSpinner.classList.add('hidden');
    }
  }

  // Switch Active Tab
  function switchTab(targetTabId) {
    state.activeTab = targetTabId;
    DOM.tabButtons.forEach(btn => {
      const isTarget = btn.getAttribute('data-target') === targetTabId;
      btn.classList.toggle('active', isTarget);
      btn.setAttribute('aria-selected', isTarget);
    });

    if (!state.isLoading) {
      DOM.emptyState.classList.add('hidden');
      DOM.tabContents.forEach(tab => {
        tab.classList.toggle('hidden', tab.id !== targetTabId);
      });
    }
  }

  // Load Initial Synthetic Notes
  async function loadInitialData() {
    try {
      // 1. Fetch Provider Health
      const healthRes = await fetch('/health');
      if (healthRes.ok) {
        const health = await healthRes.json();
        DOM.providerLabel.textContent = health.active_provider || 'Mock Provider';
      }

      // 2. Fetch Synthetic Cases
      const notesRes = await fetch('/api/notes');
      if (notesRes.ok) {
        const data = await notesRes.json();
        state.notes = data.notes || [];
        if (state.notes.length > 0) {
          selectCase('case-1');
        }
      }
    } catch (err) {
      console.warn('Network issue fetching notes, using embedded defaults:', err);
      DOM.providerLabel.textContent = 'Mock Provider (Offline)';
    }
  }

  // Select Synthetic Case
  function selectCase(caseId) {
    state.currentCaseId = caseId;
    DOM.caseChips.forEach(chip => {
      chip.classList.toggle('active', chip.getAttribute('data-case') === caseId);
    });

    const selected = state.notes.find(n => n.id === caseId);
    if (selected) {
      DOM.clinicalNoteInput.value = selected.clinical_note;
      DOM.patientTag.textContent = selected.patient_display || 'Synthetic Record';
      updateCounters();
    }
  }

  // Populate Rendered Summary
  function renderSummaryTab(markdownText) {
    DOM.summaryContainer.innerHTML = renderMarkdown(markdownText);
  }

  // Populate Jargon Cards
  function renderJargonTab(jargonList) {
    state.jargonData = jargonList || [];
    DOM.jargonCountBadge.textContent = state.jargonData.length;
    applyJargonFilters();
  }

  // Filter Jargon Cards
  function applyJargonFilters() {
    const query = DOM.jargonFilterInput.value.toLowerCase().trim();
    const cat = state.selectedCategory;

    const filtered = state.jargonData.filter(item => {
      const matchCat = (cat === 'all') || (item.category && item.category.toLowerCase().includes(cat));
      const matchQuery = !query ||
        (item.term && item.term.toLowerCase().includes(query)) ||
        (item.plain_english && item.plain_english.toLowerCase().includes(query)) ||
        (item.why_it_matters && item.why_it_matters.toLowerCase().includes(query));
      return matchCat && matchQuery;
    });

    if (filtered.length === 0) {
      DOM.jargonCardsContainer.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; color: var(--text-muted); padding: 2rem;">
          No matching medical terms found for "${query}".
        </div>
      `;
      return;
    }

    DOM.jargonCardsContainer.innerHTML = filtered.map(item => {
      const category = (item.category || 'General').toLowerCase();
      let badgeClass = 'badge-general';
      if (category.includes('diagnosis')) badgeClass = 'badge-diagnosis';
      else if (category.includes('symptom')) badgeClass = 'badge-symptom';
      else if (category.includes('medication')) badgeClass = 'badge-medication';
      else if (category.includes('procedure')) badgeClass = 'badge-procedure';
      else if (category.includes('test')) badgeClass = 'badge-test';
      else if (category.includes('anatomy')) badgeClass = 'badge-anatomy';

      return `
        <div class="jargon-card">
          <div class="jargon-card-header">
            <span class="jargon-term">${escapeHtml(item.term)}</span>
            <span class="jargon-cat-badge ${badgeClass}">${escapeHtml(item.category || 'Term')}</span>
          </div>
          <p class="jargon-plain">${escapeHtml(item.plain_english)}</p>
          <div class="jargon-why">
            <strong>Why it matters:</strong> ${escapeHtml(item.why_it_matters || 'Helps understand treatment.')}
          </div>
        </div>
      `;
    }).join('');
  }

  // Populate Structured Entities
  function renderEntitiesTab(entities) {
    if (!entities) return;

    // Diagnoses
    if (entities.diagnoses && entities.diagnoses.length > 0) {
      DOM.entitiesDiagnoses.innerHTML = entities.diagnoses.map(d => {
        const isConfirmed = d.status === 'confirmed';
        return `
          <div class="entity-card-row">
            <div class="entity-row-top">
              <span class="entity-name">${escapeHtml(d.condition)}</span>
              <span class="status-badge ${isConfirmed ? 'status-confirmed' : 'status-suspected'}">
                ${isConfirmed ? '✔ Confirmed' : '⚠️ Rule-out / Suspected'}
              </span>
            </div>
            ${d.notes ? `<p class="entity-detail-text">${escapeHtml(d.notes)}</p>` : ''}
          </div>
        `;
      }).join('');
    } else {
      DOM.entitiesDiagnoses.innerHTML = '<p class="entity-detail-text">No explicit diagnoses detected.</p>';
    }

    // Medications
    if (entities.medications && entities.medications.length > 0) {
      DOM.entitiesMedications.innerHTML = entities.medications.map(m => `
        <div class="entity-card-row">
          <div class="entity-row-top">
            <span class="entity-name">💊 ${escapeHtml(m.name)}</span>
            <span class="meta-badge">${escapeHtml(m.dosage || 'Dosage not specified')}</span>
          </div>
          <p class="entity-detail-text">
            <strong>Instructions:</strong> ${escapeHtml(m.frequency_and_route || 'As directed')}
            ${m.purpose_in_note ? ` &bull; <em>${escapeHtml(m.purpose_in_note)}</em>` : ''}
          </p>
        </div>
      `).join('');
    } else {
      DOM.entitiesMedications.innerHTML = '<p class="entity-detail-text">No medications listed.</p>';
    }

    // Symptoms
    if (entities.symptoms && entities.symptoms.length > 0) {
      DOM.entitiesSymptoms.innerHTML = entities.symptoms.map(s => `
        <span class="symptom-tag">${escapeHtml(s)}</span>
      `).join('');
    } else {
      DOM.entitiesSymptoms.innerHTML = '<span class="entity-detail-text">No symptoms specified.</span>';
    }

    // Tests & Procedures
    if (entities.tests_and_procedures && entities.tests_and_procedures.length > 0) {
      DOM.entitiesTests.innerHTML = entities.tests_and_procedures.map(t => `
        <div class="entity-card-row">
          <div class="entity-row-top">
            <span class="entity-name">🔬 ${escapeHtml(t.name)}</span>
          </div>
          <p class="entity-detail-text"><strong>Result / Finding:</strong> ${escapeHtml(t.finding_or_result || 'Pending')}</p>
        </div>
      `).join('');
    } else {
      DOM.entitiesTests.innerHTML = '<p class="entity-detail-text">No tests listed in note.</p>';
    }

    // Follow-ups
    if (entities.follow_up_instructions && entities.follow_up_instructions.length > 0) {
      DOM.entitiesFollowup.innerHTML = entities.follow_up_instructions.map(f => `
        <li>${escapeHtml(f)}</li>
      `).join('');
    } else {
      DOM.entitiesFollowup.innerHTML = '<li>Consult with your doctor for follow-up scheduling.</li>';
    }

    // Missing & Uncertain Information
    if (entities.uncertain_or_missing_information && entities.uncertain_or_missing_information.length > 0) {
      DOM.entitiesMissing.innerHTML = entities.uncertain_or_missing_information.map(m => `
        <li>${escapeHtml(m)}</li>
      `).join('');
    } else {
      DOM.entitiesMissing.innerHTML = '<li>All standard clinical fields were addressed in this record.</li>';
    }
  }

  // Populate A/B Comparison Tab
  function renderComparisonTab(comparison) {
    if (!comparison) return;

    // Naive Column
    DOM.naiveOutputBox.textContent = comparison.naive_output || '';
    if (comparison.flaws_in_naive_output) {
      DOM.naiveFlawsList.innerHTML = comparison.flaws_in_naive_output.map(f => `
        <li>${escapeHtml(f)}</li>
      `).join('');
    }

    // Structured Column
    DOM.structuredOutputBox.innerHTML = renderMarkdown(comparison.structured_output || '');
    if (comparison.strengths_in_structured_output) {
      DOM.structuredStrengthsList.innerHTML = comparison.strengths_in_structured_output.map(s => `
        <li>${escapeHtml(s)}</li>
      `).join('');
    }

    // Criteria Rubric Table
    if (comparison.comparison_criteria) {
      DOM.rubricTableBody.innerHTML = comparison.comparison_criteria.map(c => `
        <tr>
          <td>${escapeHtml(c.dimension)}</td>
          <td>${escapeHtml(c.naive_approach)}</td>
          <td>${escapeHtml(c.structured_approach)}</td>
        </tr>
      `).join('');
    }
  }

  // Run Full Pipeline Event Handler
  async function handleRunFullPipeline() {
    const text = DOM.clinicalNoteInput.value.trim();
    if (!text) {
      alert('Please enter or select a clinical note to summarize.');
      return;
    }

    setLoading(true, 'Running Prompt Engineering Pipeline (RCTCO Grounding)...');

    try {
      const res = await fetch('/api/process-all', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ clinical_note: text })
      });

      const data = await res.json();
      if (!res.ok || data.status === 'error') {
        throw new Error(data.message || 'Error processing clinical note');
      }

      // Save last processed result for CSV export
      state.lastProcessedResult = {
        note: text,
        summary: data.summary,
        translations: data.translations || [],
        entities: data.entities || {}
      };

      // Populate Tabs
      renderSummaryTab(data.summary);
      renderJargonTab(data.translations);
      renderEntitiesTab(data.entities);

      setLoading(false);
      switchTab('tab-summary');
    } catch (err) {
      setLoading(false);
      alert('Analysis Error: ' + err.message);
    }
  }

  // Parse CSV adhering to RFC 4180 (handles quoted multiline cells)
  function parseCSV(text) {
    const lines = [];
    let row = [''];
    let inQuotes = false;

    for (let i = 0; i < text.length; i++) {
      const char = text[i];
      const next = text[i + 1];

      if (char === '"') {
        if (inQuotes && next === '"') {
          row[row.length - 1] += '"';
          i++; // Skip escaped quote
        } else {
          inQuotes = !inQuotes;
        }
      } else if (char === ',' && !inQuotes) {
        row.push('');
      } else if ((char === '\r' || char === '\n') && !inQuotes) {
        if (char === '\r' && next === '\n') {
          i++;
        }
        lines.push(row);
        row = [''];
      } else {
        row[row.length - 1] += char;
      }
    }

    if (row.length > 1 || row[0] !== '') {
      lines.push(row);
    }

    return lines;
  }

  // Handle CSV file upload
  function handleCSVUpload(e) {
    const file = e.target.files && e.target.files[0];
    if (!file) return;

    state.currentCsvFileName = file.name;
    const reader = new FileReader();

    reader.onload = function (evt) {
      try {
        const content = evt.target.result;
        const rows = parseCSV(content);

        if (rows.length < 2) {
          alert('CSV file appears to be empty or missing data rows.');
          return;
        }

        const headers = rows[0].map(h => h.trim().toLowerCase());
        
        // Find column index for clinical note
        let noteColIdx = headers.findIndex(h => 
          h.includes('clinical_note') || h.includes('note') || h.includes('text') || h.includes('history')
        );
        if (noteColIdx === -1) {
          // Fallback to the column with the highest average length
          let maxLen = -1;
          for (let col = 0; col < headers.length; col++) {
            const avg = rows.slice(1).reduce((acc, r) => acc + (r[col] ? r[col].length : 0), 0) / (rows.length - 1);
            if (avg > maxLen) {
              maxLen = avg;
              noteColIdx = col;
            }
          }
        }

        // Find specialty and demographics column indices if present
        const specialtyIdx = headers.findIndex(h => h.includes('specialty') || h.includes('department'));
        const demoIdx = headers.findIndex(h => h.includes('patient') || h.includes('demographics') || h.includes('age'));

        state.csvRecords = [];
        DOM.csvRowSelect.innerHTML = '<option value="">Select a record from CSV...</option>';

        for (let i = 1; i < rows.length; i++) {
          const rowData = rows[i];
          const noteText = rowData[noteColIdx] ? rowData[noteColIdx].trim() : '';
          if (!noteText) continue;

          const specialty = specialtyIdx !== -1 && rowData[specialtyIdx] ? rowData[specialtyIdx].trim() : `Record ${i}`;
          const demo = demoIdx !== -1 && rowData[demoIdx] ? `(${rowData[demoIdx].trim()})` : '';

          state.csvRecords.push({
            index: i,
            specialty: specialty,
            demo: demo,
            note: noteText
          });

          const opt = document.createElement('option');
          opt.value = String(state.csvRecords.length - 1);
          opt.textContent = `Row ${i}: ${specialty} ${demo}`;
          DOM.csvRowSelect.appendChild(opt);
        }

        if (state.csvRecords.length === 0) {
          alert('No valid clinical notes found in the uploaded CSV.');
          return;
        }

        // Make selector visible and select first record
        DOM.csvRowSelect.classList.remove('hidden');
        DOM.csvRowSelect.value = '0';
        loadCsvRecord(0);

        // Deselect case chips
        DOM.caseChips.forEach(chip => chip.classList.remove('active'));

      } catch (err) {
        alert('Failed to parse CSV file: ' + err.message);
      }
    };

    reader.readAsText(file);
    // Reset file input so re-uploading the same file triggers change
    e.target.value = '';
  }

  // Load selected CSV record into editor
  function loadCsvRecord(recordIdx) {
    const record = state.csvRecords[recordIdx];
    if (!record) return;

    DOM.clinicalNoteInput.value = record.note;
    DOM.patientTag.textContent = `CSV: ${state.currentCsvFileName} (Row ${record.index})`;
    updateCounters();
  }

  // Handle Export to CSV
  function handleExportCSV() {
    if (!state.lastProcessedResult) {
      alert('Please run the pipeline first to generate clinical summary and extracted entities before exporting.');
      return;
    }

    const res = state.lastProcessedResult;
    const medNames = (res.entities.medications || []).map(m => m.name + (m.dosage ? ` (${m.dosage})` : '')).join('; ');
    const missingInfo = (res.entities.uncertain_or_missing_information || []).join('; ');
    const jargonTerms = (res.translations || []).map(t => `${t.term}: ${t.plain_english}`).join(' | ');

    // Helper to escape CSV cell
    const escapeCSV = (val) => {
      const str = String(val || '').replace(/"/g, '""');
      return `"${str}"`;
    };

    const headers = [
      'note_id',
      'source_document',
      'original_clinical_note',
      'plain_language_summary',
      'jargon_terms_count',
      'translated_jargon_glossary',
      'extracted_medications',
      'missing_information_flag'
    ];

    const row = [
      escapeCSV(DOM.patientTag.textContent),
      escapeCSV(state.currentCsvFileName || 'Direct Input / Preloaded Case'),
      escapeCSV(res.note),
      escapeCSV(res.summary),
      escapeCSV(res.translations.length),
      escapeCSV(jargonTerms),
      escapeCSV(medNames),
      escapeCSV(missingInfo)
    ];

    const csvContent = '\uFEFF' + headers.join(',') + '\n' + row.join(',');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const downloadLink = document.createElement('a');
    downloadLink.setAttribute('href', url);
    downloadLink.setAttribute('download', `clinical_summary_export_${Date.now()}.csv`);
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
    URL.revokeObjectURL(url);
  }

  // Run A/B Comparison Event Handler
  async function handleComparePrompts() {
    const text = DOM.clinicalNoteInput.value.trim();
    if (!text) {
      alert('Please enter or select a clinical note for A/B comparison.');
      return;
    }

    setLoading(true, 'Running A/B Comparison: Naive vs Structured Prompt...');

    try {
      const res = await fetch('/api/compare', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ clinical_note: text })
      });

      const data = await res.json();
      if (!res.ok || data.status === 'error') {
        throw new Error(data.message || 'Error executing prompt comparison');
      }

      renderComparisonTab(data.comparison);
      setLoading(false);
      switchTab('tab-compare');
    } catch (err) {
      setLoading(false);
      alert('Comparison Error: ' + err.message);
    }
  }

  // Copy Summary Handler
  function handleCopySummary() {
    const text = DOM.summaryContainer.innerText || DOM.summaryContainer.textContent;
    if (!text) return;

    navigator.clipboard.writeText(text).then(() => {
      const originalText = DOM.copySummaryBtn.textContent;
      DOM.copySummaryBtn.textContent = '✔ Copied!';
      setTimeout(() => {
        DOM.copySummaryBtn.textContent = originalText;
      }, 2000);
    });
  }

  // Utility to prevent XSS
  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  // Event Listeners Setup
  function initEventListeners() {
    DOM.clinicalNoteInput.addEventListener('input', updateCounters);

    DOM.caseChips.forEach(chip => {
      chip.addEventListener('click', () => {
        const caseId = chip.getAttribute('data-case');
        selectCase(caseId);
      });
    });

    DOM.btnClearNote.addEventListener('click', () => {
      DOM.clinicalNoteInput.value = '';
      DOM.patientTag.textContent = 'Custom Note';
      updateCounters();
      DOM.clinicalNoteInput.focus();
    });

    DOM.btnResetSample.addEventListener('click', () => {
      selectCase(state.currentCaseId);
    });

    DOM.tabButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        const target = btn.getAttribute('data-target');
        switchTab(target);
      });
    });

    DOM.btnProcessAll.addEventListener('click', handleRunFullPipeline);
    DOM.btnComparePrompts.addEventListener('click', handleComparePrompts);
    DOM.copySummaryBtn.addEventListener('click', handleCopySummary);

    // CSV Event Listeners
    DOM.uploadCsvBtn.addEventListener('click', () => {
      DOM.csvFileInput.click();
    });

    DOM.csvFileInput.addEventListener('change', handleCSVUpload);

    DOM.csvRowSelect.addEventListener('change', (e) => {
      const idx = parseInt(e.target.value, 10);
      if (!isNaN(idx)) {
        loadCsvRecord(idx);
      }
    });

    DOM.exportCsvBtn.addEventListener('click', handleExportCSV);

    // Jargon search filter
    DOM.jargonFilterInput.addEventListener('input', applyJargonFilters);

    // Category chips filter
    DOM.categoryChips.forEach(chip => {
      chip.addEventListener('click', () => {
        DOM.categoryChips.forEach(c => c.classList.remove('active'));
        chip.classList.add('active');
        state.selectedCategory = chip.getAttribute('data-cat');
        applyJargonFilters();
      });
    });

    // Methodology Modal
    DOM.openMethodologyBtn.addEventListener('click', () => {
      DOM.methodologyModal.showModal();
    });

    DOM.closeMethodologyBtn.addEventListener('click', () => {
      DOM.methodologyModal.close();
    });

    DOM.methodologyModal.addEventListener('click', (e) => {
      if (e.target === DOM.methodologyModal) {
        DOM.methodologyModal.close();
      }
    });

    // Dismiss disclaimer bar
    DOM.disclaimerDismissBtn.addEventListener('click', () => {
      DOM.disclaimerBar.style.display = 'none';
    });
  }

  // Initialize on DOM Ready
  document.addEventListener('DOMContentLoaded', () => {
    initEventListeners();
    loadInitialData();
  });

})();
