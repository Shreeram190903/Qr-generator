"""
QR Generator Pro - Flask Web Application (VERCEL COMPATIBLE)
Created by: Shreeram
Copyright © 2024 Shreeram. All rights reserved.

VERCEL COMPATIBILITY FIXES:
- In-memory QR code generation (no file system writes)
- Base64 data URLs for immediate display
- Serverless-friendly font loading
- No local file storage dependencies
"""

import os
import io
import uuid
import base64
from datetime import datetime
from flask import Flask, render_template, request, jsonify, Response
import qrcode
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'shreeram-qr-generator-vercel-key')

def generate_qr_with_headline_base64(url, headline, fill_color="black", back_color="white", box_size=10, border=4):
    """
    Generate QR code with headline and return as base64 data URL
    VERCEL-COMPATIBLE: No file system operations
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

        # Load font - VERCEL COMPATIBLE approach
        font = None
        font_size = 60

        try:
            # Try to load default font - works in most environments
            font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Linux example
            font_size = 30  # Bigger font
            font = ImageFont.truetype(font_path, font_size)
            print(f"✅ Loaded font: {font_path} with size {font_size}")
        except Exception as e:
            print(f"⚠️ Font loading failed, using basic font: {e}")
            # Create a basic font fallback
            font = ImageFont.load_default()

        # Measure text size
        dummy_img = Image.new("RGB", (1, 1))
        dummy_draw = ImageDraw.Draw(dummy_img)

        try:
            # Try new PIL method
            bbox = dummy_draw.textbbox((0, 0), headline, font=font)
            text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
            print(f"📏 Text size: {text_width}x{text_height}")
        except AttributeError:
            # Fallback for older PIL versions
            try:
                text_width, text_height = dummy_draw.textsize(headline, font=font)
                print(f"📏 Text size (fallback): {text_width}x{text_height}")
            except:
                # Ultimate fallback
                text_width = len(headline) * 15
                text_height = 30
                print(f"📏 Text size (estimated): {text_width}x{text_height}")

        # Create final image with headline
        img_width, img_height = img.size
        new_height = img_height + text_height + 40
        new_img = Image.new("RGB", (img_width, new_height), back_color)

        # Paste QR code below headline
        new_img.paste(img, (0, text_height + 30))

        print(f"🖼️ Final image size: {img_width}x{new_height}")

        # Draw headline centered
        draw = ImageDraw.Draw(new_img)
        text_x = max(0, (img_width - text_width) // 2)

        # Create bold effect (Shreeram's original technique)
        offsets = [(0, 0), (1, 0), (0, 1), (1, 1)]
        for dx, dy in offsets:
            try:
                draw.text((text_x + dx, 10 + dy), headline, font=font, fill=fill_color)
            except Exception as e:
                print(f"⚠️ Text drawing issue: {e}")
                draw.text((text_x, 10), headline, font=font, fill=fill_color)
                break

        # VERCEL COMPATIBILITY: Convert to base64 data URL instead of saving file
        buffer = io.BytesIO()
        new_img.save(buffer, format='PNG', quality=95)
        buffer.seek(0)

        # Create base64 data URL
        img_data = buffer.getvalue()
        img_base64 = base64.b64encode(img_data).decode('utf-8')
        data_url = f"data:image/png;base64,{img_base64}"

        print("✅ QR code generated as base64 data URL successfully")
        return data_url, img_data

    except Exception as e:
        print(f"❌ Error in generate_qr_with_headline_base64: {str(e)}")
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
    """Generate QR code with custom options - VERCEL COMPATIBLE"""
    try:
        print("\n" + "="*50)
        print("🚀 QR Generation Request (Vercel Compatible)")
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

        # Get numeric values
        try:
            box_size = int(request.form.get('box_size', 10))
            border = int(request.form.get('border', 4))
        except (ValueError, TypeError):
            box_size = 10
            border = 4

        print(f"   Box Size: {box_size}")
        print(f"   Border: {border}")

        # Validation
        if not url:
            print("❌ URL validation failed")
            return jsonify({'error': 'URL is required'}), 400

        if not headline:
            headline = "QR Code by Shreeram"
            print(f"📝 Using default headline: {headline}")

        # Generate unique ID for this QR code
        unique_id = str(uuid.uuid4())[:8]
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        qr_id = f"qr_{timestamp}_{unique_id}"

        print(f"🆔 QR ID: {qr_id}")

        # Generate QR code as base64 data URL (VERCEL COMPATIBLE)
        print("🎨 Starting in-memory QR generation...")
        data_url, img_data = generate_qr_with_headline_base64(url, headline, fill_color, back_color, box_size, border)

        # Store in session or return directly
        file_size_kb = round(len(img_data) / 1024, 1)

        response_data = {
            'success': True,
            'qr_id': qr_id,
            'data_url': data_url,  # Base64 data URL for immediate display
            'download_url': f'/download/{qr_id}',  # For download endpoint
            'size_kb': file_size_kb,
            'message': f'QR code generated successfully by Shreeram!'
        }

        # Store the image data in memory for download (simple approach)
        # In production, you might use Redis or database
        app.config[f'qr_data_{qr_id}'] = img_data

        print("🎉 Response prepared successfully (Vercel Compatible)")
        print("="*50 + "\n")

        return jsonify(response_data)

    except Exception as e:
        error_msg = f'Failed to generate QR code: {str(e)}'
        print(f"❌ ERROR: {error_msg}")
        import traceback
        traceback.print_exc()
        print("="*50 + "\n")
        return jsonify({'error': error_msg}), 500

@app.route('/download/<qr_id>')
def download_qr(qr_id):
    """Download QR code - VERCEL COMPATIBLE"""
    try:
        print(f"📥 Download request for QR ID: {qr_id}")

        # Retrieve image data from memory
        img_data = app.config.get(f'qr_data_{qr_id}')

        if not img_data:
            print(f"❌ QR data not found for ID: {qr_id}")
            return jsonify({'error': 'QR code not found or expired'}), 404

        print(f"✅ Serving download for QR: {qr_id}")

        return Response(
            img_data,
            mimetype='image/png',
            headers={
                'Content-Disposition': f'attachment; filename=shreeram_qr_{qr_id}.png',
                'Content-Type': 'image/png'
            }
        )

    except Exception as e:
        print(f"❌ Download error: {e}")
        return jsonify({'error': 'Download failed'}), 500

@app.route('/gallery')
def gallery():
    """Gallery page - VERCEL COMPATIBLE (simplified)"""
    try:
        print("🖼️ Loading gallery page (Vercel Compatible)")

        # In Vercel, we can't store files persistently
        # This is a simplified version that shows recently generated QR codes from memory
        recent_qrs = []

        # Get recent QR codes from app config (limited approach)
        for key in app.config:
            if key.startswith('qr_data_'):
                qr_id = key.replace('qr_data_', '')
                recent_qrs.append({
                    'id': qr_id,
                    'created': 'Recently generated',
                    'size': f"{round(len(app.config[key]) / 1024, 1)} KB"
                })

        print(f"📊 Found {len(recent_qrs)} recent QR codes in memory")
        return render_template('gallery.html', qr_codes=recent_qrs)

    except Exception as e:
        print(f"❌ Gallery error: {str(e)}")
        return render_template('gallery.html', qr_codes=[], error=str(e))

@app.route('/test')
def test():
    """Test route to verify the app is working on Vercel"""
    print("🧪 Test endpoint accessed on Vercel")
    return jsonify({
        'status': 'working',
        'message': 'Shreeram\'s QR Generator is running on Vercel!',
        'timestamp': datetime.now().isoformat(),
        'platform': 'Vercel Serverless',
        'vercel_compatible': True,
        'python_version': os.sys.version,
        'environment': 'production' if not app.debug else 'development'
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Page not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error', 'details': str(error)}), 500

# Vercel entry point
if __name__ == '__main__':
    print("🚀 QR Generator Pro by Shreeram - VERCEL COMPATIBLE VERSION")
    print("📧 Copyright © 2024 Shreeram. All rights reserved.")
    print("☁️ Optimized for Vercel serverless deployment")
    print("🌐 Starting server...")
    app.run(debug=True)
else:
    # When deployed on Vercel
    print("☁️ Running on Vercel serverless environment")
