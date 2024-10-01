import streamlit as st
import utils as U

import pandas as pd
# import utils as U
import plotly.express as px
import plotly.graph_objects as go

def get_data():
    df = pd.read_csv("affil_data.csv")
    df = U.filter_df(df)
    df = U.convert_to_datetime(df, ["start", "end"])

    return df

df = get_data()



st.header("Our very cool visualisations!")
country_code = st.selectbox("Country code", df["Occ"].unique())

df_ch = df[df["Occ"] == "CH"]

startyear_count_data = {
    "year": [int(i) for i in df_ch[df_ch["role_category"] == "phd"]["startyear"].value_counts().sort_index().keys()],
    "postdoc" : list(df_ch[df_ch["role_category"] == "postdoc"]["startyear"].value_counts().sort_index()),
    "phd" : list(df_ch[df_ch["role_category"] == "phd"]["startyear"].value_counts().sort_index()),
    "prof" : list(df_ch[df_ch["role_category"] == "prof"]["startyear"].value_counts().sort_index()),
}
df_startyear_count_data = pd.DataFrame(data=startyear_count_data)
df_startyear_count_data["total"] = df_startyear_count_data["postdoc"] + df_startyear_count_data["phd"] + df_startyear_count_data["prof"]
df_startyear_count_data['phd_proportion'] = df_startyear_count_data['phd'] / df_startyear_count_data['total']
df_startyear_count_data['postdoc_proportion'] = df_startyear_count_data['postdoc'] / df_startyear_count_data['total']
df_startyear_count_data['prof_proportion'] = df_startyear_count_data['prof'] / df_startyear_count_data['total']

line_num_pos = px.line(df_startyear_count_data, x='year', y=["phd", "postdoc", "prof"],
        title='Number of positions by role over years')

bar_stacked_num_pos = px.bar(df_startyear_count_data, x='year', y=["phd", "postdoc", "prof"],
        title='Number of positions by role over years')

bar_proportions_num_pos = px.bar(df_startyear_count_data, x='year', y=['phd_proportion', 'postdoc_proportion', 'prof_proportion'],
       title='Proportion of positions by role over years')


df_ch["duration_position"] = (df_ch["end"] - df_ch["start"]).dt.days/365
df_ch["is_female"] = (df_ch['p(gf)'] > 0.5).astype(int)

st.plotly_chart(line_num_pos)
st.plotly_chart(bar_stacked_num_pos)
st.plotly_chart(bar_proportions_num_pos)

role = st.selectbox("Role", ["PhD", "Postdoc", "Prof"]).lower()

df_ch_pos = df_ch[df_ch["role_category"].isin(["phd", "postdoc", "prof"])]
df_ch_pos = df_ch_pos[df_ch_pos["role_category"] == role]

fig_gender = px.box(df_ch_pos, x="startyear", y="duration_position", color="is_female")
st.plotly_chart(fig_gender)
# fig.update_traces(quartilemethod="inclusive")

