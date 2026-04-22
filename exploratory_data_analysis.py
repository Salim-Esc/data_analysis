#all the imports
import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px

st.set_page_config(layout='wide')

#read data
df = pd.read_csv('./Global Youtube Statistics.csv', encoding='latin1')
pd.set_option("display.float_format", '{:.2}'.format)

#operations
total_views_on_platform = df['video views'].sum()
total_subs_on_platform = df['subscribers'].sum()
total_subs_generated_last_30_days = df['subscribers_for_last_30_days'].sum()
total_uploads = df['uploads'].sum()

category_mean_susbcribers = (df.groupby('category')['subscribers'].mean()).sort_values(ascending=False)

channel_type_count = df['channel_type']

total_subs_by_country = (df.groupby('Country')['subscribers'].sum()).sort_values(ascending=False)

unemployment_rate_by_country = (df.groupby('Country')['Unemployment rate'].mean()).sort_values(ascending=False)

avg_subs_by_category_country = df.groupby(['category', 'Country'])['subscribers'].mean().unstack()

#tabular presentation of categories
different_categories = df['channel_type'][df['channel_type'].notna()].unique().to_numpy(dtype=object)
n_cols = 7
rows = int(np.floor(len(different_categories) / n_cols))
categories = pd.DataFrame(different_categories.reshape(rows, n_cols))

#streamlit
st.title("Dashboard")

#dashboard phase 1
def metric_card(title, value, bg_color):
    st.markdown(f"""
    <div style="
        background: {bg_color};
        padding: 15px;
        border-radius: 12px;
        color: white;
        width: 200px;
        height: 80px;
        autoflow: hidden;
        margin: 5px
    ">
        <div style="font-size:12px; opacity:0.8; font-weight:bold;">{title}</div>
        <div style="font-size:22px; font-weight:bold;">{value:.0f}</div>
    </div>
    """, unsafe_allow_html=True)

metric1container = st.container()

with metric1container:
    col1, col2, col3 = st.columns([2,1,1])
    with col1:
        c1, c2, c3 = st.columns(3, gap='small')
        with c1: 
            metric_card("Total uploads on platform", total_uploads, "linear-gradient(135deg, #7F00FF, #E100FF)")
        with c2: 
            metric_card("Total views on platform", total_views_on_platform, "linear-gradient(135deg, #7F00FF, #E100FF)")
        with c3: 
            metric_card("Total subs", total_subs_on_platform, "linear-gradient(135deg, #7F00FF, #E100FF)")

        st.write("")

        st.markdown("<h4 style='font-size:20px; weight:bold;'>Video Categories</h4>", unsafe_allow_html=True)
        st.dataframe(categories, hide_index=True, use_container_width=True, height=100)

    with col3:
        st.write('Source of data:https://www.kaggle.com/datasets/nelgiriyewithana/global-youtube-statistics-2023')
#dashboard phase 2
#subdist = ff.create_distplot([df['subscribers'].dropna()], ['subscribers'], show_hist=False)

chart1, chart2 = st.columns(2)

#videoviewsvsearning = px.scatter(df, x='Population', y='Urban_population')
categoryvsmeansubs = px.bar(category_mean_susbcribers, y='subscribers', title='Most subscriebed categories')
categoryvsmeansubs.update_layout(xaxis_tickangle = 45)

subsvsvideoviews = px.scatter(df.sort_values(ascending=False, by='video views').head(50), x='subscribers', y='video views', size='video views', color='category', title='Most viewed category')

channel_type_count_px = px.pie(channel_type_count, names='channel_type', title='Channel Type Population')

total_subs_by_country_px = px.bar(total_subs_by_country.head(20), y='subscribers', title='Total subscribers distribution by countries')
total_subs_by_country_px.update_layout(xaxis_tickangle = 45)

unemployment_rate_by_country_px = px.line(unemployment_rate_by_country.head(25), labels={'value':'Unemployment Rate'}, title="Unemployment Rate by Country  ")
unemployment_rate_by_country_px.update_layout(showlegend=False, xaxis_tickangle = 45)

avg_subs_by_category_country_px = px.imshow(avg_subs_by_category_country, color_continuous_scale='viridis', title='Subscribers form different country over differetn categories')
avg_subs_by_category_country_px.update_layout(title_y=0.8 ,coloraxis_showscale=True, xaxis_tickangle = 45)


with chart1:
    st.plotly_chart(categoryvsmeansubs)
    st.plotly_chart(subsvsvideoviews)
    st.plotly_chart(channel_type_count_px)

with chart2:
    st.plotly_chart(total_subs_by_country_px)
    st.plotly_chart(unemployment_rate_by_country_px)
    st.plotly_chart(avg_subs_by_category_country_px)

st.markdown("<h6 style='text-align: center;'>| Built with Streamlit 📊|</h6>", unsafe_allow_html=True)
