import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import mysql.connector
import dash_table_experiments as dte

cnx = mysql.connector.connect(user='user', password='password',
                              host='cs336-nz132.cgwqde3pqnzp.us-east-2.rds.amazonaws.com',
                              database='BarBeerDrinker')
cursor = cnx.cursor()

def cr_list(c):
    r=[]
    temp = list(c)
    for i in temp:
        if(len(i)>1):
            r.append(list(i))
        else:
            r.append(i[0])
    return r

def get_options(tab):
	#print(tab)
	if(tab == 'drinker'):
		query = "select drinker_id from drinker"
	elif (tab == 'bar'):
		query = "select bar_id from bar"
	elif (tab == 'beer'):
		query = "select item_id from beer"	
	cursor.execute(query)
	temp = cr_list(cursor)
	
	optionlist = [{'label':i,'value':i} for i in temp]
	return optionlist
	
def generate_tab(tab):
	opt = get_options(tab)
	if(tab=='drinker'):
		x =  [html.Br(),html.Div(style={'display': 'block','margin-left': 'auto','margin-right': 'auto','width':'40%'},children=[
        html.Div(style={'width':'30%'} ,children=[
            html.Label(style={'font':'20px Britannic, serif'},children='Select a drinker:')
        ], className="six columns"),
		html.Div(style={'width':'65%'} ,children=[
           html.Div(style={'width':'100%'},children=dcc.Dropdown(
			#style={'font':'25px'}
			id='drinker_drop',
			options=opt,
			value =1
		))    
        ], className="six columns"),
    ], className="row"),html.Hr(),
		html.Div(style={},id = 'd_info')]
		
	elif (tab == "bar"):
		x = [html.Br(),html.Div(style={'display': 'block','margin-left': 'auto','margin-right': 'auto','width':'40%'},children=[
        html.Div(style={'width':'30%'} ,children=[
            html.Label(style={'font':'20px Britannic, serif'},children='Select a bar:')
        ], className="six columns"),
		html.Div(style={'width':'65%'} ,children=[
           html.Div(style={'width':'100%'},children=dcc.Dropdown(
			#style={'font':'25px'}
			id='bar_drop',
			options=opt,
			value =1
		))    
        ], className="six columns"),
    ], className="row"),html.Hr(),
		html.Div(style={},id = 'b_info')]
	elif (tab == "beer"):
		x = "Beer"
	else:
		x = "SQL"
	return x

def generate_drinker(d):
	query = "select * from drinker where drinker_id = "+str(d)
	cursor.execute(query)
	temp = cr_list(cursor)
	#print(temp)
	query = "select item_id,quantity from  tran_details where transaction_id in (select transaction_id from transaction where drinker_id = "+str(d)+") and item_id in (select item_id from beer)"
	cursor.execute(query)
	temp_g = cr_list(cursor)
	beer_g = []
	fre_g = []
	
	for i in range(len(temp_g)):
		if(temp_g[i][0] not in beer_g):
			beer_g.append(temp_g[i][0])
			fre_g.append(temp_g[i][1])
		else:
			ind = beer_g.index(temp_g[i][0])
			fre_g[ind] += temp_g[i][1]
	
	beer_g_1 = []
			
	for i in beer_g:
		query = "select item_name from item where item_id="+str(i)
		cursor.execute(query)
		temp_b_n = cr_list(cursor)
		beer_g_1.append(temp_b_n[0])
	#print(beer_g)
	#print(temp_b_n)
	
	query = "select transaction_id,bar_id,time,total from transaction where drinker_id="+str(d)
	cursor.execute(query)
	temp_transaction = cr_list(cursor)
	temp_tid = []
	temp_bid=[]
	temp_time=[]
	temp_total = []
	for i in temp_transaction:
		temp_tid.append(i[0])
		query = "select name from bar where bar_id="+str(i[1])
		cursor.execute(query)
		temp_bar_n = cr_list(cursor)
		#beer_g_1.append(temp_b_n[0])
		temp_bid.append(temp_bar_n[0])
		temp_time.append(i[2])
		temp_total.append(i[3])
	print(temp_tid)
	temp_tran = pd.DataFrame({'transaction_id':temp_tid})
	temp_tran['Bar']=temp_bid
	temp_tran['time']=temp_time
	temp_tran['Total']=temp_total
	
	
	#val = [1,2,3,4,5,6,7,8]
	x = [html.Div(children=[
        html.Div(style={'width':'27%'} ,children=[
            html.H4(style={'font-weight':'bold'},children='Drinker Info'),
            html.Div(style={'font-size':'15px',},id='drinker_information',children =[
			html.Table([
			html.Tr( [html.Td(children = "Drinker ID"),html.Td(children = ":"),html.Td(children = temp[0][0])]),
			html.Tr( [html.Td(children = "Name"),html.Td(children = ":"),html.Td(children = temp[0][1])]),
			html.Tr( [html.Td(children = "City"),html.Td(children = ":"),html.Td(children = temp[0][2])]),
			html.Tr( [html.Td(children = "Contact"),html.Td(children = ":"),html.Td(children = temp[0][3])]),
			html.Tr( [html.Td(children = "Address"),html.Td(children = ":"),html.Td(children = temp[0][4])]),
			])
			])
        ], className="six columns"),
		html.Div(style={'width':'67%'} ,children=[
            html.H4(style={'font-weight':'bold'},children='Most ordered Beers'),
            dcc.Graph(
				id='mo_beer',
				figure={
					'data': [
						{'x': beer_g_1, 'y': fre_g , 'type': 'bar'},
					],
					'layout': {
						#'title': "Max bought beers",
						#'xaxis' : {'title':'Beers'},
						'yaxis' : {'title':'Frequency'},
					}
				}
			)
        ], className="six columns"),
    ], className="row"),html.Hr(),
	html.Div([
    		html.Div(style={},children = [
			html.H4(style={'font-weight':'bold'},children='Transactions'),
			dte.DataTable(
			rows=temp_tran.to_dict('records'),

			filterable=True,
			sortable=True,
			id='transactions'
		),
		
		],className="six columns"),
		html.Div([html.H4(style={'font-weight':'bold'},children='Spending Graph'),
		dcc.Graph(
			id='graph_spend',
				figure={
					'data': [
						{'x': temp_time, 'y': temp_total , 'type': 'bar'},
					],
					'layout': {
						#'title': "Max bought beers",
						'xaxis' : {'title':'Time'},
						'yaxis' : {'title':'Spending'},
					}
				}
		)],className="six columns"),
	], className="row"),
	
	] 
	return x
	
