import plotly.express as px  # type: ignore

# PIE CHART

def pie_chart(df):

    fig = px.pie(
        df,
        names='Category',
        title='Groundwater Categories'
    )

    return fig


# BAR CHART

def bar_chart(df):

    fig = px.bar(
        df,
        x='Taluka',
        y='Annual Recharge (MCM)',
        color='Category',
        title='Taluka Recharge Analysis'
    )

    return fig


# LINE CHART

def line_chart(df):

    fig = px.line(
        df,
        x='Year',
        y='Total Extraction (MCM)',
        color='Taluka',
        title='Year-wise Extraction Trend'
    )

    return fig