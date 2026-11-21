
import hashlib
import io
import math
import random
from functools import lru_cache

import streamlit as st
from PIL import Image, ImageDraw

st.set_page_config(page_title="Futomaki Studio", layout="wide")

BG = "#C6C6C6"
RED = "#ed2227"
SESAME = "Black + White Sesame Seeds"
SHISO = "Shiso Leaf"
SIZE = 1100
CENTER = SIZE // 2
ROLL_RADIUS = 448  # Previous radius was 112: now 4x as large.

PROTEINS = sorted([
    "Otoro Aburi", "Otoro", "Chutoro", "Akami", "Tempura Shrimp",
    "Miso Marinated Tofu", "Hamachi", "Hiramasa", "Shiromi", "Hotate",
    "Hotate Aburi", "Hamachi Aburi", "Ebi", "Ikura", "Uni", "Kani",
    "Salmon", "Salmon Aburi", "Tuna Salad", "Cooked Miso Salmon",
    "Cooked Bulgogi Brisket", "Cooked Gochujang Pork Belly",
    "Spicy Scallop Salad", "Grilled Chicken Breast"
], key=str.casefold)

FILLINGS = sorted([
    "Pickled Jalapeño Spears", "Avocado", "Ube Purple Yam", "Edamame",
    "Julienne Cucumber", "Yellow Daikon", "Mango Spears", "Asparagus",
    "Tamago", "Shiso Leaf", "Diced Green Onions", "Tempura Bits",
    "Julienned Carrot Spears", "Spinach", "Mayo", "Spicy Mayo", "Kimchi",
    "Cream Cheese", SESAME
], key=str.casefold)

# Colors are ingredient-specific rather than shared fish presets.
COLORS = {
    "Akami": "#bd2447", "Chutoro": "#e66b83", "Otoro": "#f0a3b3",
    "Otoro Aburi": "#d58b92", "Hamachi": "#eed4ab",
    "Hamachi Aburi": "#d6b48e", "Hiramasa": "#c9dccd",
    "Shiromi": "#f4eee7", "Hotate": "#f3e6d0",
    "Hotate Aburi": "#d9b68e", "Salmon": "#fa8868",
    "Salmon Aburi": "#e77b58", "Ebi": "#f6e6dc",
    "Kani": "#fff5e8", "Ikura": "#ed6e18", "Uni": "#eca538",
    "Tempura Shrimp": "#e5ae60", "Miso Marinated Tofu": "#e3cb9c",
    "Tuna Salad": "#d3a3a1", "Cooked Miso Salmon": "#c7845f",
    "Cooked Bulgogi Brisket": "#663b29",
    "Cooked Gochujang Pork Belly": "#ae301f",
    "Spicy Scallop Salad": "#e8ae93",
    "Grilled Chicken Breast": "#d3b48c",
    "Avocado": "#b0d779", "Edamame": "#81ba4d",
    "Julienne Cucumber": "#b0d885", "Pickled Jalapeño Spears": "#638d43",
    "Asparagus": "#709743", "Spinach": "#397044", SHISO: "#2c6840",
    "Diced Green Onions": "#6aa353", "Ube Purple Yam": "#9565b0",
    "Yellow Daikon": "#ead45e", "Mango Spears": "#f8b448",
    "Tamago": "#f1d166", "Julienned Carrot Spears": "#eb7c36",
    "Tempura Bits": "#cf9a52", "Kimchi": "#c44e2e",
    "Mayo": "#f7eedc", "Spicy Mayo": "#edaa87",
    "Cream Cheese": "#f9f6ee", SESAME: "#efe9dc"
}

if "ingredients" not in st.session_state:
    st.session_state.ingredients = {
        "Hamachi", "Avocado", "Julienne Cucumber", "Diced Green Onions"
    }
if "roll_style" not in st.session_state:
    st.session_state.roll_style = "Futomaki"


