from fastapi import FastAPI, Query, HTTPException, Response
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import requests
from io import BytesIO

app = FastAPI()


API_KEY = "franko_ff"
API_KEY = "community"
API_KEY = "KiraDevX"
API_KEY = "3MKK"
API_KEY = "ByFranKo"
API_KEY = "AKAJI-TEAM"
API_KEY = "ANY-TEAM"
API_KEY = "FRANKOOO"
API_KEY = "Rou7"
API_KEY = "FrankoDevG"
API_KEY = "LbrenesDevX"
API_KEY = "Flgwldyy"
API_KEY = "TalyeniHere"
API_KEY = "PiRate-Modz"

def create_fire_glow(image, border=40):
    new_width = image.width + border * 2
    new_height = image.height + border * 2
    base = Image.new("RGBA", (new_width, new_height), (0, 0, 0, 0))
    base.paste(image, (border, border))

    glow = base.copy()
    glow = glow.convert("L").convert("RGBA")
    r, g, b, a = glow.split()
    r = r.point(lambda i: min(255, int(i * 3)))
    g = g.point(lambda i: min(255, int(i * 1.5)))
    b = b.point(lambda i: int(i * 0.1))
    glow_colored = Image.merge("RGBA", (r, g, b, a))

    glow_blurred = glow_colored.filter(ImageFilter.GaussianBlur(radius=30))
    result = Image.alpha_composite(glow_blurred, base)
    return result

@app.get("/outfit-image")
def get_outfit(uid: str = Query(...), region: str = Query(...), key: str = Query(None)):
    if key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")

    url = f"https://aditya-outfit-v9op.onrender.com/outfit-image?uid={uid}&region={region}"

    try:
        res = requests.get(url, timeout=20)
        if res.status_code != 200 or not res.headers.get("content-type", "").startswith("image"):
            raise HTTPException(status_code=400, detail="Image not found or invalid response")

        original = Image.open(BytesIO(res.content)).convert("RGBA")

        fire_img = create_fire_glow(original, border=40)

        text_layer = Image.new("RGBA", (4000, 4000), (0, 0, 0, 0))
        draw = ImageDraw.Draw(text_layer)

        text = "@M_DD_F"

        try:
            font = ImageFont.truetype("Roboto-Bold.ttf", 1000)
        except Exception as e:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x, y = 50, 50

        shadow_color = (0, 0, 0, 200)
        for offset in [(5, 5), (5, -5), (-5, 5), (-5, -5)]:
            draw.text((x + offset[0], y + offset[1]), text, font=font, fill=shadow_color)

        text_color = (255, 255, 255, 255)
        draw.text((x, y), text, font=font, fill=text_color)

        text_layer_resized = text_layer.resize(fire_img.size, Image.Resampling.LANCZOS)

        final_img = Image.alpha_composite(fire_img, text_layer_resized)

        output = BytesIO()
        final_img.save(output, format="PNG")
        output.seek(0)

        return Response(content=output.getvalue(), media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