def generate_beer(b):
	query = "select bar_id,name,addr,city,phone,cast(open_hours as time),cast(close_hours as time) from bar where bar_id="+str(b)
	cursor.execute(query)
	temp = cr_list(cursor)
	#print(temp)
	
	query = "select hour(time) as t, count(1), sum(total) from transaction where bar_id = "+ str(b) +" group by t order by t"
	cursor.execute(query)
	temp_td = cr_list(cursor)
	temp_t=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
	temp_c=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	temp_tot = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	for i in temp_td:
		temp_c[i[0]] = i[1]
		temp_tot[i[0]] = i[2]
	s_c = sum(temp_c)
	s_tot = sum(temp_tot)
	for i in range(24):
		temp_c[i] = (temp_c[i]/s_c)*100
		temp_tot[i] = (temp_tot[i]/s_tot)*100
		
	
	val = [1,2,3,4,5,6,7,8]	
	x = [html.Div(children=[
        html.Div(style={'width':'27%'} ,children=[
            html.H4(style={'font-weight':'bold'},children='Bar Info'),
            html.Div(style={'font-size':'15px',},id='bar_information',children =[
			html.Table([
			html.Tr( [html.Td(children = "Bar ID"),html.Td(children = ":"),html.Td(children = temp[0][0])]),
			html.Tr( [html.Td(children = "Name"),html.Td(children = ":"),html.Td(children = temp[0][1])]),
			html.Tr( [html.Td(children = "Address"),html.Td(children = ":"),html.Td(children = temp[0][2]+", "+temp[0][3])]),
			html.Tr( [html.Td(children = "Phone"),html.Td(children = ":"),html.Td(children = temp[0][4])]),
			html.Tr( [html.Td(children = "Hours"),html.Td(children = ":"),html.Td(children = str(temp[0][5])+" to "+str(temp[0][6]))]),
			])
			])
        ], className="six columns"),
		html.Div(style={'width':'67%'} ,children=[
            html.H4(style={'font-weight':'bold'},children='Time distribution of sales'),
            dcc.Graph(
				id='td_bar',
				figure={
					'data': [
						{'x': temp_t, 'y': temp_c , 'name': 'People','type': 'line'},
						{'x': temp_t, 'y': temp_tot , 'name': 'Income', 'type': 'line'},
					],
					'layout': {
						#'title': "Max bought beers",
						'xaxis' : {'title':'Time'},
						#'yaxis' : {'title':'Frequency'},
					}
				}
			)
        ], className="six columns"),
    ], className="row"),html.Hr()
	
	]
	return x
	
#initialize application
app = dash.Dash()
server = app.server
app.config['suppress_callback_exceptions']=True

#application layout
app.layout = html.Div(style={'backgroundImage':'url("http://www.designbolts.com/wp-content/uploads/2013/02/Golf-Shirt-Grey-Seamless-Pattern-For-Website-Background.jpg")','borderRadius':'10px','min-height':'95vh'},children=[

	dcc.Tabs(
			id='tab',
			tabs=[{'label':'Drinker', 'value':'drinker'},{'label':'Bar', 'value':'bar'},{'label':'Beer', 'value':'beer'},{'label':'SQL Query Inerface', 'value':'sql'}],
			value = 'drinker',
			), 
	html.Div(style={'width':'100%'} , id='output'),
    html.Div(dte.DataTable(rows=[{}]), style={'display': 'none'})

])

#callback for tabs 
@app.callback(
    dash.dependencies.Output('output', 'children'),
    [dash.dependencies.Input('tab', 'value')])
	
def update_output(value):
	s = '{}'.format(value)
	#print(s)
	return generate_tab(s)

#callback for drinker dropdown
@app.callback(
    dash.dependencies.Output('d_info', 'children'),
    [dash.dependencies.Input('drinker_drop', 'value')])
	
def update_output(value):
	s = '{}'.format(value)
	#print(s)
	return generate_drinker(s)
	
#callback for bar dropdown
@app.callback(
    dash.dependencies.Output('b_info', 'children'),
    [dash.dependencies.Input('bar_drop', 'value')])
	
def update_output(value):
	s = '{}'.format(value)
	#print(s)
	return generate_beer(s)

# Loading screen CSS
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/brPBPO.css"})
	
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})
	
if __name__ == '__main__':
    app.run_server(debug=True)
