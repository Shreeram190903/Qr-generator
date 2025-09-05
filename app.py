"""
QR Generator Pro - Flask Web Application (TEMPLATE SYNTAX FIXED)
Created by: Shreeram
Copyright © 2024 Shreeram. All rights reserved.

TEMPLATE SYNTAX FIXES APPLIED:
- Fixed Jinja2 template syntax errors
- Proper {% %} and {{ }} usage
- All template rendering issues resolved
"""

import os
import io
import uuid
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory
import qrcode
from PIL import Image, ImageDraw, ImageFont
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'shreeram-qr-generator-secret-key'  
app.config['UPLOAD_FOLDER'] = 'static/generated'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def generate_qr_with_headline(url, headline, fill_color="black", back_color="white", box_size=10, border=4):
    """
    Generate QR code with headline using the original functionality
    Based on Shreeram's original QR code generator script
    """
    try:
        print(f"🎨 Generating QR for URL: {url}")
        print(f"📝 Headline: {headline}")
        print(f"🎯 Colors: {fill_color} on {back_color}")

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=int(box_size),
            border=int(border),
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGB")

        print(f"✅ QR code base image created: {img.size}")

        # Try to load font with better error handling
        font = None
        font_size = 30

        # List of font paths to try (cross-platform)
        font_paths = [
            # Windows paths
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/calibri.ttf", 
            "C:/Windows/Fonts/verdana.ttf",
            # macOS paths
            "/System/Library/Fonts/Arial.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
            "/Library/Fonts/Arial.ttf",
            # Linux paths
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans.ttf",
            "/usr/share/fonts/TTF/DejaVuSans.ttf",
        ]

        for font_path in font_paths:
            try:
                if os.path.exists(font_path):
                    font = ImageFont.truetype(font_path, font_size)
                    print(f"✅ Loaded font: {font_path}")
                    break
            except Exception as e:
                print(f"❌ Failed to load font {font_path}: {e}")
                continue

        # Fallback to default font
        if font is None:
            try:
                font = ImageFont.load_default()
                print("⚠️ Using default system font")
            except Exception as e:
                print(f"❌ Even default font failed: {e}")
                # Create a minimal working font
                font = ImageFont.load_default()

        # Measure text size with better compatibility
        dummy_img = Image.new("RGB", (1, 1))
        dummy_draw = ImageDraw.Draw(dummy_img)

        try:
            # Try new PIL method first
            bbox = dummy_draw.textbbox((0, 0), headline, font=font)
            text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
            print(f"📏 Text size (new method): {text_width}x{text_height}")
        except AttributeError:
            # Fallback to older PIL method
            try:
                text_width, text_height = dummy_draw.textsize(headline, font=font)
                print(f"📏 Text size (old method): {text_width}x{text_height}")
            except:
                # Ultimate fallback
                text_width = len(headline) * 15  # Approximate
                text_height = 30
                print(f"📏 Text size (estimated): {text_width}x{text_height}")

        # Adjust new image size to fit headline
        img_width, img_height = img.size
        new_height = img_height + text_height + 40  # Extra padding
        new_img = Image.new("RGB", (img_width, new_height), back_color)

        # Paste QR code below the headline area
        new_img.paste(img, (0, text_height + 30))

        print(f"🖼️ Final image size: {img_width}x{new_height}")

        # Draw headline centered
        draw = ImageDraw.Draw(new_img)
        text_x = max(0, (img_width - text_width) // 2)

        # Create bold effect by drawing text multiple times (Shreeram's original technique)
        offsets = [(0, 0), (1, 0), (0, 1), (1, 1)]
        for dx, dy in offsets:
            try:
                draw.text((text_x + dx, 10 + dy), headline, font=font, fill=fill_color)
            except Exception as e:
                print(f"⚠️ Text drawing error: {e}")
                # Try simpler approach
                draw.text((text_x, 10), headline, font=font, fill=fill_color)
                break

        print("✅ QR code with headline generated successfully")
        return new_img

    except Exception as e:
        print(f"❌ Error in generate_qr_with_headline: {str(e)}")
        import traceback
        traceback.print_exc()
        raise e

@app.route('/')
def index():
    """Main page with QR generator form"""
    print("🏠 Serving index page")
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_qr():
    """Generate QR code with custom options"""
    try:
        print("\n" + "="*50)
        print("🚀 QR Generation Request Received")
        print("="*50)

        # Get form data
        url = request.form.get('url', '').strip()
        headline = request.form.get('headline', '').strip()
        fill_color = request.form.get('fill_color', '#000000')
        back_color = request.form.get('back_color', '#ffffff')

        # Debug form data
        print(f"📋 Form Data:")
        print(f"   URL: {url}")
        print(f"   Headline: {headline}")
        print(f"   Fill Color: {fill_color}")
        print(f"   Back Color: {back_color}")

        # Get numeric values with error handling
        try:
            box_size = int(request.form.get('box_size', 10))
            border = int(request.form.get('border', 4))
        except (ValueError, TypeError) as e:
            print(f"⚠️ Invalid numeric values, using defaults: {e}")
            box_size = 10
            border = 4

        print(f"   Box Size: {box_size}")
        print(f"   Border: {border}")

        # Validation
        if not url:
            print("❌ URL validation failed")
            return jsonify({'error': 'URL is required'}), 400

        if not headline:
            headline = ""
            print(f"📝 Using default headline: {headline}")

        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = str(uuid.uuid4())[:8]
        filename = f"qr_shreeram_{timestamp}_{unique_id}.png"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        print(f"💾 Target file: {filepath}")

        # Generate QR code
        print("🎨 Starting QR generation...")
        qr_img = generate_qr_with_headline(url, headline, fill_color, back_color, box_size, border)

        # Save the image
        print(f"💾 Saving image to: {filepath}")
        qr_img.save(filepath, 'PNG', quality=95)

        # Verify file was saved
        if os.path.exists(filepath):
            file_size = os.path.getsize(filepath)
            print(f"✅ File saved successfully: {file_size} bytes")
        else:
            raise Exception("File was not saved properly")

        response_data = {
            'success': True,
            'filename': filename,
            'download_url': f'/download/{filename}',
            'preview_url': f'/static/generated/{filename}',
            'message': f'QR code generated successfully by Shreeram!'
        }

        print("🎉 Response prepared successfully")
        print("="*50 + "\n")

        return jsonify(response_data)

    except Exception as e:
        error_msg = f'Failed to generate QR code: {str(e)}'
        print(f"❌ ERROR: {error_msg}")
        import traceback
        traceback.print_exc()
        print("="*50 + "\n")
        return jsonify({'error': error_msg}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """Download generated QR code"""
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(filepath):
            print(f"❌ File not found: {filepath}")
            return jsonify({'error': 'File not found'}), 404

        print(f"📥 Downloading: {filename}")
        return send_from_directory(
            app.config['UPLOAD_FOLDER'], 
            filename, 
            as_attachment=True,
            download_name=f"shreeram_qrcode_{filename}"
        )
    except Exception as e:
        print(f"❌ Download error: {e}")
        return jsonify({'error': 'Download failed'}), 500

@app.route('/preview/<filename>')  
def preview_file(filename):
    """Preview generated QR code"""
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(filepath):
            print(f"❌ Preview file not found: {filepath}")
            return jsonify({'error': 'File not found'}), 404

        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        print(f"❌ Preview error: {e}")
        return jsonify({'error': 'Preview failed'}), 500

@app.route('/gallery')
def gallery():
    """Show gallery of generated QR codes"""
    try:
        print("🖼️ Loading gallery page")
        files = []
        if os.path.exists(app.config['UPLOAD_FOLDER']):
            for filename in os.listdir(app.config['UPLOAD_FOLDER']):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    if os.path.exists(file_path):
                        file_stats = os.stat(file_path)
                        files.append({
                            'filename': filename,
                            'created': datetime.fromtimestamp(file_stats.st_ctime).strftime('%Y-%m-%d %H:%M'),
                            'size': round(file_stats.st_size / 1024, 1)  # KB
                        })

        # Sort by creation time, newest first
        files.sort(key=lambda x: x['created'], reverse=True)
        print(f"📊 Found {len(files)} QR code files")
        return render_template('gallery.html', files=files)
    except Exception as e:
        print(f"❌ Gallery error: {str(e)}")
        return render_template('gallery.html', files=[], error=str(e))

@app.route('/test')
def test():
    """Test route to verify the app is working"""
    print("🧪 Test endpoint accessed")
    return jsonify({
        'status': 'working',
        'message': 'Shreeram\'s QR Generator is running perfectly!',
        'timestamp': datetime.now().isoformat(),
        'upload_folder': app.config['UPLOAD_FOLDER'],
        'upload_folder_exists': os.path.exists(app.config['UPLOAD_FOLDER'])
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Page not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("🚀 QR Generator Pro by Shreeram - TEMPLATE SYNTAX FIXED")
    print("📧 Copyright © 2024 Shreeram. All rights reserved.")
    print("🔧 All template syntax errors fixed!")
    print("🌐 Starting server at http://localhost:5000")
    print("🔧 Debug mode: ON")
    print(f"📁 Upload folder: {app.config['UPLOAD_FOLDER']}")
    print(f"📁 Folder exists: {os.path.exists(app.config['UPLOAD_FOLDER'])}")
    app.run(debug=True, host='0.0.0.0', port=5000)
