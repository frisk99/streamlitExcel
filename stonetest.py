import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
from matplotlib.font_manager import FontProperties
font_set = FontProperties(fname=r"dp_calculator\fonts\SourceHanSansSC-Bold.otf", size=15)
str1 = '<h3 align="center">粤港澳大湾区城市群高质量发展统计分析平台</h3>'
st.markdown(str1,True)
if 'city' not in st.session_state:
    st.session_state['city'] = ' '
if 'year' not in st.session_state:
    st.session_state['year'] = ' '
if 'kpi' not in st.session_state:
    st.session_state['kpi'] = ' '
@st.cache
def load_data(path):
    df = pd.read_excel(path)
    return df
data=load_data('./data.xlsx')
#st.table(data.head(5))
city_list = data['city'].unique()
citys = city_list.tolist()
city_list = np.insert(city_list,0,' ')
year_list = [' ',2011,2012,2013,2014,2015,2016,2017,2018,2019]
kpi_list = [' ','经济发展质量指数',  '创新驱动指数',  '产业升级指数',  '双循环指数',  '公共服务指标',  '污染减排指标', '改革与治理指标']
select_year = st.sidebar.selectbox(
    "年份",
      year_list
)
select_city = st.sidebar.selectbox(
    "城市",
     city_list
)
select_kpi = st.sidebar.selectbox(
    "指标",
      kpi_list
)
click =st.sidebar.button('确定')
if click :
    st.session_state['city']=select_city
    st.session_state['year']=select_year
    st.session_state['kpi'] =select_kpi
    #click =False
# 左右点击切换按钮模块

# static_city = st.select_slider(
#      'Select a color of the rainbow',
#     options=citys,
#     value=('广州市'))
#st.write('select', static_city)
city_df = data[data["city"] == select_city]
# st.write(city_df)
# st.write(select_kpi)
if( (st.session_state['kpi'] != ' ' )& (st.session_state['city'] !=' ' ) &(st.session_state['year'] ==' ') ) :
    select_city =st.session_state['city']
    select_kpi = st.session_state['kpi']
    col1,col2 = st.columns(2)
    rank=select_kpi+'排名'
  #  st.title(select_city+select_kpi+'折线图')
    sub_df = data[data.city ==select_city]
    data_x = data['year']
# sub_df = sub_df[['year',select_kpi]]
    sub_df = sub_df.groupby(['year']).mean()
    data_y =sub_df[select_kpi]
    trace = go.Scatter(
        x=data_x,
        y=data_y,
        mode='lines+markers',  # 折线图
        name=select_city+select_kpi,
        line=dict(
            color='rgba(255, 182, 193)',
            width=2,
        )

    )
    font_title = FontProperties(
        fname=r"dp_calculator\fonts\SourceHanSansSC-Bold.otf", size=15)
    layout = {
        "showlegend": True
    }
    picdata = [trace]
    fig = go.Figure(data=picdata,layout=layout)
    fig.update(layout=dict(
        title=dict(text=select_city+select_kpi+'折线图',
                   # 标题名称位置；标题中使用HTML标签
                   x=0.4,
                   y=0.9
                   ),

    ))
    st.plotly_chart(fig)
    st.write(select_city+'历年'+rank)
    st.table(sub_df[[rank]])

if( (st.session_state['kpi'] !=' ') & (st.session_state['year'] != ' ') & (st.session_state['city'] ==' ') ):
    select_year = st.session_state['year']
    select_kpi = st.session_state['kpi']
    sub_df = data[data.year==select_year]
    sub_df = sub_df.sort_values(select_kpi)
    rank = select_kpi+'排名'
    fig = px.histogram(
        sub_df[['city',select_kpi,select_kpi+'排名']],
        x=sub_df[select_kpi],
        y=sub_df['city'],
        color="city",  # 颜色分组
        labels={
            '排名':sub_df[rank]
        }
    )
    st.title(str(select_year)+'年'+select_kpi+'直方图')
    fig.update(layout=dict(xaxis=dict(title=select_kpi, tickangle=-30,
                                      showline=True, nticks=20),
                           yaxis=dict(title="city", showline=False),
                           title ='各市'+str(select_year)+'年'+select_kpi,
                           width=500, height=500,
                           ))
    st.plotly_chart(fig)
