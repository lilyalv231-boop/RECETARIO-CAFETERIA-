import base64
import os
import pandas as pd
import streamlit as st

# Configuración de página
st.set_page_config(
    page_title="Recetario Digital - Il Mercato Gentiloni",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# 🖼️ LECTURA DE LOGO OFICIAL
# -----------------------------------------------------------------------------
LOGO_FILENAME = "Logo Mercato_negro-03 (2).png"

# Función para convertir la imagen local a Base64 para el HTML del banner
def get_image_base64(file_path):
  if os.path.exists(file_path):
    with open(file_path, "rb") as f:
      data = f.read()
    return f"data:image/png;base64,{base64.b64encode(data).decode()}"
  return ""


logo_base64 = get_image_base64(LOGO_FILENAME)

# Render de Logo oficial en la esquina superior del menú lateral
try:
  st.logo(LOGO_FILENAME, size="large")
except Exception:
  pass

# -----------------------------------------------------------------------------
# 🎨 PALETA DE COLORES ELEGANTE: AZUL MARINO Y BLANCO
# -----------------------------------------------------------------------------
st.markdown(
    """
<style>
    /* Fondo general */
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* Portada / Hero Banner en Azul Marino */
    .cover-banner {
        background: linear-gradient(135deg, #0A192F 0%, #1E3A8A 60%, #1E40AF 100%);
        border-radius: 18px;
        padding: 35px 30px;
        color: #FFFFFF;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px rgba(10, 25, 47, 0.2);
        border: 1px solid #1E293B;
    }
    
    .logo-container {
        display: inline-block;
        background-color: #FFFFFF;
        padding: 10px 20px;
        border-radius: 12px;
        margin-bottom: 18px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    
    .company-logo-banner {
        max-height: 55px;
        display: block;
    }
    
    .cover-banner h1 {
        color: #FFFFFF;
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0 0 8px 0;
        letter-spacing: -0.5px;
    }
    
    .cover-banner p {
        color: #93C5FD;
        font-size: 1.05rem;
        margin: 0;
        max-width: 850px;
        font-weight: 400;
    }

    /* Badges / Etiquetas */
    .badge { 
        display: inline-block; 
        padding: 5px 14px; 
        border-radius: 20px; 
        font-size: 0.82rem; 
        font-weight: 700; 
        margin-right: 6px; 
    }
    .badge-cat { background-color: #EFF6FF; color: #1E40AF; border: 1px solid #BFDBFE; }
    .badge-prep { background-color: #F0FDF4; color: #166534; border: 1px solid #BBF7D0; }
    .badge-equip { background-color: #F8FAFC; color: #334155; border: 1px solid #E2E8F0; }
    .badge-life { background-color: #FEF2F2; color: #991B1B; border: 1px solid #FECACA; }

    /* Tarjetas de Receta */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF !important;
        border-radius: 14px !important;
        border: 1px solid #E2E8F0 !important;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05) !important;
    }

    /* Pestañas */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { 
        background-color: #F1F5F9; 
        border-radius: 8px 8px 0 0; 
        padding: 8px 18px; 
        font-weight: 700;
        color: #475569;
    }
    .stTabs [aria-selected="true"] { 
        background-color: #0A192F !important; 
        color: #FFFFFF !important; 
    }
</style>
""",
    unsafe_allow_html=True,
)

# Generación condicional del contenedor del logo en la portada
logo_html = (
    f'<div class="logo-container"><img src="{logo_base64}"'
    ' class="company-logo-banner" alt="Il Mercato Gentiloni"></div>'
    if logo_base64
    else ""
)

# Portada Banner
st.markdown(
    f"""
<div class="cover-banner">
    {logo_html}
    <h1>☕ Manual Operativo & Recetario de Barra</h1>
    <p>Estandarización institucional de bebidas: dosificación exacta por presentación, insumos base y modificadores.</p>
</div>
""",
    unsafe_allow_html=True,
)

# Diccionario inteligente de imágenes
BEVERAGE_IMAGES = {
    "AMERICANO": (
        "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?auto=format&fit=crop&w=600&q=80"
    ),
    "CAPUCCINO": (
        "https://images.unsplash.com/photo-1534778101976-62847782c213?auto=format&fit=crop&w=600&q=80"
    ),
    "LATTE": (
        "https://images.unsplash.com/photo-1570968915860-54d5c301fa9f?auto=format&fit=crop&w=600&q=80"
    ),
    "MATCHA": (
        "https://images.unsplash.com/photo-1536256263959-770b48d82b0a?auto=format&fit=crop&w=600&q=80"
    ),
    "CHOCOLATE": (
        "https://images.unsplash.com/photo-1542990253-0d0f5be5f0ed?auto=format&fit=crop&w=600&q=80"
    ),
    "CHAI": (
        "https://images.unsplash.com/photo-1576092768241-dec231879fc3?auto=format&fit=crop&w=600&q=80"
    ),
    "FRAPPE": (
        "https://images.unsplash.com/photo-1572490122747-3968b75cc699?auto=format&fit=crop&w=600&q=80"
    ),
    "ESPRESSO": (
        "https://images.unsplash.com/photo-1510591509098-f4fdc6d0ff04?auto=format&fit=crop&w=600&q=80"
    ),
    "MOCHA": (
        "https://images.unsplash.com/photo-1578314675249-a6910f80cc4e?auto=format&fit=crop&w=600&q=80"
    ),
    "PUMPKIN": (
        "https://images.unsplash.com/photo-1507138086030-616c3b6db768?auto=format&fit=crop&w=600&q=80"
    ),
    "COCCO": (
        "https://images.unsplash.com/photo-1517701604599-bb29b565090c?auto=format&fit=crop&w=600&q=80"
    ),
}

DEFAULT_IMAGE = (
    "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=600&q=80"
)

MODIFIER_KEYWORDS = [
    "LECHE ENTERA",
    "LECHE LIGHT",
    "LECHE DESLACTOSADA",
    "LECHE DE SOYA",
    "LECHE DE ALMENDRAS",
    "LECHE DE COCO",
    "LECHE DE AVENA",
    "CAFE GOURMET EN GRANO",
    "CAFE DESCAFEINADO",
    "MODIFICADORES",
]


def get_image_for_drink(nombre_bebida, sheet_name):
  nombre_upper = str(nombre_bebida).upper()
  for key, url in BEVERAGE_IMAGES.items():
    if key in nombre_upper:
      return url
  if "FRAPP" in sheet_name.upper():
    return BEVERAGE_IMAGES["FRAPPE"]
  return DEFAULT_IMAGE


@st.cache_data
def parse_cafeteria_excel(file_path):
  xl = pd.ExcelFile(file_path)
  all_recipes = []

  for sheet_name in xl.sheet_names:
    df = xl.parse(sheet_name)

    name_mask = (
        df.iloc[:, 2].astype(str).str.contains("NOMBRE DEL PLATILLO:", na=False)
    )
    recipe_indices = df[name_mask].index.tolist()

    for idx, start_row in enumerate(recipe_indices):
      end_row = (
          recipe_indices[idx + 1]
          if idx + 1 < len(recipe_indices)
          else len(df)
      )
      sub_df = df.iloc[start_row:end_row].reset_index(drop=True)

      nombre = sub_df.iloc[0, 5] if pd.notna(sub_df.iloc[0, 5]) else "Sin Nombre"
      categoria = sheet_name

      foto_url = None
      if len(sub_df) > 2 and pd.notna(sub_df.iloc[2, 5]):
        candidate = str(sub_df.iloc[2, 5]).strip()
        if candidate.startswith("http"):
          foto_url = candidate

      if not foto_url:
        foto_url = get_image_for_drink(nombre, categoria)

      tiempo_prep, tiempo_vida, equipo = "2-5 MIN", "10 MIN", "MÁQUINA ESPRESSO"

      for i in range(min(15, len(sub_df))):
        val_lbl = str(sub_df.iloc[i, 6]).upper()
        if "TIEMPO DE ELABORACIÓN" in val_lbl:
          tiempo_prep = sub_df.iloc[i, 9]
        elif "TIEMPO DE VIDA" in val_lbl:
          tiempo_vida = sub_df.iloc[i, 9]
        elif "EQUIPO" in val_lbl:
          equipo = sub_df.iloc[i, 9]

      ing_header_idx = None
      for i in range(len(sub_df)):
        if "INGREDIENTE" in [str(x).upper() for x in sub_df.iloc[i].values]:
          ing_header_idx = i
          break

      ing_base_12, ing_base_16 = [], []
      mods_12, mods_16 = [], []

      if ing_header_idx is not None:
        ing_df = sub_df.iloc[ing_header_idx + 1 :].dropna(
            subset=[sub_df.columns[2]], how="all"
        )
        for _, ing_row in ing_df.iterrows():
          ing_name = str(ing_row.iloc[2]).strip()
          if (
              ing_name
              and ing_name != "nan"
              and "NOMBRE DEL" not in ing_name
              and ing_name != "INGREDIENTE"
          ):

            is_modifier = any(
                kw in ing_name.upper() for kw in MODIFIER_KEYWORDS
            )

            cant_12 = ing_row.iloc[7] if len(ing_row) > 7 else None
            um_12 = ing_row.iloc[8] if len(ing_row) > 8 else ""
            if pd.notna(cant_12) and cant_12 != 0:
              item_str = f"{ing_name}: **{cant_12} {um_12}**".strip()
              if is_modifier:
                mods_12.append(item_str)
              else:
                ing_base_12.append(item_str)

            cant_16 = ing_row.iloc[10] if len(ing_row) > 10 else None
            um_16 = ing_row.iloc[11] if len(ing_row) > 11 else ""
            if pd.notna(cant_16) and cant_16 != 0:
              item_str = f"{ing_name}: **{cant_16} {um_16}**".strip()
              if is_modifier:
                mods_16.append(item_str)
              else:
                ing_base_16.append(item_str)

      all_recipes.append({
          "Nombre": str(nombre).strip(),
          "Categoria": categoria,
          "Foto": foto_url,
          "Tiempo_Prep": (
              str(tiempo_prep) if pd.notna(tiempo_prep) else "2-5 MIN"
          ),
          "Tiempo_Vida": str(tiempo_vida) if pd.notna(tiempo_vida) else "N/A",
          "Equipo": (
              str(equipo)
              if pd.notna(equipo)
              else "MÁQUINA ESPRESSO / LICUADORA"
          ),
          "Base_12oz": ing_base_12,
          "Mods_12oz": mods_12,
          "Base_16oz": ing_base_16,
          "Mods_16oz": mods_16,
      })

  return pd.DataFrame(all_recipes)


excel_file = "Auditoria Recetas Cafetería 2026.xlsx"
try:
  recipes_df = parse_cafeteria_excel(excel_file)
except Exception as e:
  st.error(f"Error al leer el archivo Excel: {e}")
  st.stop()

# Menú Lateral
st.sidebar.image(LOGO_FILENAME, use_container_width=True)
st.sidebar.title("Filtros de Barra")
cat_filtro = st.sidebar.selectbox(
    "Sección del Menú:",
    ["TODAS"] + list(recipes_df["Categoria"].unique()),
)
busqueda = st.sidebar.text_input("🔎 Buscar por ingrediente o bebida:")

df_display = recipes_df.copy()
if cat_filtro != "TODAS":
  df_display = df_display[df_display["Categoria"] == cat_filtro]

if busqueda:
  df_display = df_display[
      df_display["Nombre"].str.contains(busqueda, case=False, na=False)
      | df_display["Base_12oz"]
          .astype(str)
          .str.contains(busqueda, case=False, na=False)
      | df_display["Base_16oz"]
          .astype(str)
          .str.contains(busqueda, case=False, na=False)
  ]

# Métricas
col_m1, col_m2, col_m3 = st.columns(3)
col_m1.metric("☕ Total Recetas", len(df_display))
col_m2.metric("📋 Categoría", cat_filtro)
col_m3.metric("⏱️ SLA Promedio", "2 - 5 min")

st.markdown("---")

# Renderizado de Tarjetas
if df_display.empty:
  st.warning("No se encontraron recetas con los criterios seleccionados.")
else:
  cols = st.columns(2)
  for idx, row in df_display.reset_index(drop=True).iterrows():
    with cols[idx % 2]:
      with st.container(border=True):
        col_img, col_detail = st.columns([1, 1.4])

        with col_img:
          st.image(row["Foto"], use_container_width=True)

        with col_detail:
          st.markdown(f"### {row['Nombre']}")
          st.markdown(
              f"""
                    <span class="badge badge-cat">{row['Categoria']}</span>
                    <span class="badge badge-prep">⏱️ {row['Tiempo_Prep']}</span>
                    <br><br>
                    <span class="badge badge-equip">🛠️ {row['Equipo']}</span>
                    <span class="badge badge-life">⏳ Vida: {row['Tiempo_Vida']}</span>
                    """,
              unsafe_allow_html=True,
          )

        st.write("")

        tab12, tab16 = st.tabs(["🥤 Presentación 12 oz", "🥤 Presentación 16 oz"])

        with tab12:
          if row["Base_12oz"]:
            st.markdown("**Receta Base:**")
            for ing in row["Base_12oz"]:
              st.markdown(f"• {ing}")
          else:
            st.caption("No aplica / Sin especificación para 12 oz")

          if row["Mods_12oz"]:
            with st.expander("🥛 Opciones de Leche & Modificadores"):
              for mod in row["Mods_12oz"]:
                st.markdown(f"▪️ {mod}")

        with tab16:
          if row["Base_16oz"]:
            st.markdown("**Receta Base:**")
            for ing in row["Base_16oz"]:
              st.markdown(f"• {ing}")
          else:
            st.caption("No aplica / Sin especificación para 16 oz")

          if row["Mods_16oz"]:
            with st.expander("🥛 Opciones de Leche & Modificadores"):
              for mod in row["Mods_16oz"]:
                st.markdown(f"▪️ {mod}")
