
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Illinois Building Inventory", layout="wide")

st.title("Illinois State Building Inventory")
st.write("Exploring building construction and size across Illinois state agencies.")

url = "https://raw.githubusercontent.com/UIUC-iSchool-DataViz/is445_data/main/building_inventory.csv"

@st.cache_data
def load_data():
    return pd.read_csv(url, low_memory=False)

df = load_data()

df["Year Constructed"] = pd.to_numeric(df["Year Constructed"], errors="coerce")
df["Square Footage"] = pd.to_numeric(df["Square Footage"], errors="coerce")

st.header("1. Building Construction by Decade")

construction = df.dropna(subset=["Year Constructed", "Agency Name"]).copy()
construction = construction[
    construction["Year Constructed"].between(1800, 2026)
].copy()

construction["Decade"] = (
    construction["Year Constructed"] // 10 * 10
).astype(int)

agencies = ["All Agencies"] + sorted(construction["Agency Name"].unique().tolist())

selected_agency = st.selectbox(
    "Select an agency:",
    agencies
)

if selected_agency != "All Agencies":
    filtered = construction[
        construction["Agency Name"] == selected_agency
    ]
else:
    filtered = construction

decade_counts = (
    filtered.groupby("Decade")
    .size()
    .reset_index(name="Buildings")
)

decade_counts["Decade Label"] = decade_counts["Decade"].astype(str) + "s"

chart1 = (
    alt.Chart(decade_counts)
    .mark_bar(color="#4285F4")
    .encode(
        x=alt.X(
            "Decade Label:N",
            sort=alt.SortField(field="Decade", order="ascending"),
            title="Decade",
            axis=alt.Axis(labelAngle=-45)
        ),
        y=alt.Y("Buildings:Q", title="Number of Buildings"),
        tooltip=[
            alt.Tooltip("Decade Label:N", title="Decade"),
            alt.Tooltip("Buildings:Q", title="Buildings")
        ]
    )
    .properties(height=400)
)

st.altair_chart(chart1, use_container_width=True)

st.write(
    "This visualization shows the number of buildings constructed "
    "during each decade in the Illinois Building Inventory. "
    "The bar chart makes it easier to compare construction activity "
    "across different periods. I chose a blue color for the bars "
    "and a linear scale for the number of buildings so that the "
    "differences between decades are easy to identify. "
    "I also included a dropdown menu that allows users to filter "
    "the results by state agency, making it possible to compare "
    "construction trends for individual agencies. If I had more "
    "time, I would add another filter for building usage to see "
    "whether different types of buildings were constructed during "
    "different periods."
)

st.divider()

st.header("2. Total Building Square Footage by Agency")

size_data = df.dropna(subset=["Agency Name", "Square Footage"]).copy()
size_data = size_data[size_data["Square Footage"] > 0]

agency_sizes = (
    size_data.groupby("Agency Name")["Square Footage"]
    .sum()
    .reset_index()
    .sort_values("Square Footage", ascending=False)
    .head(12)
)

agency_sizes["Million Sq Ft"] = agency_sizes["Square Footage"] / 1000000

chart2 = (
    alt.Chart(agency_sizes)
    .mark_bar(color="#16A085")
    .encode(
        x=alt.X(
            "Million Sq Ft:Q",
            title="Total Square Footage (Millions)"
        ),
        y=alt.Y(
            "Agency Name:N",
            sort="-x",
            title=None,
            axis=alt.Axis(labelLimit=350, labelFontSize=12)
        ),
        tooltip=[
            alt.Tooltip("Agency Name:N", title="Agency"),
            alt.Tooltip("Square Footage:Q", title="Square Footage", format=",.0f")
        ]
    )
    .properties(height=500)
)

st.altair_chart(chart2, use_container_width=True)

st.write(
    "This visualization compares the total square footage of "
    "buildings associated with different Illinois state agencies. "
    "I wanted to highlight which agencies account for the largest "
    "amount of building space rather than simply comparing the "
    "number of buildings they have. I chose a horizontal bar chart "
    "because some of the agency names are quite long and would "
    "be difficult to read on a vertical chart. The agencies are "
    "sorted from largest to smallest, and the square footage is "
    "displayed in millions to make the values easier to understand. "
    "I used a green color to distinguish this visualization from "
    "the first one. If I had more time, I would include a filter "
    "for building status to compare buildings currently in use "
    "with those that are no longer being used."
)

st.divider()

st.header("Homework #5 Comparison")

st.write(
    "For Homework #5, I used the Bigfoot sightings dataset to "
    "create visualizations examining reports across different "
    "states and over time. For this assignment, I chose a "
    "completely different dataset focused on Illinois state "
    "buildings. Both visualizations were created specifically "
    "for Homework #6 and do not reuse the plots or written "
    "analysis from Homework #5."
)

st.caption("Data source: UIUC IS 445 Illinois Building Inventory dataset")
