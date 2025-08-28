from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import io
import qrcode
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H

app = Flask(__name__)
CORS(app)

EC_MAP = {"L": ERROR_CORRECT_L, "M": ERROR_CORRECT_M, "Q": ERROR_CORRECT_Q, "H": ERROR_CORRECT_H}

@app.post("/qr")
def make_qr():
    """
    POST JSON:
    {
      "data": "string to encode",      // required
      "box": 10,                       // optional (default=10)
      "border": 4,                     // optional (default=4)
      "ec": "M",                       // optional (L|M|Q|H, default=M)
      "fill": "#000000",               // optional (default #000000)
      "bg": "#FFFFFF",                 // optional (default #FFFFFF)
      "filename": "qrcode.png"         // optional (default qrcode.png)
    }
    """
    payload = request.get_json(silent=True) or {}
    data = payload.get("data")
    if not data:
        return jsonify({"error": "JSON body must include 'data'"}), 400

    box = int(payload.get("box", 10))
    border = int(payload.get("border", 4))
    fill = payload.get("fill", "#000000")
    bg = payload.get("bg", "#FFFFFF")
    ec = (payload.get("ec") or "M").upper()
    filename = payload.get("filename", "qrcode.png")

    if ec not in EC_MAP:
        return jsonify({"error": "Invalid 'ec'. Use one of L, M, Q, H."}), 400

    qr = qrcode.QRCode(
        version=None,
        error_correction=EC_MAP[ec],
        box_size=box,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill, back_color=bg)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return send_file(
        buf,
        mimetype="image/png",
        as_attachment=False,
        download_name=filename,
        max_age=3600,
        etag=True,
        conditional=True,
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
