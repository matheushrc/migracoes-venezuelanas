from typing import Any, cast

import pandas as pd
import pydeck as pdk
import streamlit as st

st.set_page_config(page_title="Migration Map", layout="wide")
st.title("Venezuelan Migration Routes")

# Load data
coordinates = pd.read_csv("outputs/entrevistas_coordinates.csv")

# Color palette for each person (RGB format for pydeck)
COLORS = {
    1: [255, 107, 107],  # Red
    2: [78, 205, 196],  # Teal
    3: [69, 183, 209],  # Blue
    4: [150, 206, 180],  # Green
    5: [255, 234, 167],  # Yellow
    6: [221, 160, 221],  # Plum
    8: [255, 140, 0],  # Orange
}

# Hex colors for legend display
COLORS_HEX = {
    1: "#FF6B6B",
    2: "#4ECDC4",
    3: "#45B7D1",
    4: "#96CEB4",
    5: "#FFEAA7",
    6: "#DDA0DD",
    8: "#FF8C00",
}

# Get unique person IDs
person_ids = sorted(coordinates["id"].unique())


# Create colored pill labels for each person
def format_person(pid):
    return f"Entrevistado {pid}"


# Use pills for person selection (cleaner UI)
selected_persons = st.pills(
    "Selecione Entrevistados",
    options=person_ids,
    format_func=format_person,
    selection_mode="multi",
    default=person_ids,
)

# Show color legend
st.markdown(
    "**Legenda:** "
    + " ".join([
        f'<span style="color:{COLORS_HEX.get(pid, "#808080")}; font-size: 16px;">● Entrevistado {pid}</span>'
        for pid in person_ids
    ]),
    unsafe_allow_html=True,
)


def create_arc_data(df: pd.DataFrame) -> pd.DataFrame:
    """Create arc data connecting consecutive points for each person."""
    arcs = []
    for person_id in df["id"].unique():
        person_df = df[df["id"] == person_id].reset_index(drop=True)
        color = COLORS.get(person_id, [128, 128, 128])
        for i in range(len(person_df) - 1):
            arcs.append({
                "id": person_id,
                "source_lat": person_df.loc[i, "latitude"],
                "source_lon": person_df.loc[i, "longitude"],
                "target_lat": person_df.loc[i + 1, "latitude"],
                "target_lon": person_df.loc[i + 1, "longitude"],
                "source_address": (person_df.loc[i, "address"]).split(",")[0],
                "target_address": (person_df.loc[i + 1, "address"]).split(",")[0],
                "color": color,
            })
    return pd.DataFrame(arcs)


# Filter data based on selection
if selected_persons:
    filtered_df = coordinates[coordinates["id"].isin(selected_persons)].copy()

    # Add color column based on person ID
    filtered_df["color"] = filtered_df["id"].map(COLORS)

    # Create arc data for migration routes
    arc_data = create_arc_data(filtered_df)

    # Calculate center of all points
    center_lat = filtered_df["latitude"].mean()
    center_lon = filtered_df["longitude"].mean()

    # Create scatterplot layer for locations
    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        data=filtered_df,
        get_position=["longitude", "latitude"],
        get_color="color",
        get_radius=15000,  # Radius in meters
        pickable=True,
        auto_highlight=True,
    )

    # Create arc layer for migration routes
    arc_layer = pdk.Layer(
        "ArcLayer",
        data=arc_data,
        get_source_position=["source_lon", "source_lat"],
        get_target_position=["target_lon", "target_lat"],
        get_source_color="color",
        get_target_color="color",
        get_width=3,
        pickable=True,
        auto_highlight=True,
    )

    # Create view state
    view_state = pdk.ViewState(
        latitude=center_lat,
        longitude=center_lon,
        zoom=3,
        pitch=0,
    )

    # Create deck with tooltip
    tooltip_config: dict[str, Any] = {
        "text": "Entrevistado {id}\n{source_address} → {target_address}",
        "style": {
            "backgroundColor": "steelblue",
            "color": "white",
            "fontSize": "14px",
            "padding": "10px",
        },
    }

    deck = pdk.Deck(
        layers=[arc_layer, scatter_layer],
        initial_view_state=view_state,
        map_style=cast(str, None),  # Use Streamlit theme
        tooltip=cast(bool, tooltip_config),
    )

    st.pydeck_chart(deck)

    # Show data table
    st.subheader("Detalhes das Localizações")
    st.dataframe(filtered_df[["id", "address"]], width="stretch")
else:
    st.warning("Por favor, selecione pelo menos um entrevistado.")
