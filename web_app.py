import os
import logging
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import tempfile
import shutil
import json
from datetime import datetime

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from llm.google_unified import GoogleUnifiedClient
from llm.openai import OpenAIClient
from llm.anthropic import AnthropicClient
from processor import process_single_file
from prompt import BASE_PROMPT

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {'ppt', 'pptx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return jsonify({'status': 'ok', 'message': 'Server is running'})

@app.route('/upload', methods=['POST'])
def upload_file():
    logger.info("Upload request received")
    try:
        # Check if file is present
        if 'file' not in request.files:
            logger.error("No file in request")
            return jsonify({'error': '파일이 선택되지 않았습니다'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '파일이 선택되지 않았습니다'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': 'PPT 또는 PPTX 파일만 업로드 가능합니다'}), 400

        # Get form data
        instructions = request.form.get('instructions', '')
        client_type = request.form.get('client', 'openai')
        model = request.form.get('model', 'gpt-4o-mini')
        api_key = request.form.get('api_key', '')

        # Validate API key
        if not api_key:
            return jsonify({'error': 'API 키를 입력해주세요'}), 400

        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(upload_path)

        logger.info(f"File uploaded: {unique_filename}")

        # Create output directory for this file
        output_dir = Path(app.config['OUTPUT_FOLDER']) / timestamp
        output_dir.mkdir(parents=True, exist_ok=True)

        # Prepare prompt
        if instructions and instructions.strip():
            prompt = f"{BASE_PROMPT}\n\n추가 지시사항:\n{instructions}"
        else:
            prompt = BASE_PROMPT

        # Initialize LLM client
        try:
            if client_type == "openai":
                model_instance = OpenAIClient(api_key=api_key, model=model)
            elif client_type == "anthropic":
                model_instance = AnthropicClient(api_key=api_key, model=model)
            elif client_type == "gemini":
                model_instance = GoogleUnifiedClient(
                    api_key=api_key,
                    model=model,
                    use_vertex=False
                )
            else:
                return jsonify({'error': '지원하지 않는 LLM 클라이언트입니다'}), 400

            logger.info(f"Initialized {client_type} client with model {model}")
        except Exception as e:
            logger.error(f"Failed to initialize LLM client: {str(e)}")
            return jsonify({'error': f'LLM 클라이언트 초기화 실패: {str(e)}'}), 500

        # Process the file
        try:
            # Use Docker-based LibreOffice if available, otherwise local
            libreoffice_url = os.environ.get('LIBREOFFICE_URL', None)

            # Hardcode LibreOffice path for Windows
            libreoffice_path = r"C:\Program Files\LibreOffice\program\soffice.exe"
            logger.info(f"Using hardcoded LibreOffice path: {libreoffice_path}")

            result = process_single_file(
                ppt_file=Path(upload_path),
                output_dir=output_dir,
                libreoffice_path=Path(libreoffice_path) if libreoffice_path else None,
                libreoffice_endpoint=libreoffice_url,
                model_instance=model_instance,
                rate_limit=60,
                prompt=prompt,
                save_pdf=False,
                save_images=False,
                max_workers=10
            )

            ppt_path, image_paths = result

            if not image_paths:
                return jsonify({'error': '파일 처리에 실패했습니다'}), 500

            # Read the generated JSON
            json_file = output_dir / f"{Path(upload_path).stem}.json"
            if not json_file.exists():
                return jsonify({'error': '스크립트 생성에 실패했습니다'}), 500

            with open(json_file, 'r', encoding='utf-8') as f:
                result_data = json.load(f)

            # Clean up uploaded file
            try:
                os.remove(upload_path)
            except:
                pass

            return jsonify({
                'success': True,
                'result': result_data,
                'output_file': str(json_file)
            })

        except Exception as e:
            logger.error(f"Error processing file: {str(e)}", exc_info=True)
            return jsonify({'error': f'파일 처리 중 오류가 발생했습니다: {str(e)}'}), 500

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return jsonify({'error': f'오류가 발생했습니다: {str(e)}'}), 500

@app.route('/download/<path:filename>')
def download_file(filename):
    try:
        file_path = Path(app.config['OUTPUT_FOLDER']) / filename
        if not file_path.exists():
            return jsonify({'error': '파일을 찾을 수 없습니다'}), 404

        return send_file(file_path, as_attachment=True)
    except Exception as e:
        logger.error(f"Error downloading file: {str(e)}")
        return jsonify({'error': '파일 다운로드 중 오류가 발생했습니다'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
