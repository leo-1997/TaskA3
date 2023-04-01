import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from plotly.offline import plot
import plotly.express as px

# Load COE data
df = pd.read_csv('coe_data.csv')

df["Date"] = pd.to_datetime(df["Announcement Date"], format='%d/%m/%Y')
df.set_index(["Date"], inplace=True)
df = df.sort_values(by='Date', ascending=True)
df["COE Price"] = df["Quota Premium"].str.replace("[\$\,\.]", "")
df[['COE Price']] = df[['COE Price']].apply(pd.to_numeric) 
df['Date'] = df.index

fig = make_subplots(rows=3, cols=1, shared_xaxes=False, vertical_spacing=0.1, subplot_titles=("COE Price","Category A quota and biddings","Category B quota and biddings"), specs=[[{}],[{"secondary_y": True}],[{"secondary_y": True}]])
# Create a list of traces for each category for the first plot
price_traces = []
# bidding row starts at 2
for category, category_data in df.groupby(['Category']):
    category_data = df[df['Category'] == category]
    trace = go.Scatter(x=category_data['Date'], y=category_data['COE Price'], mode='lines', name=f'Category {category}', legendgroup = '1')
    price_traces.append(trace)

# Create a trace for quota and biddings for the second plot
category_a_data = df[df['Category'] == 'Cat A (Cars up to 1600cc and 97kW)']
# category_a_data = category_a_data.sort_values(by='Quota', ascending=True)
quota_a_trace = go.Bar(x=category_a_data['Date'], y=category_a_data['Quota'], marker_color="blue", name='Quota', legendgroup = '2')
biddings_a_trace = go.Bar(x=category_a_data['Date'], y=category_a_data['Total Bids Received'], marker_color = "red", name='Biddings', legendgroup = '2')
catA_trace = go.Scatter(x=category_a_data['Date'], y=category_a_data['COE Price'], mode='lines', name='price', legendgroup = '2')
catA_trace.update(showlegend = True, hovertemplate='<b>$%{y:.2f}</b>')

category_b_data = df[df['Category'] == 'Cat B (Cars above 1600cc or 97kW)']
# category_a_data = category_a_data.sort_values(by='Quota', ascending=True)
quota_b_trace = go.Bar(x=category_b_data['Date'], y=category_b_data['Quota'], marker_color="blue", name='Quota', legendgroup = '3')
biddings_b_trace = go.Bar(x=category_b_data['Date'], y=category_b_data['Total Bids Received'], marker_color = "red", name='Biddings', legendgroup = '3')
catB_trace = go.Scatter(x=category_b_data['Date'], y=category_b_data['COE Price'], mode='lines', name='price', legendgroup = '3')
catB_trace.update(showlegend = True, hovertemplate='<b>$%{y:.2f}</b>')

# Add the traces to the subplots
for trace in price_traces:
    fig.add_trace(trace, row=1, col=1)

fig.add_trace(quota_a_trace, row=2, col=1)
fig.add_trace(biddings_a_trace, row=2, col=1)
fig.add_trace(catA_trace, row=2, col=1, secondary_y=True)
fig.add_trace(quota_b_trace, row=3, col=1)
fig.add_trace(biddings_b_trace, row=3, col=1)
fig.add_trace(catB_trace, row=3, col=1, secondary_y=True)
fig.update_layout(autotypenumbers='convert types')

# Create the layout for the first plot
layout1 = go.Layout(title='Singapore COE Price Trend', xaxis=dict(title='Date'), yaxis=dict(title='COE Price'))

# Create the layout for the second plot
layout2 = go.Layout(title='Category B Quota and Biddings Trend', xaxis=dict(title='Date'), yaxis=dict(title='Number'))

# Update the layout for both subplots
fig.update_layout(hovermode='x unified', hoverlabel=dict(bgcolor='rgba(255,255,255,0.65)', font=dict(color='black')))

# Add a hovertemplate to show the exact price and date for all categories for the first plot
for trace in fig['data'][:5]:
    trace.update(showlegend = True, hovertemplate='<b>$%{y:.2f}</b>')

# Set the overall title for the subplots
fig.update_layout(height=1500, width=1800, title_text='Singapore COE Trend', legend_tracegroupgap= 400)

# Display the plot
plot(fig)
