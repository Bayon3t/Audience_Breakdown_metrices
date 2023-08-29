import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import io
import plotly.graph_objs as go


st.set_page_config(page_title="Dashboard", page_icon="🌍", layout="wide")
st.subheader("🔔 Audiences Breakdown")
st.sidebar.image("data/logo1.png", caption="Audiences Calculator")

ad_spend_old = 0.0 # Placeholder value, replace with your actual value
average_order_value_old = 0.0  # Placeholder value, replace with your actual value
total_sales_old = 0.0  # Placeholder value, replace with your actual 


def calculate_metric_differences(old_values, new_values):
    differences = {}
    ad_spend_variant = old_values["ad_spend"] - new_values["ad_spend"]
    average_order_value = old_values["average_order_value"] - new_values["average_order_value"]
    total_sales = new_values["total_sales"] - old_values["total_sales"]
    cpa = old_values["cpa"] - new_values["cpa"]
    revenue = new_values["revenue"] - old_values["revenue"]
    total_profit_after_adspend = new_values["total_profit_after_adspend"] - old_values["total_profit_after_adspend"]
    site_conversion_rate = new_values["site_conversion_rate"] - old_values["site_conversion_rate"]
    click_conversion_rate = new_values["click_conversion_rate"] - old_values["click_conversion_rate"]
    click = new_values["click"] - old_values["click"]
    cost_per_click = old_values["cost_per_click"] - new_values["cost_per_click"]
    impression_needed = new_values["impression_needed"] - old_values["impression_needed"]
    cost_per_1000_impression = old_values["cost_per_1000_impression"] - new_values["cost_per_1000_impression"]
    cost_per_1_impression = old_values["cost_per_1_impression"] - new_values["cost_per_1_impression"]
    differences = {
        "ad_spend_variant $": ad_spend_variant,
        "average_order_value $": average_order_value,
        "total_sales": total_sales,
        "cpa $": cpa,
        "revenue $": revenue,
        "total_profit_after_adspend $": total_profit_after_adspend,
        "site_conversion_rate %": site_conversion_rate, 
        "click_conversion_rate %": click_conversion_rate,
        "click": click,
        "cost_per_click $": cost_per_click,
        "impression_needed": impression_needed,
        "cost_per_1000_impression $": cost_per_1000_impression,
        "cost_per_1_impression $": cost_per_1_impression
    }
    return differences

def get_metric_input(metric_name, default_value, column):
    return column.number_input(f"{metric_name.replace('_', ' ').title()} (Old):", value=default_value)

st.sidebar.header("Metrics Input ⌨")
col1, col2 = st.sidebar.columns(2)
old_metrics = {
    "ad_spend": get_metric_input("ad_spend", ad_spend_old, col1),
    "average_order_value": get_metric_input("average_order_value", average_order_value_old, col1),
    "total_sales": get_metric_input("total_sales", total_sales_old, col1),
    "cpa": col1.number_input("CPA (Old):", value=0.0),
    "revenue": col1.number_input("Revenue (Old):", value=0.0),
    "total_profit_after_adspend": col1.number_input("Total Profit After Ad Spend (Old):", value=0.0),
    "site_conversion_rate": col1.number_input("Site Conversion Rate (Old):", value=0.0),
    "click_conversion_rate": col1.number_input("Click Conversion Rate (Old):", value=0.0),
    "click": col1.number_input("Click (Old):", value=0.0),
    "cost_per_click": col1.number_input("Cost Per Click (Old):", value=0.0),
    "impression_needed": col1.number_input("Impression Needed (Old):", value=0.0),
    "cost_per_1000_impression": col1.number_input("Cost Per 1000 Impression (Old):", value=0.0),
    "cost_per_1_impression": col1.number_input("Cost Per 1 Impression (Old):", value=0.0)
}
new_metrics = {
    "ad_spend": col2.number_input("Ad Spend (New):", value=ad_spend_old),
    "average_order_value": col2.number_input("Average Order Value (New):", value=average_order_value_old),
    "total_sales": col2.number_input("Total Sales (New):", value=total_sales_old),
    "cpa": col2.number_input("CPA (New):", value=0.0),
    "revenue": col2.number_input("Revenue (New):", value=0.0),
    "total_profit_after_adspend": col2.number_input("Total Profit After Ad Spend (New):", value=0.0),
    "site_conversion_rate": col2.number_input("Site Conversion Rate (New):", value=0.0),
    "click_conversion_rate": col2.number_input("Click Conversion Rate (New):", value=0.0),
    "click": col2.number_input("Click (New):", value=0.0),
    "cost_per_click": col2.number_input("Cost Per Click (New):", value=0.0),
    "impression_needed": col2.number_input("Impression Needed (New):", value=0.0),
    "cost_per_1000_impression": col2.number_input("Cost Per 1000 Impression (New):", value=0.0),
    "cost_per_1_impression": col2.number_input("Cost Per 1 Impression (New):", value=0.0)
}

metric_differences = calculate_metric_differences(old_metrics, new_metrics)

st.sidebar.subheader("Metric Differences")
for metric, difference in metric_differences.items():
    st.sidebar.write(f"{metric.replace('_', ' ').title()}: {difference}")
st.sidebar.success("Metrics Calculated Successful!")

df = pd.DataFrame.from_dict(metric_differences, orient='index', columns=['difference'])
df['metric'] = df.index
df['cumulative_difference'] = df['difference'].cumsum()




# Streamlit app
st.header("Data Analysis")

# Trend Chart for Metrics Difference

fig_line = px.line(df, x='metric', y='cumulative_difference', title='Trend Chart for Metrics Difference 📈')
st.plotly_chart(fig_line)


# Funnel Chart for Metric Differences
metric_names = list(df['metric'])
metric_differences = list(df['difference'])

funnel_chart = go.Funnel(
    y=metric_names,
    x=metric_differences,
    textinfo="value+percent initial",
    opacity=0.65,
    marker=dict(color='skyblue')
    #marker=dict(color='rgb(255,0,0)')
)

layout = go.Layout(
    title='Funnel Chart - Metric Differences',
    xaxis=dict(title='Difference'),
    yaxis=dict(title='Metrics'),
)
fig_funnel = go.Figure(data=[funnel_chart], layout=layout)
fig_funnel.update_layout(margin=dict(t=50, l=0, r=0, b=0))

st.header('Funnel Chart Visualization')
st.plotly_chart(fig_funnel, use_container_width=True)

