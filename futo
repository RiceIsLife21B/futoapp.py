
import io
import math
import random
import hashlib
from functools import lru_cache

import streamlit as st
from PIL import Image, ImageDraw, ImageFilter

st.set_page_config(page_title="Futomaki Studio", layout="wide")

BACKGROUND = "#C6C6C6"
SESAME = "Black + White Sesame Seeds"
SHISO = "Shiso Leaf"

PROTEINS = sorted([
    "Otoro Aburi", "Otoro", "Chutoro", "Akami", "Tempura Shrimp",
    "Miso Marinated Tofu", "Hamachi", "Hiramasa", "Shiromi", "Hotate",
    "Hotate Aburi", "Hamachi Aburi", "Ebi", "Ikura", "Uni", "Kani",
    "Salmon", "Salmon Aburi", "Tuna Salad", "Cooked Miso Salmon",
    "Cooked Bulgogi Brisket", "Cooked Gochujang Pork Belly",
    "Spicy Scallop Salad", "Grilled Chicken Breast",
], key=str.casefold)

FILLINGS = sorted([
    "Pickled Jalapeño Spears", "Avocado", "Ube Purple Yam", "Edamame",
    "Julienne Cucumber", "Yellow Daikon", "Mango Spears", "Asparagus",
    "Tamago", "Shiso Leaf", "Diced Green Onions", "Tempura Bits",
    "Julienned Carrot Spears", "Spinach", "Mayo", "Spicy Mayo", "Kimchi",
    "Cream Cheese", "Black + White Sesame Seeds",
], key=str.casefold)

COLORS = {
    "Otoro Aburi": "#dca89c", "Otoro": "#edaca5", "Chutoro": "#d57578",
    "Akami": "#af384c", "Tempura Shrimp": "#dba663",
    "Miso Marinated Tofu": "#dec9a0", "Hamachi": "#e8d8bd",
    "Hamachi Aburi": "#d9bc91", "Hiramasa": "#dce2d6",
    "Shiromi": "#f0e6df", "Hotate": "#ede1cd",
    "Hotate Aburi": "#d6b58b", "Ebi": "#eaa090",
    "Ikura": "#f28028", "Uni": "#eeb04c", "Kani": "#e9e4dc",
    "Salmon": "#ee987d", "Salmon Aburi": "#d98565",
    "Tuna Salad": "#d0a89c", "Cooked Miso Salmon": "#c88f6a",
    "Cooked Bulgogi Brisket": "#835445",
    "Cooked Gochujang Pork Belly": "#af594b",
    "Spicy Scallop Salad": "#ecc1a2",
    "Grilled Chicken Breast": "#dcc4a0",
    "Pickled Jalapeño Spears": "#67923a", "Avocado": "#a8d166",
    "Ube Purple Yam": "#9265ab", "Edamame": "#80b951",
    "Julienne Cucumber": "#a1d177", "Yellow Daikon": "#e7d357",
    "Mango Spears": "#f6b244", "Asparagus": "#719949",
    "Tamago": "#edca5a", "Shiso Leaf": "#386d42",
    "Diced Green Onions": "#5d9b56", "Tempura Bits": "#d6aa6c",
    "Julienned Carrot Spears": "#e78038", "Spinach": "#437343",
    "Mayo": "#f6e8c9", "Spicy Mayo": "#e9a17b",
    "Kimchi": "#bc5537", "Cream Cheese": "#f4eee1",
    SESAME: "#ebebdc",
}

# Starting sample: Hamachi, avocado, cucumber, green onions.
if "ingredients" not in st.session_state:
    st.session_state.ingredients = {
        "Hamachi", "Avocado", "Julienne Cucumber", "Diced Green Onions"
    }
if "roll_style" not in st.session_state:
    st.session_state.roll_style = "Futomaki"


def rng_for(*parts):
    digest = hashlib.sha256("|".join(map(str, parts)).encode()).digest()
    return random.Random(int.from_bytes(digest[:8], "big"))


def ellipse(draw, x, y, rx, ry, color, width=0):
    box = (round(x-rx), round(y-ry), round(x+rx), round(y+ry))
    if width:
        draw.ellipse(box, outline=color, width=width)
    else:
        draw.ellipse(box, fill=color)


def spots(draw, rng, size, palette, count=100, small=.015, large=.09):
    for _ in range(count):
        x, y = rng.randrange(size), rng.randrange(size)
        radius = rng.uniform(small, large) * size
        ellipse(draw, x, y, radius, radius*rng.uniform(.55, 1.35), rng.choice(palette))


