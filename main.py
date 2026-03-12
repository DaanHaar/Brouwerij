import streamlit as st

st.set_page_config(
    page_title="De Heren van Vianen Brewery",
    page_icon="🍺",
    layout="wide"
)


col1, col2 = st.columns([1,5])
col1.image("images/logo.png", width=1000)
col2.title("De Heren van Vianen Brewery")
import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_excel("Brouwgegevens.xlsx", sheet_name="Brouwhistorie")

st.title("Brewery Dashboard")

# Clean columns
df["Kosten"] = df["Kosten"].replace('[€,]', '', regex=True).astype(float)
df["Per fles"] = df["Per fles"].replace('[€,]', '', regex=True).astype(float)
df["ABV"] = df["ABV"].replace('%','', regex=True).astype(float) * 100

col1, col2, col3, col4 = st.columns(4)
df = df.iloc[:, 2:]

col1.metric("Total brews", len(df))
col2.metric("Average ABV", f"{df['ABV'].mean():.2f}%")
col3.metric("Average rating", f"{df['Beoordeling'].mean():.1f}")
col4.metric("Avg cost / bottle", f"€{df['Per fles'].mean():.2f}")

style = st.selectbox(
    "Filter by style",
    ["All"] + sorted(df["Type"].dropna().unique().tolist())
)

if style != "All":
    df = df[df["Type"] == style]

st.subheader("Brew Log")

st.dataframe(
    df,
    use_container_width=True, hide_index=True
)

fig = px.scatter(
    df,
    x="ABV",
    y="Beoordeling",
    color="Type",
    hover_name="Naam",
    size="Liters",
    title="ABV vs Rating"
)

st.plotly_chart(fig, use_container_width=True)

fig2 = px.bar(
    df,
    x="Naam",
    y="Per fles",
    color="Type",
    title="Cost per Bottle"
)

st.plotly_chart(fig2, use_container_width=True)

st.subheader("Beer Profiles")

for _, row in df.iterrows():

    image_path = f"images/{row['Naam'].lower().replace(' ','_')}.png"

    col1, col2, col3 = st.columns([1,3,5])

    col1.image(image_path, width=150)

    col2.subheader(row["Naam"])
    col2.write(f"Style: {row['Type']}")
    col2.write(f"ABV: {round(row['ABV'],2)}")
    col2.write(f"Rating: ⭐ {row['Beoordeling']}")

    col3.write(f"IBU: {row['IBU']}")
    col3.write(f"Final gravity: {row['Final Gravity']}")
    col3.write(f"EBC: {row['EBC']}")
    col3.write(f"Per fles: {round(row['Per fles'],2)}")