def rand_for(*parts):
    data = "|".join(map(str, parts)).encode("utf-8")
    return random.Random(int.from_bytes(hashlib.sha256(data).digest()[:8], "big"))


def oval(d, x, y, rx, ry, color, outline=None, width=1):
    bounds = (round(x-rx), round(y-ry), round(x+rx), round(y+ry))
    d.ellipse(bounds, fill=color, outline=outline, width=width)


def scatter(d, rng, s, palette, count, min_r, max_r, ellipse_ratio=1):
    for _ in range(count):
        x, y = rng.randrange(s), rng.randrange(s)
        r = rng.uniform(min_r, max_r) * s
        oval(d, x, y, r, r*ellipse_ratio*rng.uniform(.75, 1.2), rng.choice(palette))


def fibers(d, rng, s, palette, count=105, width=3, span=.25, slope=.05):
    for _ in range(count):
        x, y = rng.randrange(s), rng.randrange(s)
        dx = rng.uniform(.04, span)*s
        dy = rng.uniform(-slope, slope)*s
        d.line((x-dx,y-dy,x+dx,y+dy), fill=rng.choice(palette), width=width)


def scorch(d, rng, s, count=105):
    for _ in range(count):
        x,y=rng.randrange(s),rng.randrange(s)
        rx=rng.uniform(.009,.055)*s
        oval(d,x,y,rx,rx*.3,rng.choice(["#65351d80","#a464348c","#dca05d8c"]))