if( (st.session_state['kpi'] ==' ') & (st.session_state['year'] == ' ') & (st.session_state['city'] !=' ')):
    select_city = st.session_state.city
    #st.title(select_city+'历年各项指标')
    st.write(select_city+'历年各项指标')
    sub_df = data[data.city == select_city]
    sub_df1 = sub_df
    sub_df =sub_df[['year','经济发展质量指数',  '创新驱动指数',  '产业升级指数',  '双循环指数',  '公共服务指标', '污染减排指标', '改革与治理指标']]
    sub_df.set_index('year', inplace=True)
    sub_df = sub_df[sub_df.columns[::-1]]
    st.line_chart(sub_df[['经济发展质量指数',  '创新驱动指数',  '产业升级指数',  '双循环指数',  '公共服务指标', '污染减排指标', '改革与治理指标']])
    sub_df1.rename(columns={'year':'年份'},inplace=True)
    st.write(select_city + '历年各项指标排名')
    st.table(sub_df1[['年份','经济发展质量指数排名',  '创新驱动指数排名',  '产业升级指数排名',  '双循环指数排名',  '公共服务指标排名', '污染减排指标排名', '改革与治理指标排名']])
if( (select_kpi !=' ') & (select_year != ' ') & (select_city !=' ') ):
    sub_df = data[(data.city == select_city) ]
    sub_df =sub_df[sub_df.year == select_year]
    rank=select_kpi+'排名'
    sub_df.rename(columns={rank:'排名'}, inplace=True)
    fig = go.Figure(data=[go.Table(
        header=dict(values=[select_kpi, '排名'],
                    font_size=18,
                    height=30),

        # 设置表头
        cells=dict(values=[sub_df[select_kpi],  # 通过numpy给定数据
                           sub_df['排名']
                           ],
                   font_size=15,
                   height=30))
    ]
    )
    fig.update(layout=dict(
                           title=dict(text=str(select_year)+select_city+select_kpi[0:len(select_kpi)-2]+'情况',
                                      # 标题名称位置；标题中使用HTML标签
                                      x=0.5,
                                      y=0.9
                                      ),

                           ))
    st.plotly_chart(fig)
if 'count' not in st.session_state:
    st.session_state['count'] = 0
if 'switchyear' not in st.session_state:
    st.session_state['switchyear'] = 2011
if ( (st.session_state['kpi'] ==' ') & (st.session_state['year'] != ' ') & (st.session_state['city'] ==' ') ):
    select_year = st.session_state['year']
    #fig,ax =plt.hist(data)
    col1, col2,col3,col4,col5,col6,col7,col8 = st.columns(8)
    buttonleft=col1.button('<')
    buttonright=col8.button('>')
    if (buttonleft & (st.session_state.count>0)):
        st.session_state.count = st.session_state.count -1
    if (buttonright & (st.session_state.count<20)):
        st.session_state.count = st.session_state.count +1
    index =st.session_state.count
    city = citys[index]
    #st.header(city+str(st.session_state['year'])+'年'+'各项指标')
    sub_df = data[(data.city == city) & (data.year == select_year)]
    sub_df.plot.bar()
    data_y = sub_df[['经济发展质量指数',  '创新驱动指数',  '产业升级指数',  '双循环指数',  '公共服务指标', '污染减排指标', '改革与治理指标']].values
    datay=[]
    for i in data_y.flat:
        datay.append(i)
    truey=np.array(datay)
    kpis=[ '经济发展质量指数',  '创新驱动指数',  '产业升级指数',  '双循环指数',  '公共服务指标', '污染减排指标', '改革与治理指标']
    plt.rcParams[
        'font.sans-serif'] = [
        'SimHei']
    ind = len(kpis)
    x=np.arange(0,7,1)
    y=np.arange(0,6,1)
    fig = px.histogram(
        x=kpis,
        y=truey,
        color=kpis,  # 颜色分组
    )
    fig.update(layout=dict(xaxis=dict(title=' ', tickangle=-30,
                                      showline=True, nticks=20),
                           yaxis=dict(title="指标数", showline=False),
                           title=dict(text=city+str(st.session_state['year'])+'年'+'各项指标',
                                      # 标题名称位置；标题中使用HTML标签
                                      x=0.5,
                                      y=0.97
                                      ),
                           width=700, height=580,
                           ))
    st.plotly_chart(fig)
if ( (st.session_state['kpi'] ==' ') & (st.session_state['year'] != ' ') & (st.session_state['city'] !=' ') ):
    select_year = st.session_state['year']
    index =st.session_state.count
    city = st.session_state.city
