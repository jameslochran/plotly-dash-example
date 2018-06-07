# -*- coding: utf-8 -*-
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
#import re




all_data = pd.read_csv('campaign_data.csv')







app = dash.Dash()

df = all_data
metrics = ["LIKES","COMMENTS","ENGAGEMENT RATE","EXPECTED ENGAGEMENT","ENGAGEMENT RATIO"]
campaigns = ["Reduce your Footprint","Making the ROI Case","Bridging The Gap"]

colour_dict = {}
colour_dict["Reduce your Footprint"] = 'rgb(240,21,22)'
colour_dict["Making the ROI Case"] = 'rgb(22,96,185)'
colour_dict["Bridging The Gap"] = 'rgb(6,193,95)'

external_css = [ "https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
        "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
        "//fonts.googleapis.com/css?family=Raleway:400,300,600",
        "https://cdn.rawgit.com/plotly/dash-app-stylesheets/5047eb29e4afe01b45b27b1d2f7deda2a942311a/goldman-sachs-report.css",
        "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]

for css in external_css:
    app.css.append_css({ "external_url": css })


app.layout = html.Div([
 		html.Div([
        html.Img(src="https://www.pcr-online.biz/.image/t_share/MTUxOTMyMjgxNDQ3NTg5MTU1/18-pcr-market-report-iconjpg.jpg",
                style={
                    'height': '50px',
                    'float': 'right',
                    'position': 'relative',
                    'top':'0px',
                    'bottom': '0px',
                    'left': '0px'
                },
                ),
        html.H2('Marketing Campaign Interactivity Report',
                style={
                    'position': 'relative',
                    'top': '0px',
                    'left': '0px',
                    'font-family': 'Dosis',
                    'display': 'inline',
                    'font-size': '4.0rem',
                    'color': '#4D637F'
                }),


    	], className='container', style={'padding':'0px','position': 'relative', 'right': '5px', 'width':'100%', 'color':'#fff'}),
				html.Div([
					html.Div([
						html.H6('Choose Metric:', className = "gs-header gs-text-header padded")
						],
						style={'width': '25%', 'display': 'inline-block'}
					),
					html.Div([
						html.H6('Choose Campaign:', className = "gs-header gs-text-header padded")
						],
						style={'width': '50%', 'display': 'inline-block'}
					),
					html.Div([
						html.H6('Choose Country:', className = "gs-header gs-text-header padded")
						],
						style={'width': '25%', 'display': 'inline-block'}
					),
				], style={'width':'90%', 'padding-left':'80px'}),
				html.Div([
					html.Div([
						dcc.Dropdown(
							id='yaxis-column',
							options=[{'label': i, 'value': i} for i in metrics],
							value='ENGAGEMENT RATIO')
						],
						style={'width': '25%', 'display': 'inline-block'}
					),
					html.Div([
						dcc.Dropdown(
							id='campaign-selection',
							options=[{'label': i, 'value': i} for i in campaigns],
							multi=True,
							value=campaigns)
						],
						style={'width': '50%', 'display': 'inline-block'}
					),
					html.Div([
						dcc.Dropdown(
							id='country-selection',
							value='All')
						],
						style={'width': '25%', 'display': 'inline-block'}
					)
				], style={'width':'90%', 'padding-left':'80px'}),
				html.Div([
				    html.H6('Click on the campaign name to remove it from the graph. The lines represent the average for each campaign.',style={'width':'90%', 'padding-left':'80px'} ),
					html.Div([
						dcc.Graph(id='main-graph')
						],
						style={'width': '80%', 'display': 'block', 'margin-left':'100px'}
					),
				],
				className='row'
				),
				html.Div([
					html.H4('Select a point above to see the details below.'),
					html.Div([
						html.H6('Selected Post:', className = "gs-header gs-text-header padded")
						],
						style={'width': '100%', 'display': 'inline-block'}
					)
				], style={'width':'90%', 'padding-left':'80px'}),
				html.Div([
					html.Div([
						html.A([
							html.Img(id='selected-post-image',
									style={'position': 'relative',
										   'height' : '150',
										   'width' : '150',
										   'left' : '30%',
										   'top' : '30'})
							],
							id='selected-post-hyperlink',
							target='_blank'
						)
					],style={'width': '50%', 'display': 'inline-block'}
					),
					html.Div([
						html.A([
							html.H5(id='selected-ig-handle')
							],
							id='selected-ig-handle-hyperlink',
							target='_blank',
							className='column',
							style={'position': 'relative',
									'display':'none',
								   'left' : '27%',
								   'top' : '5'}
						),
						html.H5(id='selected-likes',
								className='column',
								style={'position': 'relative',
									   'left' : '25%',
									   'top' : '5'}
						),
						html.H5(id='selected-comments',
								className='column',
								style={'position': 'relative',
									   'left' : '25%',
									   'top' : '5'}
						),
						html.H5(id='selected-engagement-rate',
								className='column',
								style={'position': 'relative',
									   'left' : '25%',
									   'top' : '5'}
						),
						html.H5(id='selected-engagement-ratio',
								className='column',
								style={'position': 'relative',
									   'left' : '25%',
									   'top' : '5'}
						)
					],style={'width': '25%', 'display': 'inline-block','position': 'relative'}
					)
				]),
				html.Div([
					html.Div([
						html.H6('', className = "gs-header gs-text-header padded")
						],
						style={'width': '100%', 'display': 'inline-block','margin-top' : '45'}
					)
				])
			])


@app.callback(
    Output('country-selection', 'options'),
    [dash.dependencies.Input('campaign-selection', 'value')])
def populate_country_selection(campaign_selection):
	country_list = ["All"]
	for campaign in campaign_selection:
		campaign_df = df[df['CAMPAIGN'] == campaign]
		campaign_country_list = campaign_df['COUNTRY'].unique()
		country_list.extend([i for i in campaign_country_list])
	return [{'label': i, 'value': i} for i in country_list]

'''*****************************************************************************************
Selected Post functions
*******************************************************************************************'''
@app.callback(
    Output('selected-post-image', 'src'),
    [Input('main-graph', 'clickData'),
    dash.dependencies.Input('campaign-selection', 'value'),
     dash.dependencies.Input('country-selection', 'value')])
def display_selected_post_image(clickData,
				 				campaign_selection,
				 				country_selection):
	if clickData:
		try:
			post_id = clickData["points"][0]["customdata"]
		except KeyError:
			return None
		if country_selection == 'All':
			df_country = df
		else:
			df_country = df[df['COUNTRY'] == country_selection]
		if campaign_selection:
			df_campaigns = [df_country[df_country['CAMPAIGN'] == i] for i in campaign_selection]
			for df_campaign in df_campaigns:
				if post_id in df_campaign['POST ID'].values:
					return df_campaign[df_campaign['POST ID'] == post_id]["IMAGE"].unique()
	return None

@app.callback(
	Output('selected-ig-handle', 'children'),
	[Input('main-graph', 'clickData'),
	dash.dependencies.Input('campaign-selection', 'value'),
	dash.dependencies.Input('country-selection', 'value')])
def display_selected_ig_handle(clickData,
				 				campaign_selection,
				 				country_selection):
	if clickData:
		try:
			post_id = clickData["points"][0]["customdata"]
		except KeyError:
			return None
		if country_selection == 'All':
			df_country = df
		else:
			df_country = df[df['COUNTRY'] == country_selection]
		if campaign_selection:
			df_campaigns = [df_country[df_country['CAMPAIGN'] == i] for i in campaign_selection]
			for df_campaign in df_campaigns:
				if post_id in df_campaign['POST ID'].values:
					return df_campaign[df_campaign['POST ID'] == post_id]["IG HANDLE"]
	return None

@app.callback(
    Output('selected-ig-handle-hyperlink', 'href'),
    [Input('main-graph', 'clickData'),
    dash.dependencies.Input('campaign-selection', 'value'),
     dash.dependencies.Input('country-selection', 'value')])
def display_selected_ig_handle_hyperlink(clickData,
				 				campaign_selection,
				 				country_selection):
	if clickData:
		try:
			post_id = clickData["points"][0]["customdata"]
		except KeyError:
			return None
		if country_selection == 'All':
			df_country = df
		else:
			df_country = df[df['COUNTRY'] == country_selection]
		if campaign_selection:
			df_campaigns = [df_country[df_country['CAMPAIGN'] == i] for i in campaign_selection]
			for df_campaign in df_campaigns:
				if post_id in df_campaign['POST ID'].values:
					return "https://www.instagram.com/" + df_campaign[df_campaign['POST ID'] == post_id]["IG HANDLE"]
	return None

@app.callback(
    Output('selected-likes', 'children'),
    [Input('main-graph', 'clickData'),
     dash.dependencies.Input('campaign-selection', 'value'),
     dash.dependencies.Input('country-selection', 'value')])
def display_selected_likes(clickData,
				 				campaign_selection,
				 				country_selection):
	if clickData:
		try:
			post_id = clickData["points"][0]["customdata"]
		except KeyError:
			return None
		if country_selection == 'All':
			df_country = df
		else:
			df_country = df[df['COUNTRY'] == country_selection]
		if campaign_selection:
			df_campaigns = [df_country[df_country['CAMPAIGN'] == i] for i in campaign_selection]
			for df_campaign in df_campaigns:
				if post_id in df_campaign['POST ID'].values:
					return "{:,}".format(df_campaign[df_campaign['POST ID'] == post_id]["LIKES"].values[0]) + " Likes"
	return None


@app.callback(
    Output('selected-comments', 'children'),
    [Input('main-graph', 'clickData'),
    dash.dependencies.Input('campaign-selection', 'value'),
     dash.dependencies.Input('country-selection', 'value')])
def display_selected_comments(clickData,
				 				campaign_selection,
				 				country_selection):
	if clickData:
		try:
			post_id = clickData["points"][0]["customdata"]
		except KeyError:
			return None
		if country_selection == 'All':
			df_country = df
		else:
			df_country = df[df['COUNTRY'] == country_selection]
		if campaign_selection:
			df_campaigns = [df_country[df_country['CAMPAIGN'] == i] for i in campaign_selection]
			for df_campaign in df_campaigns:
				if post_id in df_campaign['POST ID'].values:
					return "{:,}".format(df_campaign[df_campaign['POST ID'] == post_id]["COMMENTS"].values[0]) + " Comments"
	return None

@app.callback(
    Output('selected-engagement-rate', 'children'),
    [Input('main-graph', 'clickData'),
    dash.dependencies.Input('campaign-selection', 'value'),
     dash.dependencies.Input('country-selection', 'value')])
def display_selected_engagement_rate(clickData,
				 				campaign_selection,
				 				country_selection):
	if clickData:
		try:
			post_id = clickData["points"][0]["customdata"]
		except KeyError:
			return None
		if country_selection == 'All':
			df_country = df
		else:
			df_country = df[df['COUNTRY'] == country_selection]
		if campaign_selection:
			df_campaigns = [df_country[df_country['CAMPAIGN'] == i] for i in campaign_selection]
			for df_campaign in df_campaigns:
				if post_id in df_campaign['POST ID'].values:
					return "{:.2f}".format(df_campaign[df_campaign['POST ID'] == post_id]["ENGAGEMENT RATE"].values[0]) + "% Eng. Rate"
	return None

@app.callback(
    Output('selected-engagement-ratio', 'children'),
    [Input('main-graph', 'clickData'),
    dash.dependencies.Input('campaign-selection', 'value'),
     dash.dependencies.Input('country-selection', 'value')])
def display_selected_engagement_ratio(clickData,
				 				campaign_selection,
				 				country_selection):
	if clickData:
		try:
			post_id = clickData["points"][0]["customdata"]
		except KeyError:
			return None
		if country_selection == 'All':
			df_country = df
		else:
			df_country = df[df['COUNTRY'] == country_selection]
		if campaign_selection:
			df_campaigns = [df_country[df_country['CAMPAIGN'] == i] for i in campaign_selection]
			for df_campaign in df_campaigns:
				if post_id in df_campaign['POST ID'].values:
					return "{:.2f}".format(df_campaign[df_campaign['POST ID'] == post_id]["ENGAGEMENT RATIO"].values[0]) + " Eng. Ratio"
	return None

@app.callback(
    Output('selected-post-hyperlink', 'href'),
    [Input('main-graph', 'clickData'),
    dash.dependencies.Input('campaign-selection', 'value'),
     dash.dependencies.Input('country-selection', 'value')])
def display_selected_post_hyperlink(clickData,
					 				campaign_selection,
				 				country_selection):
	if clickData:
		try:
			post_id = clickData["points"][0]["customdata"]
		except KeyError:
			return None
		if country_selection == 'All':
			df_country = df
		else:
			df_country = df[df['COUNTRY'] == country_selection]
		if campaign_selection:
			df_campaigns = [df_country[df_country['CAMPAIGN'] == i] for i in campaign_selection]
			for df_campaign in df_campaigns:
				if post_id in df_campaign['POST ID'].values:
					return None
	return None

'''*****************************************************************************************
Graph functions
*******************************************************************************************'''

@app.callback(
	dash.dependencies.Output('main-graph', 'figure'),
	[dash.dependencies.Input('yaxis-column', 'value'),
	 dash.dependencies.Input('campaign-selection', 'value'),
	 dash.dependencies.Input('country-selection', 'value'),
	 Input('main-graph', 'clickData')])
def update_graph(yaxis_column_name,
				 campaign_selection,
				 country_selection,
				 clickData):

	if country_selection == 'All':
		df_country = df
	else:
		df_country = df[df['COUNTRY'] == country_selection]

	if campaign_selection:
		if clickData:
			try:
				post_id = clickData["points"][0]["customdata"]
			except KeyError:
				post_id = None
		else:
			post_id = None

		df_campaigns = []
		for campaign in campaign_selection:
			df_campaigns.append(df_country[df_country['CAMPAIGN'] == campaign])

		df_post = pd.DataFrame()
		for df_campaign in df_campaigns:
			if post_id in df_campaign['POST ID'].values:
				df_post = df_campaign[df_campaign['POST ID'] == post_id]
				break

		max_y = 0.0
		min_y = 100000000000000000.0

		data = []
		colour_count = 0
		for df_campaign in df_campaigns:
			data.append(go.Scatter( x=df_campaign["DATE POSTED"],
									y=df_campaign[yaxis_column_name],
									customdata = df_campaign["POST ID"],
									mode='markers',
									name=campaign_selection[colour_count],
									marker=dict(
										color=colour_dict[campaign_selection[colour_count]],
									),
									text=df_campaign['IG HANDLE'],
									opacity=0.6
								))
			try:
				max_x = max(df_campaign["DATE POSTED"])
				min_x = min(df_campaign["DATE POSTED"])
				average = df_campaign[yaxis_column_name].mean()
				data.append(go.Scatter( x=[min_x,max_x],
										y=[average,average],
										mode='lines',
										name=campaign_selection[colour_count],
										marker=dict(
											color=colour_dict[campaign_selection[colour_count]],
										),
										opacity=0.6,
										showlegend=False
									))
				if df_campaign[yaxis_column_name].max() > max_y: max_y = df_campaign[yaxis_column_name].max()
				if df_campaign[yaxis_column_name].min() < min_y: min_y = df_campaign[yaxis_column_name].min()
			except ValueError:
				pass
			colour_count+=1

		y_axis_range = [0.0,1.1*max_y]

		if not df_post.empty:
			data.append(go.Scatter( x=df_post["DATE POSTED"],
									y=df_post[yaxis_column_name],
									customdata = df_post["POST ID"],
									mode='markers',
									name='Selected Post',
									marker=dict(color='rgb(0,0,0)'),
									opacity=1.0,
									showlegend=False))
		figure = {	'data': data,
					'layout': go.Layout(title='',
										showlegend=True,
										hovermode='closest',
										legend=dict(orientation="h",
													x=0,
													y=100),
										yaxis=dict(range=y_axis_range))
				 }
		return figure
	else:
		return None


if __name__ == '__main__':
    app.run_server(debug=True)