@lru_cache(maxsize=128)
def ingredient_texture(name, size=340):
    """Generated cross-sectional food-like textures. No external image assets."""
    rng = rng_for(name, size)
    image = Image.new("RGB", (size, size), COLORS[name])
    d = ImageDraw.Draw(image, "RGBA")

    if name == "Diced Green Onions":
        # Deliberately large onion tubes: roughly 3× their original diameter.
        spots(d, rng, size, ["#b3d789", "#5c9c53", "#2c753f"], 90, .016, .055)
        for _ in range(115):
            x, y = rng.randrange(size), rng.randrange(size)
            r = rng.uniform(.027, .057) * size
            ellipse(d, x, y, r, r, "#327c42")
            ellipse(d, x, y, r*.74, r*.74, "#e0eabb")
            ellipse(d, x, y, r*.43, r*.43, "#90c574")
    elif name in {"Avocado", "Edamame"}:
        spots(d, rng, size, ["#c7e791", "#80b15a", "#e1edb8", "#6e9e47"], 270, .012, .065)
    elif name in {"Julienne Cucumber", "Asparagus", "Pickled Jalapeño Spears"}:
        spots(d, rng, size, ["#4b8b46", "#a8d67e", "#e5f0b8", "#76b065"], 220, .012, .07)
        spots(d, rng, size, ["#f5f2d5", "#e7efbf"], 130, .004, .014)
    elif name in {"Spinach", SHISO}:
        spots(d, rng, size, ["#215b36", "#5e914c", "#86af5c"], 260, .008, .09)
        for _ in range(125):
            x, y = rng.randrange(size), rng.randrange(size)
            d.line((x,y,x+rng.randrange(-25,26),y+rng.randrange(-25,26)), fill="#bbd796", width=2)
    elif name == "Ikura":
        spots(d, rng, size, ["#f48a26", "#c95924", "#ee6f1d"], 410, .025, .055)
        spots(d, rng, size, ["#ffd37f", "#ffbb5f"], 210, .005, .012)
    elif name in {"Tempura Shrimp", "Tempura Bits"}:
        spots(d, rng, size, ["#f4d79d", "#bd8239", "#f9eac9", "#dba95f"], 450, .006, .052)
        if name == "Tempura Shrimp":
            spots(d, rng, size, ["#eea292", "#fff3db"], 110, .02, .07)
    elif name in {"Mayo", "Spicy Mayo", "Cream Cheese"}:
        palette = ["#f8cfb3", "#da8468", "#f6e4ca"] if name == "Spicy Mayo" else ["#fffbed", "#ece3ca", "#faf3e5"]
        spots(d, rng, size, palette, 220, .007, .055)
    elif name in {"Mango Spears", "Tamago", "Yellow Daikon", "Julienned Carrot Spears", "Ube Purple Yam", "Miso Marinated Tofu"}:
        palette = (["#8d5ba7", "#c4a1d0", "#74428c"] if name == "Ube Purple Yam"
            else ["#e97c35", "#ffb563", "#db6427"] if name == "Julienned Carrot Spears"
            else ["#e5a12c", "#ffd477", "#f3b23b"] if name == "Mango Spears"
            else ["#edd38a", "#fff2ae", "#c9a956"])
        spots(d, rng, size, palette, 250, .015, .08)
    elif name == "Kimchi":
        spots(d, rng, size, ["#a73a2b", "#dc793c", "#efb16b", "#7b9c59"], 310, .009, .073)
    elif name in {"Ebi", "Kani"}:
        spots(d, rng, size, ["#f7ede0", "#e88b81", "#fff8ed", "#d96c65"], 215, .01, .08)
    elif name in {"Tuna Salad", "Spicy Scallop Salad"}:
        spots(d, rng, size, ["#fff0d7", "#bd8f7e", "#eac4a9", "#e4a17e"], 325, .013, .058)
    elif name == "Uni":
        spots(d, rng, size, ["#ffdc83", "#e9a13d", "#c88126", "#f6c05a"], 340, .01, .06)
    else:
        # Sashimi fibers, marbling, or cooked/seared surface variations.
        palette = ["#fff5e7", "#eecfb8", "#c78577", COLORS[name]]
        spots(d, rng, size, palette, 260, .007, .044)
        for _ in range(150):
            x, y = rng.randrange(size), rng.randrange(size)
            dx = rng.randrange(12,90)
            d.arc((x-dx,y-8,x+dx,y+8), 180, 350, fill=(255,246,234,rng.randint(45,140)), width=rng.choice([1,2,3]))
        if "Aburi" in name or "Cooked" in name or "Grilled" in name:
            spots(d, rng, size, ["#8c5338", "#b6784c", "#e2b889"], 220, .003, .026)
    return image


