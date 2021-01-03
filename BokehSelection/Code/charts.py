
from bokeh.plotting import figure, output_file, show
from bokeh.models import Span
from bokeh.models import HoverTool,ColumnDataSource
from bokeh.models import Title
import pandas as pd
import datetime
import sys
import numpy as np
import sqlite3
import csv
import os
import holidays
from py_vollib.black.implied_volatility import implied_volatility
from py_vollib.black.greeks.numerical import delta, gamma
pd.options.display.float_format = '{:.2f}'.format 
def blackIV(df, F=None, rf=None):
    if F is None: F = df['F']
    if rf is None: rf = .02
    try:
        iv = implied_volatility(discounted_option_price=df['Mid'], # change to 'Mid'
                                F=F,
                                K=df['Strike'],
                                r=rf,
                                t=df['BDTE']/252,
                                flag=df['Flag'])
    except:
        iv = np.nan
    return iv
def blackDelta(df, F=None, rf=None):
    if F is None: F = df['F']
    if rf is None: rf = .02
    try:
        delt = delta(flag=df['Flag'],
                     F=F,
                     K=df['Strike'],
                     t=df['BDTE']/252,
                     r=rf,
                     sigma=df['IV'])
    except:
        delt = np.nan
    return delt
def blackGamma(df, F=None, rf=None):
    if F is None: F = df['F']
    if rf is None: rf = .02
    try:
        gam = gamma(flag=df['Flag'],
                    F=F,
                    K=df['Strike'],
                    t=df['BDTE']/252,
                    r=rf,
                    sigma=df['IV'])
    except:
        gam = np.nan
    return gam
