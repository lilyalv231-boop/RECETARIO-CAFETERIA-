import pandas as pd
import streamlit as st

# Configuración de página con estética de Cafetería
st.set_page_config(
    page_title="Manual de Recetas - Cafetería", page_icon="☕", layout="wide"
)

# Estilo visual moderno
st.markdown(
    """
<style>
    .main { background-color: #fcfbf9; }
    .stAppHeader { background-color: rgba(0,0,0,0); }
    .badge-bar {
        background-color: #2e1503;
        color: #ffffff;
        padding: 5px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .badge-time {
        background-color: #e8f5e9;
        color: #2e7d32;
        padding: 5px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .badge-equip {
        background-color: #e3f2fd;
        color: #1565c0;
        padding: 5px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .mod-section {
        background-color: #fff9f2;
        border-left: 3px solid #f57c00;
        padding: 8px 12px;
        border-radius: 4px;
        margin-top: 10px;
    }
</style>
""",
    unsafe_allow_html=True,
)

st.title("☕ Recetario & Manual Operativo de Barra")
st.caption("Estandarización de Bebidas, Dosificación e Insumos")


# Palabras clave para detectar modificadores
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


# Función para parsear el Excel agrupando modificadores
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

            # Determinar si es un ingrediente base o modificador
            is_modifier = any(
                kw in ing_name.upper() for kw in MODIFIER_KEYWORDS
            )

            # Extraer 12 oz
            cant_12 = ing_row.iloc[7] if len(ing_row) > 7 else None
            um_12 = ing_row.iloc[8] if len(ing_row) > 8 else ""
            if pd.notna(cant_12) and cant_12 != 0:
              item_str = f"{ing_name}: {cant_12} {um_12}".strip()
              if is_modifier:
                mods_12.append(item_str)
              else:
                ing_base_12.append(item_str)

            # Extraer 16 oz
            cant_16 = ing_row.iloc[10] if len(ing_row) > 10 else None
            um_16 = ing_row.iloc[11] if len(ing_row) > 11 else ""
            if pd.notna(cant_16) and cant_16 != 0:
              item_str = f"{ing_name}: {cant_16} {um_16}".strip()
              if is_modifier:
                mods_16.append(item_str)
              else:
                ing_base_16.append(item_str)

      all_recipes.append({
          "Nombre": str(nombre).strip(),
          "Categoria": categoria,
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


# Cargar datos
excel_file = "Auditoria Recetas Cafetería 2026.xlsx"
try:
  recipes_df = parse_cafeteria_excel(excel_file)
except Exception as e:
  st.error(f"Error al leer el archivo Excel: {e}")
  st.stop()

# Menú Lateral
st.sidebar.header("🔍 Filtros de Barra")
cat_filtro = st.sidebar.selectbox(
    "Sección de Menú:",
    ["TODAS"] + list(recipes_df["Categoria"].unique()),
)
busqueda = st.sidebar.text_input("🔎 Buscar bebida o insumo:")

# Filtrado
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
col1, col2, col3 = st.columns(3)
col1.metric("Bebidas Estandarizadas", len(df_display))
col2.metric("Categoría Activa", cat_filtro)
col3.metric("Pestañas en Menú", recipes_df["Categoria"].nunique())

st.markdown("---")

# Despliegue de Recetas
if df_display.empty:
  st.warning("No se encontraron recetas con los criterios de búsqueda.")
else:
  for idx, row in df_display.iterrows():
    with st.container(border=True):
      header_col1, header_col2 = st.columns([3, 1])

      with header_col1:
        st.subheader(f"🥤 {row['Nombre']}")
        st.markdown(
            f"<span class='badge-bar'>{row['Categoria']}</span> "
            f"<span class='badge-time'>⏱️ Prep: {row['Tiempo_Prep']}</span> "
            f"<span class='badge-equip'>🛠️ {row['Equipo']}</span>",
            unsafe_allow_html=True,
        )

      with header_col2:
        st.caption(f"**Tiempo de vida:** {row['Tiempo_Vida']}")

      st.write("")

      # Columnas de 12 oz y 16 oz
      col_12, col_16 = st.columns(2)

      # Render 12 oz
      with col_12:
        st.markdown("##### 🥤 Presentación 12 oz")
        st.markdown("**Receta Base:**")
        if row["Base_12oz"]:
          for ing in row["Base_12oz"]:
            st.write(f"• {ing}")
        else:
          st.info("Sin receta base especificada")

        if row["Mods_12oz"]:
          with st.expander("🥛 Opciones de Leche / Modificadores (12 oz)"):
            for mod in row["Mods_12oz"]:
              st.write(f"▪️ {mod}")

      # Render 16 oz
      with col_16:
        st.markdown("##### 🥤 Presentación 16 oz")
        st.markdown("**Receta Base:**")
        if row["Base_16oz"]:
          for ing in row["Base_16oz"]:
            st.write(f"• {ing}")
        else:
          st.info("Sin receta base especificada")

        if row["Mods_16oz"]:
          with st.expander("🥛 Opciones de Leche / Modificadores (16 oz)"):
            for mod in row["Mods_16oz"]:
              st.write(f"▪️ {mod}")