@lru_cache(maxsize=128)
def texture(name, s=512):
    """Distinct, illustrated food textures. These are not photographs."""
    rng = rand_for("ingredient",name,s)
    im = Image.new("RGB",(s,s),COLORS[name])
    d=ImageDraw.Draw(im,"RGBA")

    if name in {"Akami","Chutoro","Otoro","Otoro Aburi"}:
        if name == "Akami":
            fibers(d,rng,s,["#e54c6f80","#8e153a80","#f6a3a875"],150,3,.35,.035)
            scatter(d,rng,s,["#9e183044","#f0657950"],70,.006,.028)
        elif name == "Chutoro":
            fibers(d,rng,s,["#fff0d6a9","#f6b5bbaa","#b9375970"],170,5,.38,.05)
            scatter(d,rng,s,["#fff5e777","#cc415f65"],105,.004,.035)
        else:
            # Fat-rich pink belly tuna with broad irregular marbling.
            fibers(d,rng,s,["#fff5e6db","#fff9f3b8","#d86d8690"],220,8,.43,.10)
            scatter(d,rng,s,["#fff5e8aa","#ffe7dc9a"],85,.015,.07,.35)
            if name == "Otoro Aburi": scorch(d,rng,s,180)

    elif name in {"Salmon","Salmon Aburi","Cooked Miso Salmon"}:
        fibers(d,rng,s,["#fff0cebb","#ffd5ae9c","#e9685577"],185,7,.42,.045)
        scatter(d,rng,s,["#ffb58480","#da644966"],60,.008,.038)
        if name != "Salmon": scorch(d,rng,s,175)

    elif name in {"Hamachi","Hamachi Aburi"}:
        # Warm ivory/gold hamachi, translucent pale striping.
        fibers(d,rng,s,["#fff6ddaa","#d9ae7b91","#fffef2a0"],140,5,.30,.05)
        scatter(d,rng,s,["#efd9b07d","#c9af8660"],90,.012,.05)
        if name.endswith("Aburi"): scorch(d,rng,s,160)

    elif name == "Hiramasa":
        # Silvery, pale green kingfish with subtle cool, long grain.
        fibers(d,rng,s,["#edf4e8d4","#8eacac80","#fffef2a6"],195,3,.46,.025)
        scatter(d,rng,s,["#b2c8c788","#f4f7e8bb"],85,.012,.045)

    elif name == "Shiromi":
        # Near-white transparent flesh with fine rose-grey lines.
        fibers(d,rng,s,["#d7c4c3ad","#ffffffcd","#d8d6d0b0"],170,2,.38,.06)
        scatter(d,rng,s,["#ffffffb5","#ebdeda80"],80,.006,.035)

    elif name in {"Hotate","Hotate Aburi"}:
        # Scallop: creamy rounded lobes and radial fine fibers.
        scatter(d,rng,s,["#fff8e8","#dfcbb3","#f1e4d0"],160,.03,.11,.7)
        fibers(d,rng,s,["#ffffffaa","#c9b49e73"],170,2,.08,.32)
        if name.endswith("Aburi"): scorch(d,rng,s,210)

    elif name == "Ebi":
        # Shrimp: pale ivory flesh with bright coral orange curved bands.
        scatter(d,rng,s,["#fff8ed","#f3ddd0"],190,.025,.08)
        for j in range(27):
            yy=(j+.35)*s/27
            d.arc((-s*.15,yy-s*.22,s*1.15,yy+s*.22),10,170,fill="#ec8467d9",width=max(5,s//36))
        fibers(d,rng,s,["#ffffffa6","#f4a48e7c"],115,3,.14,.06)

    elif name == "Kani":
        # White crab with recognizable salmon-coral surimi stripes.
        scatter(d,rng,s,["#ffffff","#fff5ea","#ecdfd2"],180,.01,.05)
        for j in range(0,s,59):
            d.line((-15,j+24,s+15,j-20),fill="#ed8067e0",width=17)
            d.line((-15,j+41,s+15,j-3),fill="#ffc5a6be",width=6)

    elif name == "Miso Marinated Tofu":
        scatter(d,rng,s,["#f2e3c5","#b89b6e","#f8edd6"],155,.017,.05)
        # Clearly visible dark grill marks, diagonal across tofu.
        for x in range(-s,s*2,95):
            d.line((x,-20,x-s*.53,s+20),fill="#6d4326d4",width=16)
            d.line((x+17,-20,x+17-s*.53,s+20),fill="#b27c4188",width=7)

    elif name == "Cooked Bulgogi Brisket":
        fibers(d,rng,s,["#3e2117d0","#ad7551bb","#e0a16970"],205,8,.29,.12)
        scatter(d,rng,s,["#4a2719aa","#96582f99"],165,.01,.05)

    elif name == "Cooked Gochujang Pork Belly":
        scatter(d,rng,s,["#7a1b13a6","#e3522d8e","#c43c228e"],245,.013,.074)
        fibers(d,rng,s,["#f0a07a99","#75190da6"],145,5,.32,.08)
        scorch(d,rng,s,100)

    elif name == "Grilled Chicken Breast":
        fibers(d,rng,s,["#f3e3beaa","#a7895b78","#fdf5dcaa"],190,4,.28,.055)
        for j in range(-s,s*2,115):
            d.line((j,0,j-s*.38,s),fill="#81573397",width=10)

    elif name == "Tempura Shrimp":
        scatter(d,rng,s,["#f9e3a3","#c78a44","#f5c76e","#ffeac5"],410,.009,.067)
        scatter(d,rng,s,["#f1a188","#fff3df"],90,.02,.08)

    elif name == "Ikura":
        scatter(d,rng,s,["#bb3c12","#ef7719","#fa952b"],400,.025,.065)
        scatter(d,rng,s,["#ffdc7b","#ffbd55"],230,.003,.013)

    elif name == "Uni":
        scatter(d,rng,s,["#edac40","#ffd878","#c98628","#f6be59"],330,.013,.068)

    elif name in {"Tuna Salad","Spicy Scallop Salad"}:
        p=["#c18b89","#e8bdb6","#f4e7d5"] if name=="Tuna Salad" else ["#df9a7b","#efc3aa","#f7e4c8"]
        scatter(d,rng,s,p,340,.012,.074)
        scatter(d,rng,s,["#fff7dd","#fbedd9"],170,.009,.035)

    elif name == "Diced Green Onions":
        scatter(d,rng,s,["#549849","#acd279","#e5edb6"],160,.014,.06)
        for _ in range(190):
            x,y=rng.randrange(s),rng.randrange(s)
            r=rng.uniform(.032,.066)*s  # Large scallion rings.
            oval(d,x,y,r,r,"#286d38")
            oval(d,x,y,r*.73,r*.73,"#d6e8a4")
            oval(d,x,y,r*.40,r*.40,"#7fb85b")

    elif name in {"Avocado","Edamame"}:
        scatter(d,rng,s,["#7fae49","#cce68d","#a3ce71","#edf4b9"],340,.015,.068)

    elif name in {"Julienne Cucumber","Asparagus","Pickled Jalapeño Spears"}:
        scatter(d,rng,s,["#387e42","#8dbe5c","#dce7a1","#b1d785"],270,.01,.075)
        scatter(d,rng,s,["#e9efcc","#ffffffab"],150,.004,.02)

    elif name in {"Spinach",SHISO}:
        scatter(d,rng,s,["#1d5938","#43874b","#82af60"],340,.012,.088)
        fibers(d,rng,s,["#b1d48ca8","#2b634d99"],165,2,.14,.17)

    elif name == "Kimchi":
        scatter(d,rng,s,["#92291e","#ec7b38","#f2bf72","#789445"],370,.012,.073)

    elif name in {"Mayo","Spicy Mayo","Cream Cheese"}:
        p=["#f2c0a1","#d77b5b","#ffe2c5"] if name=="Spicy Mayo" else ["#ffffff","#eae0c9","#fff5e3"]
        scatter(d,rng,s,p,230,.015,.07)

    elif name in {"Ube Purple Yam","Mango Spears","Julienned Carrot Spears","Yellow Daikon","Tamago"}:
        p=(["#7d5196","#be94cb","#e6cdee"] if name=="Ube Purple Yam"
           else ["#ea9c2d","#ffc963","#f9b046"] if name=="Mango Spears"
           else ["#d96928","#f39a3e","#ffc16d"] if name=="Julienned Carrot Spears"
           else ["#d7c04b","#fff3b0","#f0d76d"])
        scatter(d,rng,s,p,275,.015,.08)

    elif name == "Tempura Bits":
        scatter(d,rng,s,["#a97535","#e7ba73","#fff0c1","#c58d46"],450,.006,.056)

    elif name == SESAME:
        for _ in range(1500):
            x,y=rng.randrange(s),rng.randrange(s)
            oval(d,x,y,3,2,rng.choice(["#262924","#fff9e5","#d4c9b6"]))

    return im


@lru_cache(maxsize=128)
def thumbnail(name):
    s=84
    mask=Image.new("L",(s,s),0)
    ImageDraw.Draw(mask).ellipse((2,2,s-3,s-3),fill=255)
    result=Image.new("RGBA",(s,s),(0,0,0,0))
    tile=texture(name,512).resize((s,s),Image.Resampling.LANCZOS)
    result.paste(tile,(0,0),mask)
    ImageDraw.Draw(result).ellipse((2,2,s-3,s-3),outline=RED,width=2)
    return result


def draw_rice(image,cx,cy,r,seed):
    rng=rand_for("rice",seed)
    d=ImageDraw.Draw(image,"RGBA")
    oval(d,cx,cy,r,r,"#f3f1e8")
    for _ in range(3400):
        a=rng.random()*math.tau
        rr=r*math.sqrt(rng.random())
        x,y=cx+rr*math.cos(a),cy+rr*math.sin(a)
        oval(d,x,y,rng.uniform(2,7),rng.uniform(1,3.5),rng.choice([
            "#fffefaad","#dedbd0b0","#ffffffc9","#d5d0c28a"
        ]))


def leaf_ring(image,cx,cy,r):
    d=ImageDraw.Draw(image,"RGBA")
    oval(d,cx,cy,r,r,None,"#326a3a",width=24)
    oval(d,cx,cy,r-7,r-7,None,"#83b364",width=7)
    for j in range(120):
        a=j*math.tau/120
        d.line((cx+r*math.cos(a),cy+r*math.sin(a),
                cx+(r-23)*math.cos(a+.085),cy+(r-23)*math.sin(a+.085)),
               fill="#badb8ca6",width=2)


def fill_core(image,cx,cy,r,names):
    if not names:
        oval(ImageDraw.Draw(image),cx,cy,r,r,"#e9e4d4")
        return
    n=len(names)
    # Entire interior is divided into equal angular sections, no empty gaps.
    for i,name in enumerate(names):
        a=-90+360*i/n
        b=-90+360*(i+1)/n
        mask=Image.new("L",image.size,0)
        md=ImageDraw.Draw(mask)
        bounds=(cx-r,cy-r,cx+r,cy+r)
        if n==1:
            md.ellipse(bounds,fill=255)
        else:
            md.pieslice(bounds,a,b,fill=255)
        # Use a large seamless repeated texture for each sector.
        tex=texture(name,512)
        tile=tex.resize((r*2+2,r*2+2),Image.Resampling.BICUBIC)
        patch=Image.new("RGB",image.size)
        patch.paste(tile,(cx-r-1,cy-r-1))
        image.paste(patch,(0,0),mask)
    if n>1:
        d=ImageDraw.Draw(image,"RGBA")
        for i in range(n):
            a=math.radians(-90+360*i/n)
            d.line((cx,cy,cx+r*math.cos(a),cy+r*math.sin(a)),fill="#564c3544",width=2)


def sesame_coating(image,cx,cy,r,inner):
    d=ImageDraw.Draw(image)
    rng=rand_for("outer-sesame")
    for _ in range(1650):
        angle=rng.random()*math.tau
        radius=math.sqrt(rng.uniform(inner**2,r**2))
        x=cx+radius*math.cos(angle)
        y=cy+radius*math.sin(angle)
        oval(d,x,y,rng.uniform(1.5,4),rng.uniform(1,2.5),
             rng.choice(["#1d211d","#fdfaf0","#d2c7ae"]))


def render_roll():
    image=Image.new("RGB",(SIZE,SIZE),BG)
    cx=cy=CENTER
    R=ROLL_RADIUS
    items=st.session_state.ingredients
    names=([n for n in PROTEINS if n in items]
           +[n for n in FILLINGS if n in items and n not in (SHISO,SESAME)])
    d=ImageDraw.Draw(image,"RGBA")
    oval(d,cx+5,cy+10,R+4,R+4,"#59605745")
    if st.session_state.roll_style=="Futomaki":
        oval(d,cx,cy,R,R,"#1b2920")
        oval(d,cx,cy,R-6,R-6,None,"#617557",width=4)
        draw_rice(image,cx,cy,R-15,"futomaki")
        core_r=round(R*.75)  # Rice is approx. 25% of the radius.
    else:
        draw_rice(image,cx,cy,R,"uramaki")
        if SESAME in items:
            sesame_coating(image,cx,cy,R-6,round(R*.81))
        core_r=round(R*.75)
        d=ImageDraw.Draw(image,"RGBA")
        oval(d,cx,cy,core_r+10,core_r+10,"#1b2920")
        oval(d,cx,cy,core_r+7,core_r+7,None,"#607a58",width=4)
        core_r-=3
    if SHISO in items:
        leaf_ring(image,cx,cy,core_r)
        core_r-=24
    fill_core(image,cx,cy,core_r,names)
    return image


def toggle(name):
    chosen=st.session_state.ingredients
    if name in chosen:
        chosen.remove(name)
    else:
        chosen.add(name)
        if name==SESAME:
            st.session_state.roll_style="Uramaki"


def change_style(kind):
    st.session_state.roll_style=kind
    if kind=="Futomaki":
        st.session_state.ingredients.discard(SESAME)


def reset_roll():
    st.session_state.ingredients=set()
    st.session_state.roll_style="Futomaki"


st.markdown("""
<style>
.stApp {background:#C6C6C6; color:#29352e;}
h1,h2,h3 {color:#29352e;}
/* White controls with red strokes, including the two roll-style bars. */
div.stButton > button, div.stDownloadButton > button {
  background:#ffffff !important;
  border:2px solid #ed2227 !important;
  color:#ed2227 !important;
  border-radius:8px !important;
  height:auto !important;
  min-height:43px !important;
  width:100% !important;
  white-space:normal !important;
  word-break:normal !important;
  overflow-wrap:anywhere !important;
  text-align:left !important;
  line-height:1.35 !important;
  padding:9px 10px !important;
  font-weight:650 !important;
  font-size:13px !important;
}
div.stButton > button:hover, div.stDownloadButton > button:hover {
  background:#fff1f1 !important;
}
div.stButton > button p, div.stDownloadButton > button p,
div.stButton > button span, div.stDownloadButton > button span {
  white-space:normal !important;
  overflow:visible !important;
  text-overflow:clip !important;
  word-break:normal !important;
}
/* The download button typography remains #ed2227. */
[data-testid="stDownloadButton"] button {color:#ed2227 !important;}
.selected-style {color:#ed2227;font-weight:750;font-size:16px;padding:12px 0;}
.selected-style strong {color:#ed2227;}
[data-testid="stImage"] img {border-radius:10px;}
</style>
""",unsafe_allow_html=True)

st.title("Futomaki Studio")
st.caption("Single-roll development preview · top-down cross section · #C6C6C6")

left,right=st.columns([1.25,1.65],gap="large")
with left:
    protein_col,filling_col=st.columns(2,gap="medium")
    for col,label,items in [
        (protein_col,"PROTEINS",PROTEINS),
        (filling_col,"FILLINGS",FILLINGS)
    ]:
        with col:
            st.subheader(label)
            for name in items:
                # Visual preview next to the full, wrapping ingredient name.
                icon_col,button_col=st.columns([1,4],gap="small",vertical_alignment="center")
                with icon_col:
                    st.image(thumbnail(name),use_container_width=True)
                with button_col:
                    chosen=name in st.session_state.ingredients
                    label_text=("✓ " if chosen else "+ ")+name
                    st.button(label_text,key="ingredient_"+name,
                              on_click=toggle,args=(name,))

with right:
    st.subheader("Build your roll")
    c1,c2,c3=st.columns([1,1,.8])
    with c1:
        st.button("Futomaki",on_click=change_style,args=("Futomaki",))
    with c2:
        st.button("Uramaki",on_click=change_style,args=("Uramaki",))
    with c3:
        st.button("Clear roll",on_click=reset_roll)

    current=st.session_state.roll_style
    description=("Nori outside · rice inside" if current=="Futomaki"
                 else "Rice outside · nori inside")
    st.markdown(
        '<div class="selected-style">Selected style: '
        +current+' — '+description+'</div>',
        unsafe_allow_html=True
    )
    roll_image=render_roll()
    st.image(roll_image,use_container_width=True)
    out=io.BytesIO()
    roll_image.save(out,format="PNG")
    st.download_button("Download roll mockup (PNG)",data=out.getvalue(),
                       file_name="futomaki-studio-one-roll.png",mime="image/png")

    pp=[n for n in PROTEINS if n in st.session_state.ingredients]
    ff=[n for n in FILLINGS if n in st.session_state.ingredients]
    st.markdown("**Selected ingredients**")
    st.write("**Proteins:** "+(", ".join(pp) if pp else "None"))
    st.write("**Fillings:** "+(", ".join(ff) if ff else "None"))
    st.caption("Illustrated food textures, not actual photographs. Ingredient regions expand "
               "to occupy the full interior. Shiso wraps the filling area; sesame stays "
               "on the exterior rice and automatically selects Uramaki.")