@lru_cache(maxsize=128)
def thumbnail(name):
    tex = ingredient_texture(name, 120)
    icon = Image.new("RGBA", (64,64), (255,255,255,0))
    mask = Image.new("L", (64,64), 0)
    m = ImageDraw.Draw(mask)
    m.ellipse((2,2,62,62), fill=255)
    if name == SESAME:
        tex = Image.new("RGB", (64,64), "#f7f1de")
        td = ImageDraw.Draw(tex)
        rng = rng_for("seed-icon")
        for _ in range(115):
            x,y = rng.randrange(64),rng.randrange(64)
            ellipse(td,x,y,1.6,.9,rng.choice(["#1a211c", "#fffdfa", "#dfd2a8"]))
    else:
        tex = tex.resize((64,64),Image.Resampling.LANCZOS)
    icon.paste(tex,(0,0),mask)
    ImageDraw.Draw(icon).ellipse((2,2,62,62),outline="#667464",width=2)
    return icon


def draw_circle(draw, x, y, r, fill, width=0):
    ellipse(draw,x,y,r,r,fill,width)


def rice(image, cx, cy, radius, seed):
    rng=rng_for("rice",seed)
    d=ImageDraw.Draw(image,"RGBA")
    draw_circle(d,cx,cy,radius,"#f4f2e9")
    for _ in range(1250):
        a=rng.random()*math.tau
        rr=radius*math.sqrt(rng.random())
        x,y=cx+rr*math.cos(a),cy+rr*math.sin(a)
        ellipse(d,x,y,rng.uniform(1.3,4),rng.uniform(.7,2.2),rng.choice([
            "#ffffffb8", "#e1dfd5a8", "#f5f5eda6", "#cbcbbf66"
        ]))


def seed_coating(image,cx,cy,outer_r,inner_r,piece):
    d=ImageDraw.Draw(image)
    rng=rng_for("sesame",piece)
    for _ in range(360):
        a=rng.random()*math.tau
        r=math.sqrt(rng.uniform(inner_r**2,outer_r**2))
        x,y=cx+math.cos(a)*r,cy+math.sin(a)*r
        ellipse(d,x,y,rng.uniform(1,2.2),rng.uniform(.7,1.15),rng.choice(["#252621", "#fcf9e9", "#d6cdb7"]))


def draw_shiso_ring(image,cx,cy,outer_r):
    d=ImageDraw.Draw(image,"RGBA")
    draw_circle(d,cx,cy,outer_r,"#2e7040",11)
    draw_circle(d,cx,cy,outer_r-5,"#8ab063",2)
    for index in range(90):
        a=index*math.tau/90
        x1,y1=cx+outer_r*math.cos(a),cy+outer_r*math.sin(a)
        x2,y2=cx+(outer_r-10)*math.cos(a+.07),cy+(outer_r-10)*math.sin(a+.07)
        d.line((x1,y1,x2,y2),fill="#b8d58b",width=1)


def draw_filled_interior(image,cx,cy,radius,names,piece):
    """Every selected item occupies a full sector of the interior disk."""
    if not names:
        ImageDraw.Draw(image).ellipse((cx-radius,cy-radius,cx+radius,cy+radius),fill="#ede9d7")
        return
    n=len(names)
    turn=(piece%4)*1.5
    for i,name in enumerate(names):
        start=-90+360*i/n+turn
        end=-90+360*(i+1)/n+turn
        mask=Image.new("L",image.size,0)
        md=ImageDraw.Draw(mask)
        box=(cx-radius,cy-radius,cx+radius,cy+radius)
        # Pillow pie coordinates rotate clockwise from 3 o'clock.
        md.pieslice(box,start,end,fill=255)
        # Render the texture with a different offset per piece and ingredient.
        tile=ingredient_texture(name,340)
        offset_rng=rng_for(name,piece)
        dx=offset_rng.randrange(10,80)
        dy=offset_rng.randrange(10,80)
        patch=tile.crop((dx,dy,dx+224,dy+224)).resize((radius*2+2,radius*2+2),Image.Resampling.BICUBIC)
        layer=Image.new("RGB",image.size)
        layer.paste(patch,(cx-radius-1,cy-radius-1))
        image.paste(layer,(0,0),mask)
    d=ImageDraw.Draw(image,"RGBA")
    if n>1:
        for i in range(n):
            a=math.radians(-90+360*i/n+turn)
            d.line((cx,cy,cx+radius*math.cos(a),cy+radius*math.sin(a)),fill="#473c3333",width=2)


