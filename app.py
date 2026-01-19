import streamlit as st
import qrcode
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
import io

# वेबसाइटची रचना (UI)
st.set_page_config(page_title="Ai Sab Kuch - Artistic QR", layout="centered")
st.title("🎨 Artistic QR Design Agent")
st.subheader("तुमच्या नावाचा स्टेंसिल QR कोड तयार करा")

# युजरकडून इनपुट घेणे
user_name = st.text_input("तुमचे नाव लिहा (उदा. प्रनंपु):", "प्रनंपु")
target_url = st.text_input("QR स्कॅन केल्यावर कोणती लिंक उघडली पाहिजे?", "https://aisabkuch.com")

if st.button("QR कोड जनरेट करा"):
    with st.spinner('तुमचा डिजिटल आर्ट कोड तयार होत आहे...'):
        # १. स्टेंसिल तयार करणे
        stencil = np.ones((500, 500), dtype=np.uint8) * 255
        pil_stencil = Image.fromarray(stencil)
        draw = ImageDraw.Draw(pil_stencil)
        
        # फॉन्ट निवड (तुमच्या सर्व्हरवर असलेला मराठी फॉन्ट पाथ वापरा)
        try:
            font = ImageFont.truetype("arial.ttf", 150)
        except:
            font = ImageFont.load_default()

        draw.text((50, 150), user_name, fill=0, font=font)
        stencil_np = np.array(pil_stencil)

        # २. QR कोड तयार करणे
        qr = qrcode.QRCode(version=5, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=2)
        qr.add_data(target_url)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white").convert('L')
        qr_img = qr_img.resize((500, 500), Image.NEAREST)
        qr_np = np.array(qr_img)

        # ३. स्टेंसिल आणि QR एकत्र करणे
        final_qr = np.ones((500, 500), dtype=np.uint8) * 255
        final_qr[stencil_np == 0] = qr_np[stencil_np == 0]

        # निकाल दाखवणे
        result_img = Image.fromarray(final_qr)
        st.image(result_img, caption=f"तुमचा '{user_name}' QR कोड", use_container_width=True)

        # डाउनलोड बटण
        buf = io.BytesIO()
        result_img.save(buf, format="PNG")
        st.download_button(label="QR डाउनलोड करा", data=buf.getvalue(), file_name="my_art_qr.png", mime="image/png")

st.info("प्रोफेसर टीप: हा कोड Marketing आणि Personal Branding साठी उत्तम आहे!")
