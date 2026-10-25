import json
import os
from flask import Blueprint, jsonify, request, render_template, send_file
from app.services.llm_service import (
    get_provider,
    summarize_clinical_note,
    translate_clinical_jargon,
    extract_clinical_entities,
    compare_clinical_prompts,
    process_all_tasks
)

main_bp = Blueprint('main', __name__)

@main_bp.route('/api/sample-csv', methods=['GET'])
def download_sample_csv():
    """Allows downloading the preloaded sample CSV file for testing."""
    csv_path = os.path.join(os.path.dirname(__file__), 'data', 'sample_clinical_notes.csv')
    return send_file(csv_path, mimetype='text/csv', as_attachment=True, download_name='sample_clinical_notes.csv')

def _load_synthetic_notes():
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'synthetic_notes.json')
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading synthetic notes: {e}")
        return []

@main_bp.route('/')
def index():
    # If index.html exists, render it; otherwise return status JSON
    template_path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')
    if os.path.exists(template_path) and os.path.getsize(template_path) > 100:
        return render_template('index.html')
    return jsonify({
        "status": "online",
        "project": "Clinical Note Summariser & Jargon Translator",
        "stage": "Stage 3 - LLM Providers & API Ready",
        "active_provider": get_provider().provider_name,
        "endpoints": [
            "/api/notes",
            "/api/process-all",
            "/api/summarize",
            "/api/translate",
            "/api/extract",
            "/api/compare"
        ]
    })

@main_bp.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "active_provider": get_provider().provider_name
    })

@main_bp.route('/api/notes', methods=['GET'])
def get_synthetic_notes():
    """Returns the list of de-identified synthetic test cases."""
    notes = _load_synthetic_notes()
    return jsonify({"status": "success", "notes": notes})

@main_bp.route('/api/process-all', methods=['POST'])
def handle_process_all():
    """Processes all three core prompt engineering tasks in one payload."""
    data = request.get_json() or {}
    note = data.get('clinical_note', '').strip()
    provider_type = data.get('provider')

    if not note:
        return jsonify({"status": "error", "message": "Clinical note cannot be empty."}), 400

    result = process_all_tasks(note, provider_type)
    return jsonify(result)

@main_bp.route('/api/summarize', methods=['POST'])
def handle_summarize():
    """Processes layperson summarisation."""
    data = request.get_json() or {}
    note = data.get('clinical_note', '').strip()
    provider_type = data.get('provider')

    if not note:
        return jsonify({"status": "error", "message": "Clinical note cannot be empty."}), 400

    result = summarize_clinical_note(note, provider_type)
    return jsonify({"status": "success", "data": result})

@main_bp.route('/api/translate', methods=['POST'])
def handle_translate():
    """Processes jargon translation."""
    data = request.get_json() or {}
    note = data.get('clinical_note', '').strip()
    provider_type = data.get('provider')

    if not note:
        return jsonify({"status": "error", "message": "Clinical note cannot be empty."}), 400

    result = translate_clinical_jargon(note, provider_type)
    return jsonify({"status": "success", "translations": result})

@main_bp.route('/api/extract', methods=['POST'])
def handle_extract():
    """Processes clinical entity extraction."""
    data = request.get_json() or {}
    note = data.get('clinical_note', '').strip()
    provider_type = data.get('provider')

    if not note:
        return jsonify({"status": "error", "message": "Clinical note cannot be empty."}), 400

    result = extract_clinical_entities(note, provider_type)
    return jsonify({"status": "success", "entities": result})

@main_bp.route('/api/compare', methods=['POST'])
def handle_compare():
    """Executes A/B comparison between Naive and Structured prompts."""
    data = request.get_json() or {}
    note = data.get('clinical_note', '').strip()
    provider_type = data.get('provider')

    if not note:
        return jsonify({"status": "error", "message": "Clinical note cannot be empty."}), 400

    result = compare_clinical_prompts(note, provider_type)
    return jsonify({"status": "success", "comparison": result})
