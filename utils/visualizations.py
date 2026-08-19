"""Data visualization utilities using Plotly."""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np


def create_energy_trend_chart(df):
    """Create energy consumption trend chart."""
    if "Datetime" in df.columns and "AEP_MW" in df.columns:
        fig = px.line(df, x="Datetime", y="AEP_MW", title="Energy Consumption Trend",
                     labels={"AEP_MW": "Energy (MW)", "Datetime": "Date"})
        fig.update_layout(template="plotly_dark", hovermode="x unified")
        return fig
    elif "Energy_Consumption_kWh" in df.columns:
        fig = px.line(df, y="Energy_Consumption_kWh", title="Energy Consumption Trend",
                     labels={"Energy_Consumption_kWh": "Energy (kWh)"})
        fig.update_layout(template="plotly_dark", hovermode="x unified")
        return fig
    return None


def create_scatter_chart(df, x_col, y_col, title="Scatter Plot"):
    """Create scatter plot comparing two variables."""
    fig = px.scatter(df, x=x_col, y=y_col, title=title, trendline="ols",
                    labels={x_col: x_col.replace("_", " ").title(),
                           y_col: y_col.replace("_", " ").title()})
    fig.update_layout(template="plotly_dark", hovermode="closest")
    return fig


def create_correlation_heatmap(df):
    """Create correlation heatmap for numeric columns."""
    numeric_df = df.select_dtypes(include=[np.number])
    corr_matrix = numeric_df.corr()

    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale="RdBu",
        zmid=0,
    ))
    fig.update_layout(title="Correlation Heatmap", template="plotly_dark")
    return fig


def create_distribution_chart(df, col, title="Distribution"):
    """Create distribution histogram."""
    fig = px.histogram(df, x=col, title=title, nbins=50,
                      labels={col: col.replace("_", " ").title()})
    fig.update_layout(template="plotly_dark", showlegend=False)
    return fig


def create_bar_chart(df, x_col, y_col, title="Bar Chart"):
    """Create bar chart."""
    fig = px.bar(df, x=x_col, y=y_col, title=title,
                labels={x_col: x_col.replace("_", " ").title(),
                       y_col: y_col.replace("_", " ").title()})
    fig.update_layout(template="plotly_dark")
    return fig


def create_box_plot(df, y_col, x_col=None, title="Box Plot"):
    """Create box plot."""
    fig = px.box(df, y=y_col, x=x_col, title=title)
    fig.update_layout(template="plotly_dark")
    return fig


def create_hourly_consumption_chart(df):
    """Create hourly average energy consumption."""
    if "hour" in df.columns and "AEP_MW" in df.columns:
        hourly_avg = df.groupby("hour")["AEP_MW"].mean()
        fig = px.bar(x=hourly_avg.index, y=hourly_avg.values,
                    title="Average Hourly Energy Consumption",
                    labels={"x": "Hour", "y": "Energy (MW)"})
        fig.update_layout(template="plotly_dark")
        return fig
    return None


def create_weather_distribution(df):
    """Create weather distribution pie chart."""
    if "Weather" in df.columns:
        weather_counts = df["Weather"].value_counts()
        fig = px.pie(values=weather_counts.values, names=weather_counts.index,
                    title="Weather Distribution")
        fig.update_layout(template="plotly_dark")
        return fig
    return None


def create_comparison_chart(models_metrics):
    """Create model comparison bar chart."""
    df_metrics = pd.DataFrame(models_metrics).T
    fig = px.bar(df_metrics, barmode="group", title="Model Performance Comparison",
                labels={"value": "Score", "index": "Model"})
    fig.update_layout(template="plotly_dark")
    return fig