def draw_roll(image,cx,cy,radius,piece,style,names,shiso_on,sesame_on):
    d=ImageDraw.Draw(image,"RGBA")
    # Small drop shadow.
    ellipse(d,cx+3,cy+7,radius+4,radius+4,"#4a4e4540")
    if style=="Futomaki":
        draw_circle(d,cx,cy,radius,"#19271f")
        draw_circle(d,cx,cy,radius-4,"#405744",2)
        rice(image,cx,cy,radius-9,piece)
        # Rice band is 25% of total radius: core radius ~0.75 R.
        core_r=round(radius*.75)
        if shiso_on:
            draw_shiso_ring(image,cx,cy,core_r)
            core_r-=10
        draw_filled_interior(image,cx,cy,core_r,names,piece)
    else:
        rice(image,cx,cy,radius,piece)
        if sesame_on:
            seed_coating(image,cx,cy,radius-2,radius*.79,piece)
        # Nori separates inner ingredients and external rice.
        nori_r=round(radius*.75)
        draw_circle(d,cx,cy,nori_r+4,"#1d2b21")
        draw_circle(d,cx,cy,nori_r+3,"#547052",2)
        core_r=nori_r-5
        if shiso_on:
            draw_shiso_ring(image,cx,cy,core_r)
            core_r-=10
        draw_filled_interior(image,cx,cy,core_r,names,piece)


def render():
    image=Image.new("RGB",(1200,660),BACKGROUND)
    selection=st.session_state.ingredients
    interior=( [name for name in PROTEINS if name in selection]
             + [name for name in FILLINGS if name in selection and name not in (SESAME,SHISO)] )
    for row in range(2):
        for col in range(4):
            draw_roll(image,160+col*292,171+row*316,112,
                      row*4+col,st.session_state.roll_style,interior,
                      SHISO in selection,SESAME in selection)
    return image


def toggle_ingredient(name):
    items=st.session_state.ingredients
    if name in items:
        items.remove(name)
    else:
        items.add(name)
        if name==SESAME:
            st.session_state.roll_style="Uramaki"


def choose_style(style):
    st.session_state.roll_style=style
    if style=="Futomaki":
        st.session_state.ingredients.discard(SESAME)


st.markdown("""
<style>
.stApp { background:#C6C6C6; color:#27362c; }
h1,h2,h3 { color:#244b37; }
div.stButton > button { width:100%; text-align:left; min-height:38px;
    background:#f7f8f5; color:#263f2e; border:1px solid #b9c3b9;
    border-radius:8px; white-space:normal; font-size:.82rem; }
div.stButton > button:hover { border-color:#52795b; color:#1e5034; }
[data-testid="stImage"] img { border-radius:8px; }
</style>
""",unsafe_allow_html=True)

st.title("Futomaki Studio")
st.caption("Interactive sushi roll development · 8 pieces · top view · #C6C6C6")

left,right=st.columns([1.1,1.65],gap="large")
with left:
    protein_col,filling_col=st.columns(2,gap="small")
    for col,label,items in [(protein_col,"PROTEINS",PROTEINS),(filling_col,"FILLINGS",FILLINGS)]:
        with col:
            st.subheader(label)
            for name in items:
                icon_col,button_col=st.columns([1,4],gap="small",vertical_alignment="center")
                with icon_col:
                    st.image(thumbnail(name),width=38)
                with button_col:
                    mark="✓ " if name in st.session_state.ingredients else "+ "
                    st.button(mark+name,key="item_"+name,on_click=toggle_ingredient,args=(name,))

with right:
    st.subheader("Build your roll")
    a,b,c=st.columns([1,1,1])
    with a:
        st.button("Futomaki",on_click=choose_style,args=("Futomaki",))
    with b:
        st.button("Uramaki",on_click=choose_style,args=("Uramaki",))
    with c:
        if st.button("Clear roll"):
            st.session_state.ingredients.clear()
            st.session_state.roll_style="Futomaki"
            st.rerun()

    st.info("Selected style: **"+st.session_state.roll_style+"** · "+(
        "Nori outside / rice inside" if st.session_state.roll_style=="Futomaki"
        else "Rice outside / nori around fillings"))

    preview=render()
    st.image(preview,caption="Eight cross-sectional sushi pieces in two rows of four",use_container_width=True)
    buf=io.BytesIO()
    preview.save(buf,format="PNG")
    st.download_button("Download roll mockup (PNG)",data=buf.getvalue(),
                       file_name="futomaki-studio-roll.png",mime="image/png")

    chosen_proteins=[x for x in PROTEINS if x in st.session_state.ingredients]
    chosen_fillings=[x for x in FILLINGS if x in st.session_state.ingredients]
    st.markdown("**Selected ingredients**")
    st.write("**Proteins:** "+(", ".join(chosen_proteins) if chosen_proteins else "None"))
    st.write("**Fillings:** "+(", ".join(chosen_fillings) if chosen_fillings else "None"))
    st.caption("Images are procedurally illustrated, not photographs. Ingredients fill the central disk; shiso stays in a continuous ring. Sesame appears on the outside of Uramaki.")
