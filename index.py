import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import mysql.connector
import dash_table_experiments as dte
import sys
import datetime
from datetime import datetime as dt

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
	else: return []
	cursor.execute(query)
	temp = cr_list(cursor)
	
	optionlist = [{'label':i,'value':i} for i in temp]
	return optionlist
	
def generate_tab(tab):
	opt = get_options(tab)
	if(tab=='drinker'):
		x =  [html.Div(style={'backgroundImage':'url("http://insightcounselingllc.com/wp-content/uploads/2015/09/bigstock-Group-of-young-multi-ethnic-fr-65952550.jpg")','height':'700px','width':'100%'}),
		html.Hr(),html.Br(),html.Div(style={'display': 'block','margin-left': 'auto','margin-right': 'auto','width':'40%'},children=[
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
		x = [html.Div(style={'backgroundImage':'url("https://res.cloudinary.com/stephens-media/image/upload/v1533067330/RJ/manual/nflbarstv_loop.gif")','height':'700px','width':'100%'}),
		html.Hr(),html.Br(),html.Div(style={'display': 'block','margin-left': 'auto','margin-right': 'auto','width':'40%'},children=[
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
		x = [html.Div(style={'backgroundImage':'url("https://stmed.net/sites/default/files/styles/1440x900/public/beer-wallpapers-28209-1852976.jpg?itok=zWcb4G9k")','height':'700px','width':'100%'}),
		html.Hr(),html.Br(),html.Div(style={'display': 'block','margin-left': 'auto','margin-right': 'auto','width':'40%'},children=[
        html.Div(style={'width':'30%'} ,children=[
            html.Label(style={'font':'20px Britannic, serif'},children='Select a beer:')
        ], className="six columns"),
		html.Div(style={'width':'65%'} ,children=[
           html.Div(style={'width':'100%'},children=dcc.Dropdown(
			#style={'font':'25px'}
			id='beer_drop',
			options=opt,
			value =4
		))    
        ], className="six columns"),
    ], className="row"),html.Hr(),
		html.Div(style={},id = 'beer_info')]
	elif(tab == "modify"):
		x = [html.H4(style={'font-weight':'bold'},children='Bar/Drinker/Item queries. Constraints checked: Primary key'),dcc.Textarea(
		id='bar_q',
		placeholder='Enter a correctly formatted query for bar table...Note that bar_id,drinker_id and item_id are auto generated columns.',
		value='',
		style={'width': '100%'}
		), html.Button('Execute', id='bar_exe'),
		html.Div(id='bar_label',
             children='')
		]
	else:
		x = [html.H4(style={'font-weight':'bold'},children='Write select queries here:'),dcc.Textarea(
		id='select_q',
		placeholder='Enter query',
		value='',
		style={'width': '100%'}
		),html.Button('Execute', id='select_exe'),
		html.Div(id='select_label',
             children='')
		]
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
	#print(temp_tid)
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
	
def generate_bar(b):
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
	
	query = "select drinker_id from transaction where bar_id="+ str(b) +" group by drinker_id order by sum(total) desc limit 10;"
	cursor.execute(query)
	temp_g1_x = cr_list(cursor)
	temp_g1_x1=[]
	
	for i in temp_g1_x:
		query = "select drinker from drinker where drinker_id="+str(i)
		cursor.execute(query)
		temp_x = cr_list(cursor)
		temp_g1_x1.append(temp_x[0])
	
	query = "select sum(total) as s from transaction where bar_id="+ str(b) +" group by drinker_id order by s desc limit 10;"
	cursor.execute(query)
	temp_g1_y = cr_list(cursor)
	
	
	query = "select item_id from tran_details where transaction_id in (select transaction_id from transaction where bar_id="+ str(b) +") group by item_id order by sum(quantity) desc limit 10"
	cursor.execute(query)
	temp_g2_x = cr_list(cursor)
	temp_g2_x1=[]
	temp_g3_x=[]
	
	query = "select item_id from sells where bar_id="+str(b)
	cursor.execute(query)
	temp_at_items = cr_list(cursor)
	at_items_ol = [{'label':i,'value':i} for i in temp_at_items]
	
	
	for i in temp_g2_x:
		query = "select item_name from item where item_id="+str(i)
		cursor.execute(query)
		temp_x = cr_list(cursor)
		temp_g2_x1.append(temp_x[0])
		
		query = "select manufacturer from beer where item_id="+str(i)
		cursor.execute(query)
		temp_x = cr_list(cursor)
		if (len(temp_x)>0):
			temp_g3_x.append(temp_x[0])
		else:
			temp_g3_x.append("null")
	
	query = "select sum(quantity) from tran_details where transaction_id in (select transaction_id from transaction where bar_id="+ str(b) +") group by item_id order by sum(quantity) desc limit 10"
	cursor.execute(query)
	temp_g2_y = cr_list(cursor)
	temp_g3_y = []
	temp_g3_x1= []
	i=0;
	for i in range(len(temp_g3_x)):
		if(temp_g3_x[i]=="null"):
			pass
		else:
			temp_g3_x1.append(temp_g3_x[i])
			temp_g3_y.append(temp_g2_y[i])
			i=i+1
	
	#print(temp_g3_x1)
	#print(temp_g3_y)
	
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
    ], className="row"),html.Hr(),
	#graphs 1,2
	html.Div(children=[
        html.Div(style={'width':'47%'} ,children=[
            html.H4(style={'font-weight':'bold'},children='Top Drinkers'),
            html.Div(style={'font-size':'15px',},id='bar_g1_div',children =[
			dcc.Graph(
			id='bar_g1',
				figure={
					'data': [
						{'x': temp_g1_x1, 'y': temp_g1_y , 'type': 'bar'},
					],
					'layout': {
						#'title': "Max bought beers",
						'xaxis' : {'title':'Drinker'},
						'yaxis' : {'title':'Spending'},
					}
				}
			)
			])
        ], className="six columns"),
		html.Div(style={'width':'47%'} ,children=[
            html.H4(style={'font-weight':'bold'},children='Popular Items'),
            html.Div(style={'font-size':'15px',},id='bar_g2_div',children =[
			dcc.Graph(
			id='bar_g2',
				figure={
					'data': [
						{'x': temp_g2_x1, 'y': temp_g2_y , 'type': 'bar'},
					],
					'layout': {
						#'title': "Max bought beers",
						'xaxis' : {'title':'Items'},
						'yaxis' : {'title':'Sales'},
					}
				}
			)
			])
        ], className="six columns"),
    ], className="row"),html.Hr(),
	
	#graphs 3,4
	html.Div(children=[
        html.Div(style={'width':'47%'} ,children=[
            html.H4(style={'font-weight':'bold'},children='Top Manufacturers'),
            html.Div(style={'font-size':'15px',},id='bar_g3_div',children =[
			dcc.Graph(
			id='bar_g3',
				figure={
					'data': [
						{'x': temp_g3_x1, 'y': temp_g3_y , 'type': 'bar'},
					],
					'layout': {
						#'title': "Max bought beers",
						'xaxis' : {'title':'Manufacturer'},
						'yaxis' : {'title':'Sales'},
					}
				}
			)
			])
        ], className="six columns"),
		html.Div(style={'width':'47%'} ,children=[
            html.H4(style={'font-weight':'bold'},children='Add transaction'),
            html.Div(style={'font-size':'15px',},id='bar_g2_div',children =[
			html.Table([
				html.Tr( [html.Td(children = "Drinker ID"),html.Td(children = ":"),html.Td(children=dcc.Dropdown(id='at_drinker',options=get_options('drinker')))]),
				html.Tr( [html.Td(children = "Item ID"),html.Td(children = ":"),html.Td(children=dcc.Dropdown(id='at_item',options=at_items_ol,multi=True))]),
				html.Tr( [html.Td(children = "Quantity"),html.Td(children = ":"),html.Td(children = dcc.Input(id= 'at_quantity' ,placeholder='Seperated by commas...',type='text'))]),
				html.Tr( [html.Td(children = "Tip"),html.Td(children = ":"),html.Td(children = dcc.Input(id= 'at_tip',placeholder='Enter tip...',type='text'))]),
				html.Tr( [html.Td(children = html.Button('Add', id='at_add') ),html.Td(children = " "),html.Td(children = " ")]),
				]),html.Div(id='at_out',children='')
			])
        ], className="six columns"),
    ], className="row"),html.Hr(),
	
	
	
	]
	return x
	
def generate_beer(b):
	query = "select item_name from item where item_id="+str(b)
	cursor.execute(query)
	temp_bn = cr_list(cursor)[0]
	
	query = "select manufacturer from beer where item_id="+str(b)
	cursor.execute(query)
	temp_mn = cr_list(cursor)[0]
	
	query = "select hour(time) as t, sum(quantity) from tran_details a join transaction b on a.transaction_id = b.transaction_id where item_id = "+ str(b) +" group by t"
	cursor.execute(query)
	temp_td = cr_list(cursor)
	temp_t=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
	temp_q=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	#temp_tot = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	for i in temp_td:
		temp_q[i[0]] = i[1]
		#temp_tot[i[0]] = i[2]
	s_c = sum(temp_q)
	#s_tot = sum(temp_tot)
	for i in range(24):
		temp_q[i] = (temp_q[i]/s_c)*100
		#temp_tot[i] = (temp_tot[i]/s_tot)*100

	query = "select bar_id from tran_details a join transaction b on a.transaction_id = b.transaction_id where item_id = "+ str(b) +" group by bar_id order by sum(quantity) desc limit 10"
	cursor.execute(query)
	temp_g1_x = cr_list(cursor)
	temp_g1_x1=[]
	
	for i in temp_g1_x:
		query = "select name from bar where bar_id="+str(i)
		cursor.execute(query)
		temp_x = cr_list(cursor)
		temp_g1_x1.append(temp_x[0])
	
	query = "select sum(quantity) from tran_details a join transaction b on a.transaction_id = b.transaction_id where item_id = "+ str(b) +" group by bar_id order by sum(quantity) desc limit 10"
	cursor.execute(query)
	temp_g1_y = cr_list(cursor)
	
	
	query = "select drinker_id from tran_details a join transaction b on a.transaction_id = b.transaction_id where item_id = "+ str(b) +" group by drinker_id order by sum(quantity) desc limit 10"
	cursor.execute(query)
	temp_g2_x = cr_list(cursor)
	temp_g2_x1=[]
	
	for i in temp_g2_x:
		query = "select drinker from drinker where drinker_id="+str(i)
		cursor.execute(query)
		temp_x = cr_list(cursor)
		temp_g2_x1.append(temp_x[0])
	
	query = "select sum(quantity) from tran_details a join transaction b on a.transaction_id = b.transaction_id where item_id = "+ str(b) +" group by drinker_id order by sum(quantity) desc limit 10"
	cursor.execute(query)
	temp_g2_y = cr_list(cursor)
	
		
	x=[html.Div(children=[
        html.Div(style={'width':'27%'} ,children=[
            html.H4(style={'font-weight':'bold'},children='Beer Info'),
            html.Div(style={'font-size':'15px',},id='beer_information',children =[
			html.Table([
			html.Tr( [html.Td(children = "Item ID"),html.Td(children = ":"),html.Td(children = b)]),
			html.Tr( [html.Td(children = "Name"),html.Td(children = ":"),html.Td(children = temp_bn)]),
			html.Tr( [html.Td(children = "Manufacturer"),html.Td(children = ":"),html.Td(children = temp_mn)]),
			])
			])
        ], className="six columns"),
		html.Div(style={'width':'67%'} ,children=[
            html.H4(style={'font-weight':'bold'},children='Time distribution of sales'),
            dcc.Graph(
				id='td_beer',
				figure={
					'data': [
						{'x': temp_t, 'y': temp_q , 'name': 'People','type': 'line'},
						#{'x': temp_t, 'y': temp_tot , 'name': 'Income', 'type': 'line'},
					],
					'layout': {
						#'title': "Max bought beers",
						'xaxis' : {'title':'Time'},
						'yaxis' : {'title':'Quantity sold'},
					}
				}
			)
        ], className="six columns"),
    ], className="row"),html.Hr(),
	#graphs 1,2
	html.Div(children=[
        html.Div(style={'width':'47%'} ,children=[
            html.H4(style={'font-weight':'bold'},children='Top Bars'),
            html.Div(style={'font-size':'15px',},id='bar_g1_div',children =[
			dcc.Graph(
			id='beer_g1',
				figure={
					'data': [
						{'x': temp_g1_x1, 'y': temp_g1_y , 'type': 'bar'},
					],
					'layout': {
						#'title': "Max bought beers",
						'xaxis' : {'title':'Bar'},
						'yaxis' : {'title':'Sales'},
					}
				}
			)
			])
        ], className="six columns"),
		html.Div(style={'width':'47%'} ,children=[
            html.H4(style={'font-weight':'bold'},children='Top Drinkers'),
            html.Div(style={'font-size':'15px',},id='bar_g2_div',children =[
			dcc.Graph(
			id='beer_g2',
				figure={
					'data': [
						{'x': temp_g2_x1, 'y': temp_g2_y , 'type': 'bar'},
					],
					'layout': {
						#'title': "Max bought beers",
						'xaxis' : {'title':'Drinkers'},
						'yaxis' : {'title':'Quantity bought'},
					}
				}
			)
			])
        ], className="six columns"),
    ], className="row"),html.Hr(),
	]
	return x

#initialize application
app = dash.Dash()
server = app.server
app.config['suppress_callback_exceptions']=True

#application layout
app.layout = html.Div(style={'backgroundImage':'url("https://blog.visme.co/wp-content/uploads/2017/07/50-Beautiful-and-Minimalist-Presentation-Backgrounds-047.jpg")','borderRadius':'10px','min-height':'95vh'},children=[

	dcc.Tabs(
			id='tab',
			tabs=[{'label':'Drinker', 'value':'drinker'},{'label':'Bar', 'value':'bar'},{'label':'Beer', 'value':'beer'},{'label':'SQL Query Inerface', 'value':'sql'},{'label':'Modification', 'value':'modify'}],
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
	return generate_bar(s)
	
#callback for beer dropdown
@app.callback(
    dash.dependencies.Output('beer_info', 'children'),
    [dash.dependencies.Input('beer_drop', 'value')])
	
def update_output(value):
	s = '{}'.format(value)
	#print(s)
	return generate_beer(s)

#button for bar/drinker/item execute
@app.callback(
	dash.dependencies.Output('bar_label', 'children'),
	[dash.dependencies.Input('bar_exe', 'n_clicks')],
	[dash.dependencies.State('bar_q', 'value')])

def update_output(n_clicks, value):
	query = '{}'.format(value)
	
	if(query==""):
		return
	
	try:
		cursor.execute(query)
	except:
		err = str(sys.exc_info()[0]).split(".")[-1][:-2]
		return "Unexpected error: " + str(err)
		
	cnx.commit()
	#for i in cursor:
	if(cursor.rowcount>0):
		return "Successful." + str(cursor.rowcount) + " rows affected"
	elif(cursor.rowcount==-1):
		return
	else:
		return "0 rows affected"

#button for sql query interface
@app.callback(
	dash.dependencies.Output('select_label', 'children'),
	[dash.dependencies.Input('select_exe', 'n_clicks')],
	[dash.dependencies.State('select_q', 'value')])

def update_output(n_clicks, value):
	query = '{}'.format(value)
	
	if(query==""):
		return
	
	
	try:
		temp = pd.read_sql_query(query,cnx)
		
	except:
	#	err = str(sys.exc_info()[0]).split(".")[-1][:-2]
		return "Unexpected error. Verify syntax."
		
	#cnx.commit()
	#for i in cursor:
	'''
	if(cursor.rowcount>0):
		return "Successful." + str(cursor.rowcount) + " rows affected"
	elif(cursor.rowcount==-1):
		return
	else:
		return "0 rows affected"
	'''
	x = [dte.DataTable(
			rows=temp.to_dict('records'),
			filterable=True,
			sortable=True,
			id='transactions')]
	
	return x

#button for adding transaction in bar page
@app.callback(
	dash.dependencies.Output('at_out', 'children'),
	[dash.dependencies.Input('at_add', 'n_clicks')],
	[dash.dependencies.State('bar_drop', 'value'),
	dash.dependencies.State('at_drinker', 'value'),
	dash.dependencies.State('at_item', 'value'),
	dash.dependencies.State('at_quantity', 'value'),
	dash.dependencies.State('at_tip', 'value')
	])

def update_output(n_clicks, input1, input2, input3, input4, input5):
	r = ""
	n = '{}'.format(n_clicks)
	b1 = '{}'.format(input1)
	d1 = '{}'.format(input2)
	items = '{}'.format(input3)
	quan = ('{}'.format(input4)).split(',')
	tip = '{}'.format(input5)
	
	#print(len(items))
	#print(items)
	if(items=="None"):
		return r
	items = items.replace('[','').replace(']','').split(',')
	#print(b1)
	#print(d1)
	#print(items)
	#print(quan)
	#print(tip)
	
	query = "select max(transaction_id) from transaction"
	cursor.execute(query)
	t_id = (cr_list(cursor)[0])+1
	#print(t_id)
	
	cursor.execute("select open_hours,close_hours from bar where bar_id ="+str(b1))
	b_times = cr_list(cursor)
	s = b_times[0][0].seconds
	e = b_times[0][1].seconds
	
	#print(s)
	#print(e)
	
	x1 = datetime.datetime.now()
	date = dt.strftime(x1, '%Y-%m-%d %H:%M')
	t_s = datetime.timedelta(hours=x1.hour,minutes=x1.minute,seconds=x1.second).total_seconds()
	#print(t_s)
	
	if(t_s>=s or t_s<=e): #time constraint
		#print("after time constraint")
		cost=[]
		j=0
        
		#cursor.execute("select item_id from sells where bar_id="+str(b1))
		#item1 = cr_list(cursor)
        
		while(j<len(items)):  #loop for tran_details
			#print("inside j while")
			#i = random.randint(0,len(item1)-1)
			
			try: #bar sells item? item already in transaction: primary key.
				i1=int(items[j])
				#print(i1)
				quantity = int(quan[j])
				#print(quantity)
				cursor.execute("select price from sells where bar_id = "+ str(b1) +" and item_id="+str(i1))
				i_price = cr_list(cursor)[0]
				cursor.execute("insert into tran_details values("+ str(t_id) +","+ str(i1) +","+ str(quantity) +")")
				j=j+1
				cost.append(i_price*quantity)
				#print("tran_details")
			except:
				r = "Unexpected error. Please try again."
				return r
		fin_cost = round(sum(cost),2)
		#print(fin_cost)
		tax = round(fin_cost*0.07,2)
		total = fin_cost+tax+float(tip)
		cursor.execute("insert into transaction values("+ str(t_id) +","+str(b1)+","+str(d1)+",'"+date+"',"+str(tip)+","+str(tax)+","+str(total)+","+str(fin_cost)+")")
		#print("transaction "+ str(t_id))
		#t_id = t_id+1
		r = "Transaction added with transaction_id: "+str(t_id)
		cnx.commit()
	else:
		r = "The bar is closed. Please come later..."
	
	
	return r
	
#callback for clearing drinking dropdown in add transaction
@app.callback(
    dash.dependencies.Output('at_drinker', 'value'),
    [dash.dependencies.Input('at_add', 'n_clicks')])
	
def update_output(value):
	return ""
	
#callback for clearing item dropdown in add transaction
@app.callback(
    dash.dependencies.Output('at_item', 'value'),
    [dash.dependencies.Input('at_add', 'n_clicks')])
	
def update_output(value):
	return ""
	
#callback for clearing quantity in add transaction
@app.callback(
    dash.dependencies.Output('at_quantity', 'value'),
    [dash.dependencies.Input('at_add', 'n_clicks')])
	
def update_output(value):
	return ""
	
#callback for clearing tip in add transaction
@app.callback(
    dash.dependencies.Output('at_tip', 'value'),
    [dash.dependencies.Input('at_add', 'n_clicks')])
	
def update_output(value):
	return ""
	
# Loading screen CSS
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/brPBPO.css"})
	
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})
	
if __name__ == '__main__':
    app.run_server(debug=True)