def GEX(filename):
    raw = pd.read_table(filename)
    spotF = float(raw.columns[0].split(',')[-2]) 
    ticker = raw.columns[0].split(',')[0][1:4] 
    rf = .02
    pltDate = raw.loc[0][0].split(',')[0][:11] 
    pltTime = raw.loc[0][0].split(',')[0][-8:] 
    dtDate = datetime.datetime.strptime(pltDate, '%b %d %Y').date()

    # Extract dataframe for analysis
    raw = pd.read_table(filename, sep=',', header=2)
    c = raw.loc[:, :'Strike'].copy(deep=True)
    c.columns = c.columns.str.replace('Calls', 'ID')
    p = (raw.loc[:, 'Strike':].join(raw.loc[:, 'Expiration Date']))\
                              .copy(deep=True)
                              
    p.columns = p.columns.str.replace('Puts', 'ID')
    p.columns = p.columns.str.replace('.1', '')
    p = p[c.columns]

    c['Flag'] = 'c'
    p['Flag'] = 'p'
    
    c['Expiry'] = pd.to_datetime(c['Expiration Date'],
                                 infer_datetime_format=True)
    p['Expiry'] = pd.to_datetime(p['Expiration Date'],
                                 infer_datetime_format=True)
   
    df = c.append(p, ignore_index=True)
    
    df = df[(df['ID'].str[-3] != '-') &\
            (df['ID'].str[-4] != '-')
            ].copy(deep=True)

    for item in ['Bid', 'Ask', 'Last Sale', 'IV', 'Delta',
                 'Gamma', 'Open Int', 'Strike']:
        df[item] = pd.to_numeric(df[item], errors='coerce')

    us_holidays = holidays.UnitedStates(years=list(range(2000, 2030)))
    us_hlist = list(us_holidays.keys())

    A = [d.date() for d in df['Expiry']]
    df['BDTE'] = np.busday_count(dtDate, A, weekmask='1111100',
                                  holidays=us_hlist)

    df = df.loc[(df['Open Int'] > 10) &\
                (df['Bid'] > .05) &\
                (df['BDTE'] >= 1) #&\
                ].copy(deep=True)
    
    
    df['Mid'] = np.mean(df[['Bid', 'Ask']], axis=1)
    
    df['IV'] = df.apply(lambda x: blackIV(x, F=spotF, rf=rf), axis=1)
    df = df[(df['IV'] > .01) & (df['IV'] < 2.)].copy(deep=True)
    
    df['Delta'] = df.apply(lambda x: blackDelta(x, F=spotF, rf=rf), axis=1)
    df = df[np.abs(df['Delta'])<.95].copy(deep=True)
    
    increment = 10 if ticker in ['SPX', 'NDX'] else 1
    nPoints = 20
    Fs = list((np.linspace(start=spotF, 
                           stop=spotF+increment*nPoints,
                           num=nPoints,
                           endpoint=False)-increment*nPoints//2).astype(int))

    for F in Fs:
        df[str(F)+'_g'] = df.apply(lambda x: blackGamma(x, F=F, rf=rf),
                                   axis=1)

    for F in Fs:
        df[str(F)+'_GEX'] = 10**-6*(100*F*(df['Flag']=='c')*df[str(F)+'_g']*df['Open Int']\
                                   -100*F*(df['Flag']=='p')*df[str(F)+'_g']*df['Open Int'])

    GEXs = [(0.1 if ticker not in ['SPX', 'NDX'] else 1)*np.sum(df[str(F)+'_GEX'], axis=0) for F in Fs]
    s = pd.Series(dict(zip(Fs, GEXs))).astype(int)
    zeroGEX = int(np.interp(x=0, xp=s.values, fp=s.index))
    
    return s,df,zeroGEX
def blackGexFull(filename):
    raw = pd.read_table(filename)
    spotF = float(raw.columns[0].split(',')[-2]) 
    ticker = raw.columns[0].split(',')[0][1:4] 
    rf = .02
    pltDate = raw.loc[0][0].split(',')[0][:11] 
    pltTime = raw.loc[0][0].split(',')[0][-8:] 
    dtDate = datetime.datetime.strptime(pltDate, '%b %d %Y').date()
    
    raw = pd.read_table(filename, sep=',', header=2)
    c = raw.loc[:, :'Strike'].copy(deep=True)
    c.columns = c.columns.str.replace('Calls', 'ID')
    p = (raw.loc[:, 'Strike':].join(raw.loc[:, 'Expiration Date']))\
                              .copy(deep=True)
                              
    p.columns = p.columns.str.replace('Puts', 'ID')
    p.columns = p.columns.str.replace('.1', '')
    p = p[c.columns]

    c['Flag'] = 'c'
    p['Flag'] = 'p'
    
    c['Expiry'] = pd.to_datetime(c['Expiration Date'],
                                 infer_datetime_format=True)
    p['Expiry'] = pd.to_datetime(p['Expiration Date'],
                                 infer_datetime_format=True)
    
    df = c.append(p, ignore_index=True)
        
     
    df = df[(df['ID'].str[-3] != '-') &\
            (df['ID'].str[-4] != '-')
            ].copy(deep=True)

    for item in ['Bid', 'Ask', 'Last Sale', 'IV', 'Delta',
                 'Gamma', 'Open Int', 'Strike']:
        df[item] = pd.to_numeric(df[item], errors='coerce')

    us_holidays = holidays.UnitedStates(years=list(range(2000, 2030)))
    us_hlist = list(us_holidays.keys())

    A = [d.date() for d in df['Expiry']]
    
    df['BDTE'] = np.busday_count(dtDate, A, weekmask='1111100',
                                 holidays=us_hlist)
    df = df.loc[
                (df['BDTE'] >= 1) #&\
                ].copy(deep=True)
   
    df['Mid'] = np.mean(df[['Bid', 'Ask']], axis=1)
    df['IV'] = df.apply(lambda x: blackIV(x, F=spotF, rf=rf), axis=1)
    
    df['Delta'] = df.apply(lambda x: blackDelta(x, F=spotF, rf=rf), axis=1)
    
    df['Gamma'] = df.apply(lambda x: blackGamma(x, F=spotF, rf=rf), axis=1)
    
    return df       
    
if len(sys.argv) != 4:
        sys.exit("Usage: python charts.py names of the files -today.csv -yesterday.csv period in days")

if not os.path.exists('Charts_html'):
    os.mkdir('Charts_html')
    folder='Charts_html'
else:
    folder='Charts_html'
    
with open(sys.argv[1]) as File:
    data=list(csv.reader(File))
price=float(data[0][1]) 

oi=pd.read_csv(sys.argv[1],skiprows=2,parse_dates=['Expiration Date'])
oi_Y=pd.read_csv(sys.argv[2],skiprows=2,parse_dates=['Expiration Date'])

us_holidays = holidays.UnitedStates(years=list(range(2000, 2030)))
us_hlist = list(us_holidays.keys())


oi2=oi.set_index('Expiration Date')
oi2_Y=oi_Y.set_index('Expiration Date')
date=pd.DataFrame()
date_Y=pd.DataFrame()
date['date'] = pd.date_range(oi['Expiration Date'][0], periods=int(sys.argv[3]), freq='D')
date_Y['date'] = pd.date_range(oi_Y['Expiration Date'][0], periods=int(sys.argv[3]), freq='D')
sql_date=date['date'][0]
df_dates = oi2[(oi2.index >= date['date'][0]) & (oi2.index <= date['date'][int(sys.argv[3])-1])]
# df_dates_Y = oi2_Y[(oi2_Y.index >= date_Y['date'][0]) & (oi2_Y.index <= date_Y['date'][int(sys.argv[3])-1])]
df1 = df_dates[(df_dates['Open Int'] > 10) &\
            (df_dates['Bid'] > .05) ]
print('Calculating data')
print()
x,df,zero_gex=GEX(sys.argv[1])[0],GEX(sys.argv[1])[1],GEX(sys.argv[1])[2]
df.to_csv('df.csv')
df_Y=GEX(sys.argv[2])[1]
df_full=blackGexFull(sys.argv[1])
df_full.to_csv('df_full.csv')
print('Done calculations')

'''
Open Interest graphs
'''
dates=df[(df['Expiry'] > date['date'][0]) & (df['Expiry'] < date['date'][int(sys.argv[3])-1])]

dates_Y=df_Y[(df_Y['Expiry'] > date['date'][0]) & (df_Y['Expiry'] < date['date'][int(sys.argv[3])-1])]

'''
Not grouped versions
'''

Puts=dates[dates['Flag']=='p']
Puts.to_csv('Puts.csv')
Calls=dates[dates['Flag']=='c']
Calls.to_csv('Calls.csv')
p_c_ratio=Puts['Vol'].sum()/Calls['Vol'].sum()
PutsY=dates_Y[dates_Y['Flag']=='p']
PutsY.to_csv('PutsY.csv')
CallsY=dates_Y[dates_Y['Flag']=='c']
CallsY.to_csv('CallsY.csv')

'''
Grouped versions
'''
Calls2=Calls.groupby(['Strike']).sum()
Calls2['Strike']=Calls2.index
Calls2.to_csv('Calls2.csv')
CallsY2=CallsY.groupby(['Strike']).sum()
CallsY2['Strike']=CallsY2.index
CallsY2.to_csv('CallsY2.csv')

Puts2=Puts.groupby(['Strike']).sum()
Puts2['Strike']=Puts2.index
Puts2.to_csv('Puts2.csv')
PutsY2=PutsY.groupby(['Strike']).sum()
PutsY2['Strike']=PutsY2.index
PutsY2.to_csv('PutsY2.csv')
'''
Plots simple
'''

output_file(f"{folder}/Current_Call-OIsimple_{sys.argv[3]}_days.html")
strikes=Calls['Strike'] 
op_int=Calls['Open Int']
source = ColumnDataSource(data=dict(x=strikes,y=op_int))
MyHover10 = HoverTool(
	tooltips=[
		( 'Strike', '@x'),
		( 'OI', '@y' ), 
       
	], point_policy="follow_mouse"	
)    
p = figure(title="Current Call Open Interest Simple SPX",tools=["pan,wheel_zoom,xwheel_zoom,ywheel_zoom,box_zoom,zoom_in, xzoom_in, yzoom_in,zoom_out, xzoom_out, yzoom_out,reset,save,lasso_select", MyHover10], x_axis_label='Strike Price', y_axis_label='OI',width=1200,height=600)
p.yaxis.formatter.use_scientific = False
MyHover10.formatters.use_scientific = False
p.vbar(source=source,x='x', width=0.5, bottom=0,
        top='y', color="firebrick")
show(p)


output_file(f"{folder}/Current_Put-OIsimple_{sys.argv[3]}_days.html")
strikes=Puts['Strike'] 
op_int=Puts['Open Int']
source = ColumnDataSource(data=dict(x=strikes,y=op_int))
MyHover11 = HoverTool(
	tooltips=[
		( 'Strike', '@x'),
		( 'OI', '@y' ), 
       
	], point_policy="follow_mouse"	
)    
p = figure(title="Current Put Open Interest Simple SPX",tools=["pan,wheel_zoom,xwheel_zoom,ywheel_zoom,box_zoom,zoom_in, xzoom_in, yzoom_in,zoom_out, xzoom_out, yzoom_out,reset,save,lasso_select", MyHover11], x_axis_label='Strike Price', y_axis_label='OI',width=1200,height=600)
p.yaxis.formatter.use_scientific = False
MyHover11.formatters.use_scientific = False
p.vbar(source=source,x='x', width=0.5, bottom=0,
        top='y', color="firebrick")
show(p)

output_file(f"{folder}/Yesterdays_Put-VolumeSimple_{sys.argv[3]}_days.html")
strikes=PutsY['Strike'] 
op_int=PutsY['Vol']
source = ColumnDataSource(data=dict(x=strikes,y=op_int))
MyHover12 = HoverTool(
	tooltips=[
		( 'Strike', '@x'),
		( 'Vol.', '@y' ), 
       
	], point_policy="follow_mouse"	
)    
p = figure(title="Current Put Volume Simple SPX",tools=["pan,wheel_zoom,xwheel_zoom,ywheel_zoom,box_zoom,zoom_in, xzoom_in, yzoom_in,zoom_out, xzoom_out, yzoom_out,reset,save,lasso_select", MyHover12], x_axis_label='Strike Price', y_axis_label='Volume',width=1200,height=600)
p.yaxis.formatter.use_scientific = False
MyHover12.formatters.use_scientific = False
p.vbar(source=source,x='x', width=0.5, bottom=0,
        top='y', color="firebrick")
show(p)

output_file(f"{folder}/Yesterdays_Call-VolumeSimple_{sys.argv[3]}_days.html")
strikes=CallsY['Strike'] 
op_int=CallsY['Vol']
source = ColumnDataSource(data=dict(x=strikes,y=op_int))
MyHover13 = HoverTool(
	tooltips=[
		( 'Strike', '@x'),
		( 'Vol.', '@y' ), 
       
	], point_policy="follow_mouse"	
)    
p = figure(title="Current Call Volume Simple SPX",tools=["pan,wheel_zoom,xwheel_zoom,ywheel_zoom,box_zoom,zoom_in, xzoom_in, yzoom_in,zoom_out, xzoom_out, yzoom_out,reset,save,lasso_select", MyHover13], x_axis_label='Strike Price', y_axis_label='Volume',width=1200,height=600)
p.yaxis.formatter.use_scientific = False
MyHover13.formatters.use_scientific = False
p.vbar(source=source,x='x',  width=0.5, bottom=0,
        top='y', color="firebrick")
show(p)

'''
Plots grouped
'''

output_file(f"{folder}/Current-OI-grouped_{sys.argv[3]}_days.html")
strikes=Calls2['Strike'] 
op_int=Calls2['Open Int']
source = ColumnDataSource(data=dict(x=strikes,y=op_int))
strikes_p=Puts2['Strike'] 
op_int_p=Puts2['Open Int']
source2 = ColumnDataSource(data=dict(x=strikes_p,y=op_int_p))
MyHover14 = HoverTool(
	tooltips=[
		( 'Strike', '@x'),
		( 'OI', '@y' ), 
       
	], point_policy="follow_mouse"	
)    
p = figure(title="Current Call/Put Open Interest Grouped SPX",tools=["pan,wheel_zoom,xwheel_zoom,ywheel_zoom,box_zoom,zoom_in, xzoom_in, yzoom_in,zoom_out, xzoom_out, yzoom_out,reset,save,lasso_select", MyHover14], x_axis_label='Strike Price', y_axis_label='OI',width=1200,height=600)
p.yaxis.formatter.use_scientific = False
MyHover14.formatters.use_scientific = False
p.vbar(source=source,x='x', width=1, bottom=0,
        top='y', color="firebrick")
p.vbar(source=source2,x='x', width=0.5, bottom=0,
        top='y', color="blue",fill_alpha=.5)
show(p)

output_file(f"{folder}/Current_Call-OIgrouped_{sys.argv[3]}_days.html")
strikes=Calls2['Strike'] 
op_int=Calls2['Open Int']
source = ColumnDataSource(data=dict(x=strikes,y=op_int))
MyHover14 = HoverTool(
	tooltips=[
		( 'Strike', '@x'),
		( 'OI', '@y' ), 
       
	], point_policy="follow_mouse"	
)    
p = figure(title="Current Call Open Interest Grouped SPX",tools=["pan,wheel_zoom,xwheel_zoom,ywheel_zoom,box_zoom,zoom_in, xzoom_in, yzoom_in,zoom_out, xzoom_out, yzoom_out,reset,save,lasso_select", MyHover14], x_axis_label='Strike Price', y_axis_label='OI',width=1200,height=600)
p.yaxis.formatter.use_scientific = False
MyHover14.formatters.use_scientific = False
p.vbar(source=source,x='x', width=0.5, bottom=0,
        top='y', color="firebrick")
show(p)

output_file(f"{folder}/Current_Put-OIgrouped_{sys.argv[3]}_days.html")
strikes=Puts2['Strike'] 
op_int=Puts2['Open Int']
source = ColumnDataSource(data=dict(x=strikes,y=op_int))
MyHover15 = HoverTool(
	tooltips=[
		( 'Strike', '@x'),
		( 'OI', '@y' ), 
       
	], point_policy="follow_mouse"	
)    
p = figure(title="Current Put Open Interest Grouped SPX",tools=["pan,wheel_zoom,xwheel_zoom,ywheel_zoom,box_zoom,zoom_in, xzoom_in, yzoom_in,zoom_out, xzoom_out, yzoom_out,reset,save,lasso_select", MyHover15], x_axis_label='Strike Price', y_axis_label='OI',width=1200,height=600)
p.yaxis.formatter.use_scientific = False
MyHover15.formatters.use_scientific = False
p.vbar(source=source,x='x', width=0.5, bottom=0,
        top='y', color="firebrick")
show(p)

output_file(f"{folder}/Yesterdays_Put-VolumeGrouped_{sys.argv[3]}_days.html")
strikes=PutsY2['Strike'] 
op_int=PutsY2['Vol']
source = ColumnDataSource(data=dict(x=strikes,y=op_int))
MyHover16 = HoverTool(
	tooltips=[
		( 'Strike', '@x'),
		( 'Vol.', '@y' ), 
       
	], point_policy="follow_mouse"	
)    
p = figure(title="Yesterdays Put Volume Grouped SPX", tools=["pan,wheel_zoom,xwheel_zoom,ywheel_zoom,box_zoom,zoom_in, xzoom_in, yzoom_in,zoom_out, xzoom_out, yzoom_out,reset,save,lasso_select", MyHover16],x_axis_label='Strike Price', y_axis_label='Volume',width=1200,height=600)
p.yaxis.formatter.use_scientific = False
MyHover16.formatters.use_scientific = False
p.vbar(source=source,x='x',  width=0.5, bottom=0,
        top='y', color="firebrick")
show(p)

output_file(f"{folder}/Yesterdays_Call-VolumeGrouped_{sys.argv[3]}_days.html")
strikes=CallsY2['Strike'] 
op_int=CallsY2['Vol']
source = ColumnDataSource(data=dict(x=strikes,y=op_int))
MyHover17 = HoverTool(
	tooltips=[
		( 'Strike', '@x'),
		( 'Vol.', '@y' ), 
       
	], point_policy="follow_mouse"	
)    
p = figure(title="Yesterdays Call Volume Grouped SPX",tools=["pan,wheel_zoom,xwheel_zoom,ywheel_zoom,box_zoom,zoom_in, xzoom_in, yzoom_in,zoom_out, xzoom_out, yzoom_out,reset,save,lasso_select", MyHover17], x_axis_label='Strike Price', y_axis_label='Volume',width=1200,height=600)
p.yaxis.formatter.use_scientific = False
MyHover17.formatters.use_scientific = False
p.vbar(source=source,x='x',  width=0.5, bottom=0,
        top='y', color="firebrick")
show(p)

'''
OI change grouped
'''

output_file(f"{folder}/OI Call-ChangeGrouped_{sys.argv[3]}_days.html")
strikes=Calls2['Strike']
strikes_y=CallsY2['Strike']
op_int=Calls2['Open Int']
op_int_y=CallsY2['Open Int']
source = ColumnDataSource(data=dict(x=strikes,y1=op_int,y2=op_int_y))
MyHover1 = HoverTool(
	tooltips=[
		( 'OI today', '@y1'),
		( 'OI yesterday', '@y2' ), 
        ('Strike','@x')
       
	], point_policy="follow_mouse"	
)    
p = figure(tools=["pan,wheel_zoom,xwheel_zoom,ywheel_zoom,box_zoom,zoom_in, xzoom_in, yzoom_in,zoom_out, xzoom_out, yzoom_out,reset,save,lasso_select", MyHover1], x_axis_label='Strike Price', y_axis_label='OI',width=1200,height=600)
p.title.text = f"OI Call-Change Grouped SPX"

p.yaxis.formatter.use_scientific = False
MyHover1.formatters.use_scientific = False
p.vbar_stack(['y1', 'y2'], x='x', width=0.8, color=("grey", "lightgrey"), source=source)
show(p)



output_file(f"{folder}/OI Put-ChangeGrouped_{sys.argv[3]}_days.html")
strikes=Puts2['Strike']
strikes_y=PutsY2['Strike']
op_int=Puts2['Open Int']
op_int_y=PutsY2['Open Int']
source = ColumnDataSource(data=dict(x=strikes,y1=op_int,y2=op_int_y))
MyHover2 = HoverTool(
	tooltips=[
		( 'OI today', '@y1'),
		( 'OI yesterday', '@y2' ), 
        ('Strike','@x')
       
	], point_policy="follow_mouse"	
)    
p = figure(tools=["pan,wheel_zoom,xwheel_zoom,ywheel_zoom,box_zoom,zoom_in, xzoom_in, yzoom_in,zoom_out, xzoom_out, yzoom_out,reset,save,lasso_select", MyHover2], x_axis_label='Strike Price', y_axis_label='OI',width=1200,height=600)

p.title.text = f"OI Put-Change Grouped SPX"

p.yaxis.formatter.use_scientific = False
MyHover2.formatters.use_scientific = False
p.vbar_stack(['y1', 'y2'], x='x', width=0.8, color=("grey", "lightgrey"), source=source)

show(p)
'''
Just Change, not stacked
'''
Calls2['Strikes']=Calls2.index
CallsY2['Strikes']=CallsY2.index
df_c=pd.merge(Calls2,CallsY2,on='Strikes',how='inner')
df_c['op_int_change']=df_c['Open Int_x']-df_c['Open Int_y']
df_c.to_csv('df_c.csv')
output_file(f"{folder}/OI Call-PureChange_{sys.argv[3]}_days.html")
strikes=df_c['Strikes']
op_int_change=df_c['op_int_change']
source = ColumnDataSource(data=dict(x=strikes,y=op_int_change))
MyHover1 = HoverTool(
	tooltips=[
		( 'OI change', '@y'),
		 
        ('Strike','@x')
       
	], point_policy="follow_mouse"	
)    
p = figure(tools=["pan,wheel_zoom,xwheel_zoom,ywheel_zoom,box_zoom,zoom_in, xzoom_in, yzoom_in,zoom_out, xzoom_out, yzoom_out,reset,save,lasso_select", MyHover1], x_axis_label='Strike Price', y_axis_label='OI',width=1200,height=600)
p.title.text = f"OI Call-Just the change (today-yesterday) SPX"

p.yaxis.formatter.use_scientific = False
MyHover1.formatters.use_scientific = False
p.vbar(source=source,x='x', width=0.5, bottom=0,
        top='y', color="firebrick")
show(p)

Puts2['Strikes']=Puts2.index
PutsY2['Strikes']=PutsY2.index
df_p=pd.merge(Puts2,PutsY2,on='Strikes',how='inner')
df_p['op_int_change']=df_p['Open Int_x']-df_p['Open Int_y']
df_p.to_csv('df_p.csv')
output_file(f"{folder}/OI Put-PureChange_{sys.argv[3]}_days.html")
strikes=df_p['Strikes']
op_int_change=df_p['op_int_change']
source = ColumnDataSource(data=dict(x=strikes,y=op_int_change))
MyHover2 = HoverTool(
	tooltips=[
		( 'OI change', '@y'),
		 
        ('Strike','@x')
       
	], point_policy="follow_mouse"	
)    
p = figure(tools=["pan,wheel_zoom,xwheel_zoom,ywheel_zoom,box_zoom,zoom_in, xzoom_in, yzoom_in,zoom_out, xzoom_out, yzoom_out,reset,save,lasso_select", MyHover2], x_axis_label='Strike Price', y_axis_label='OI',width=1200,height=600)

p.title.text = f"OI Put--Just the change (today-yesterday) SPX"

p.yaxis.formatter.use_scientific = False
MyHover2.formatters.use_scientific = False
p.vbar(source=source,x='x', width=0.5, bottom=0,
        top='y', color="firebrick")
show(p)





'''
OI change simple
'''

output_file(f"{folder}/OI Call-ChangeSimple_{sys.argv[3]}_days.html")
strikes=Calls['Strike']
strikes_y=CallsY['Strike']
op_int=Calls['Open Int']
op_int_y=CallsY['Open Int']
source = ColumnDataSource(data=dict(x=strikes,y1=op_int,y2=op_int_y))
MyHover3 = HoverTool(
	tooltips=[
		( 'OI today', '@y1'),
		( 'OI yesterday', '@y2' ), 
        ('Strike','@x') ,
       
	], point_policy="follow_mouse"	
)    
p = figure(title="OI Call-Change Simple SPX",tools=["pan,wheel_zoom,xwheel_zoom,ywheel_zoom,box_zoom,zoom_in, xzoom_in, yzoom_in,zoom_out, xzoom_out, yzoom_out,reset,save,lasso_select", MyHover3], x_axis_label='Strike Price', y_axis_label='OI',width=1200,height=600)
p.yaxis.formatter.use_scientific = False
MyHover3.formatters.use_scientific = False
p.vbar_stack(['y1', 'y2'], x='x', width=0.8, color=("grey", "lightgrey"), source=source)
show(p)



output_file(f"{folder}/OI Put-ChangeSimple_{sys.argv[3]}_days.html")
strikes=Puts['Strike']
strikes_y=PutsY['Strike']
op_int=Puts['Open Int']
op_int_y=PutsY['Open Int']
source = ColumnDataSource(data=dict(x=strikes,y1=op_int,y2=op_int_y))
MyHover4 = HoverTool(
	tooltips=[
		( 'OI today', '@y1'),
		( 'OI yesterday', '@y2' ), 
        ('Strike','@x'),
       
	], point_policy="follow_mouse"	
)    
p = figure(title="OI Put-Change Simple SPX",tools=["pan,wheel_zoom,xwheel_zoom,ywheel_zoom,box_zoom,zoom_in, xzoom_in, yzoom_in,zoom_out, xzoom_out, yzoom_out,reset,save,lasso_select", MyHover4], x_axis_label='Strike Price', y_axis_label='OI',width=1200,height=600)
p.yaxis.formatter.use_scientific = False
MyHover4.formatters.use_scientific = False
p.vbar_stack(['y1', 'y2'], x='x', width=0.8, color=("grey", "lightgrey"), source=source)
show(p)
'''
GEX
'''


output_file(f"{folder}/GEX_{sys.argv[3]}_days.html")
strikes=x.index 
gex=x.values
source = ColumnDataSource(data=dict(x=strikes,y=gex))
MyHover5 = HoverTool(
	tooltips=[
		( 'Strike', '@x'),
		( 'GEX', '@y' ), 
       
	], point_policy="follow_mouse"	
)    
p = figure(title="GEX SPX",tools=["pan,wheel_zoom,xwheel_zoom,ywheel_zoom,box_zoom,zoom_in, xzoom_in, yzoom_in,zoom_out, xzoom_out, yzoom_out,reset,save,lasso_select", MyHover5], x_axis_label='Strike Price', y_axis_label='GEX',width=1200,height=600)
p.vbar(source=source,x='x', width=0.5, bottom=0,
        top='y', color="firebrick")
p.yaxis.formatter.use_scientific = False
MyHover5.formatters.use_scientific = False
zero = zero_gex
Zero_GEX = Span(location=zero,
                            dimension='height', line_color='red',
                            line_dash='dashed', line_width=3)
p.add_layout(Zero_GEX)
show(p)   

'''
Simple GEX
''' 
output_file(f"{folder}/GEX_simple_{sys.argv[3]}_days.html")
df_gamma=pd.DataFrame()
df_gamma['Strike']=df1['Strike'] 
df_gamma['G_S']=df1['Gamma']*df1['Open Int']*100+df1['Gamma.1']*df1['Open Int.1']*(-100)
df_gamma['G_SS']=df_gamma['G_S']*price*(price/100)
strikes=df_gamma['Strike'] 
gex=df_gamma['G_SS']
source = ColumnDataSource(data=dict(x=strikes,y=gex))
MyHover6 = HoverTool(
	tooltips=[
		( 'Strike', '@x'),
		( 'GEX', '@y' ), 
       
	], point_policy="follow_mouse"	
)    
p = figure(title="GEX simple SPX",tools=["pan,wheel_zoom,xwheel_zoom,ywheel_zoom,box_zoom,zoom_in, xzoom_in, yzoom_in,zoom_out, xzoom_out, yzoom_out,reset,save,lasso_select", MyHover6], x_axis_label='Strike Price', y_axis_label='GEX',width=1200,height=600)
p.yaxis.formatter.use_scientific = False
MyHover6.formatters.use_scientific = False
p.vbar(source=source,x='x', width=0.5, bottom=0,
        top='y', color="firebrick")
show(p)   

'''
Simple GEX grouped
''' 

output_file(f"{folder}/GEX_simpleGrouped_{sys.argv[3]}_days.html")
df_gamma=pd.DataFrame()
df_gamma['Strike']=df1['Strike'] 
df_gamma['G_S']=df1['Gamma']*df1['Open Int']*100+df1['Gamma.1']*df1['Open Int.1']*(-100)
df_gamma['G_SS']=df_gamma['G_S']*price*(price/100)
df_gamma_grouped=pd.DataFrame()
df_gamma_grouped=df_gamma.groupby(['Strike']).sum()
df_gamma_grouped['Strike']=df_gamma_grouped.index
strikes=df_gamma_grouped['Strike'] 
gex=df_gamma_grouped['G_SS']
source = ColumnDataSource(data=dict(x=strikes,y=gex))
MyHover7 = HoverTool(
	tooltips=[
		( 'Strike', '@x'),
		( 'GEX', '@y' ), 
       
	], point_policy="follow_mouse"	
)    
p = figure(title="GEX simple Grouped SPX",tools=["pan,wheel_zoom,xwheel_zoom,ywheel_zoom,box_zoom,zoom_in, xzoom_in, yzoom_in,zoom_out, xzoom_out, yzoom_out,reset,save,lasso_select", MyHover7], x_axis_label='Strike Price', y_axis_label='GEX',width=1200,height=600)
p.yaxis.formatter.use_scientific = False
MyHover7.formatters.use_scientific = False
p.vbar(source=source,x='x', width=0.5, bottom=0,
        top='y', color="firebrick")
show(p)  
'''
GEX with black gamma unfiltered
'''
output_file(f"{folder}/GEX_BlackGrouped_{sys.argv[3]}_days.html")
PutsF=df_full[df_full['Flag']=='p'].copy(deep=True)
CallsF=df_full[df_full['Flag']=='c'].copy(deep=True)
CallsF['GEX']=((CallsF['Open Int']*CallsF['Gamma']*100))
PutsF['GEX']=((PutsF['Open Int']*PutsF['Gamma']*(-100))) 
df_gammaF=pd.DataFrame()
df_gammaF['Strike']=CallsF['Strike'] 
df_gammaF['G_S']=CallsF['GEX']+PutsF['GEX'].values
df_gammaF['G_SS']=df_gammaF['G_S']*price*(price/100)
min_gex=df_gammaF['G_SS'].min()
max_gex=df_gammaF['G_SS'].max()
total_gex=df_gammaF['G_SS'].sum()
df_gammaF_grouped=pd.DataFrame()
df_gammaF_grouped=df_gammaF.groupby(['Strike']).sum()
df_gammaF_grouped['Strike']=df_gammaF_grouped.index
df_gammaF_grouped.to_csv('df_gammaF_grouped.csv')

strikes=df_gammaF_grouped['Strike'] 
gex=df_gammaF_grouped['G_SS']
source = ColumnDataSource(data=dict(x=strikes,y=gex))
MyHover18 = HoverTool(
 	tooltips=[
		( 'Strike', '@x'),
		( 'GEX', '@y' ), 
       
 	], point_policy="follow_mouse"	
)    
p = figure(tools=["pan,wheel_zoom,xwheel_zoom,ywheel_zoom,box_zoom,zoom_in, xzoom_in, yzoom_in,zoom_out, xzoom_out, yzoom_out,reset,save,lasso_select", MyHover18], x_axis_label='Strike Price', y_axis_label='GEX',width=1200,height=600)
p.yaxis.formatter.use_scientific = False
MyHover18.formatters.use_scientific = False
p.vbar(source=source,x='x', width=0.5, bottom=0,
        top='y', color="firebrick")
zero = zero_gex
Zero_GEX = Span(location=zero,
                            dimension='height', line_color='red',
                            line_dash='dashed', line_width=3)
p.add_layout(Zero_GEX)
p.title.text = f"ZeroGex={zero_gex}    minGex={round(min_gex,2)}    maxGex={round(max_gex,2)}    total_gex={round(total_gex,2)}    Last={price}    Put/Call ratio={round(p_c_ratio,2)}"
p.title.align = "center"
p.title.text_color = "grey"
p.title.text_font_size = "14px"
p.title.background_fill_color = "lightgrey"
p.add_layout(Title(text="GEX Black-gamma grouped Grouped SPX", text_font_size="20pt"), 'above')
show(p)   


'''
Lambda
'''

df['Lambda']=(df['Strike']/df['Mid'])*df['Delta']   
output_file(f"{folder}/Lambda_{sys.argv[3]}_days.html")
strikes=df['Strike'] 
lamb=df['Lambda']
source = ColumnDataSource(data=dict(x=strikes,y=lamb))
MyHover8 = HoverTool(
	tooltips=[
		( 'Strike', '@x'),
		( 'Lambda', '@y' ), 
       
	], point_policy="follow_mouse"	
)    
p = figure(title="Lambda SPX (price=Middle)", tools=["pan,wheel_zoom,xwheel_zoom,ywheel_zoom,box_zoom,zoom_in, xzoom_in, yzoom_in,zoom_out, xzoom_out, yzoom_out,reset,save,lasso_select", MyHover8],x_axis_label='Strike Price', y_axis_label='Lambda',width=1200,height=600)
p.yaxis.formatter.use_scientific = False
MyHover8.formatters.use_scientific = False
p.vbar(source=source,x='x', width=0.5, bottom=0,
        top='y', color="firebrick")
show(p)

'''
Lambda grouped
'''

df['Lambda']=(df['Strike']/df['Mid'])*df['Delta']   
df_grouped=df.groupby(['Strike']).sum()
df_grouped['Strike']=df_grouped.index
output_file(f"{folder}/LambdaGrouped_{sys.argv[3]}_days.html")
strikes=df_grouped['Strike'] 
lamb=df_grouped['Lambda']
source = ColumnDataSource(data=dict(x=strikes,y=lamb))
MyHover9 = HoverTool(
	tooltips=[
		( 'Strike', '@x'),
		( 'Lambda', '@y' ), 
       
	], point_policy="follow_mouse"	
)    
p = figure(title="Lambda Grouped SPX (price=Middle)",tools=["pan,wheel_zoom,xwheel_zoom,ywheel_zoom,box_zoom,zoom_in, xzoom_in, yzoom_in,zoom_out, xzoom_out, yzoom_out,reset,save,lasso_select", MyHover9], x_axis_label='Strike Price', y_axis_label='Lambda',width=1200,height=600)
p.yaxis.formatter.use_scientific = False
MyHover9.formatters.use_scientific = False
p.vbar(source=source,x='x', width=0.5, bottom=0,
        top='y', color="firebrick")
show(p)      

print('Connecting to SQLite db -"gexsp.db"')
sql_date=sql_date.strftime('%Y-%m-%d')
try:
    conn = sqlite3.connect("gexsp.db") 
    cursor = conn.cursor()
    cursor.execute("INSERT INTO gex VALUES (?,?,?,?,?,?,?)", (str(sql_date),price,min_gex,zero_gex,max_gex,total_gex,p_c_ratio))
    conn.commit()
    print('SQL database updated')
except Exception as e:
    print(e)
print()
print('Finished')