#st.header(city+str(st.session_state['year'])+'年'+'各项指标')
    sub_df = data[(data.city == city) & (data.year == select_year)]
    sub_df.plot.bar()
    data_y = sub_df[['经济发展质量指数',  '创新驱动指数',  '产业升级指数',  '双循环指数',  '公共服务指标', '污染减排指标', '改革与治理指标']].values
    datay=[]
    for i in data_y.flat:
        datay.append(i)
    truey=np.array(datay)
    kpis=[ '经济发展质量指数',  '创新驱动指数',  '产业升级指数',  '双循环指数',  '公共服务指标', '污染减排指标', '改革与治理指标']
    plt.rcParams[
        'font.sans-serif'] = [
        'SimHei']
    ind = len(kpis)
    x=np.arange(0,7,1)
    y=np.arange(0,6,1)
    fig = px.histogram(
        x=kpis,
        y=truey,
        color=kpis,  # 颜色分组

    )
 #  title = city + str(st.session_state['year']) + '年' + '各项指标',
    fig.update(layout=dict(xaxis=dict(title=' ', tickangle=-30,
                                      showline=True, nticks=20),
                           yaxis=dict(title="指标数", showline=False),
                           title=dict(text= city + str(st.session_state['year']) + '年' + '各项指标',
                                      # 标题名称位置；标题中使用HTML标签
                                      x=0.5,
                                      y=0.97
                                      ),
                           width=700, height=580,
                           ))
    st.plotly_chart(fig)
if( (st.session_state['kpi'] !=' ') & (st.session_state['year'] == ' ') & (st.session_state['city'] ==' ') ):
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
    buttonleft = col1.button('<')
    buttonright = col8.button('>')
    if (buttonleft & (st.session_state.switchyear > 2011)):
        st.session_state.switchyear = st.session_state.switchyear - 1
    if (buttonright & (st.session_state.switchyear < 2019)):
        st.session_state.switchyear = st.session_state.switchyear + 1
    select_kpi = st.session_state['kpi']
    sub_df = data[data.year==st.session_state.switchyear]
    sub_df = sub_df.sort_values(select_kpi)
    rank = select_kpi+'排名'
    fig = px.histogram(
        sub_df[['city',select_kpi,select_kpi+'排名']],
        x=sub_df[select_kpi],
        y=sub_df['city'],
        color="city",  # 颜色分组
        labels={
            '排名':sub_df[rank]
        }
    )
    #st.subheader(str(st.session_state.switchyear)+'年'+select_kpi+'直方图')
    #str = '<h1 align="center">This is heading 1</h1>'
    #st.markdown(str,True)
    fig.update(layout=dict(xaxis=dict(title=select_kpi, tickangle=-30,
                                      showline=True, nticks=20),
                           yaxis=dict(title="city", showline=False),
                           title =dict(text= str(st.session_state.switchyear)+'年'+select_kpi+'直方图',
                                      # 标题名称位置；标题中使用HTML标签
                                      x=0.5,
                                      y=0.97
                                      ),
                           width=700, height=580,
                           ))
    st.plotly_chart(fig)
    # buttonleft = col1.button('<')
    # buttonright = col8.button('>')
    # if (buttonleft & (st.session_state.switchyear > 2011)):
    #     st.session_state.switchyear = st.session_state.switchyear - 1
    # if (buttonright & (st.session_state.switchyear < 2019)):
    #     st.session_state.switchyear = st.session_state.switchyear + 1
str2='<a style="display: block;text-align:right;color:#d0d0d0;">powered by Nanjing Audit University</a>'
if(not ((st.session_state['kpi'] ==' ') & (st.session_state['year'] == ' ') & (st.session_state['city'] ==' ')) ):
    st.markdown(str2,True)
if( (st.session_state['kpi'] ==' ') & (st.session_state['year'] == ' ') & (st.session_state['city'] ==' ') ):
   # str3 ='<style><body background="https://i.loli.net/2021/12/03/iToaG2Egfx3kcF4.jpg"> <body>'
    st.image("https://z3.ax1x.com/2021/12/03/oaePrF.jpg")
    st.write(':sunny:这是一个数据分析网页')
    st.write(':point_left: 点击侧边栏选取各项指标 :page_facing_up:')
    st.write(':smiley: 点击确定来查看图表 :bar_chart:')
    for i in range(20):
        st.write("")
    #st.write("powered by Nanjing Audit University")
    str3 = '<a style="display: block;color:#d0d0d0;position: absolute;bottom: 0;left: 0;">powered by Nanjing Audit University</a>'
    st.markdown(str3,True)
