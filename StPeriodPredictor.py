# C:/jita/C_thesis/gui/pack2/stperiod.py

import streamlit as st
import pandas as pd
from autogluon.tabular import TabularPredictor

st.write("""
# ML Building Period Predictor
""")

# Height, LFRS, Material, ; Geometry, Foundation Depth, Foundation Type, Floor above ground, Floors below ground

model_path = '0313-crude-clone-opt'
predictor = TabularPredictor.load(model_path).predict

col1, col2 = st.columns(2)

col1.write('Required Parameters')
height = col1.number_input('Height(m)')
loc = col1.selectbox('Location', ['', 'China', 'Chile', 'France', 'Japan', 'Spain', 'Turkey'])
mat = col1.selectbox('Material', ['Concrete', 'Steel', 'Masonry'])
lrfs = col1.selectbox('LFRS', ['Frame', 'Shear Wall', 'Tube'])

col2.write('Optional Parameters')
floor1 = col2.number_input('Floors above ground', key=1)
floor2 = col2.number_input('Floors below ground', key=2)
found_depth = col2.number_input('Foundation depth', key=3)
geom = col2.selectbox('Geometry', ['Rectangular', 'Non-rectangular'])
found_type = col2.selectbox('Foundation type', ['Shaft', 'Direct', 'Pile'])

res_text = f"Period = "

def show_result():
    cols = ['loc', 'name', 'mat', 'lfrs', 'length', 'width', 'height', 'floor1',
       'floor0', 'data_type', 'func1', 'func0', 'plan1', 'plan0', 'f_depth',
       'f_type', 's_type', 'year0', 'year1']
    vals = [loc, '', mat, lrfs, None, None, float(height), None, 
        None, None, None, None, None, None, None, 
        None, None, None, None]
    input_data = {
        'location':loc, 
        'mat':mat, 
        'lfrs':lrfs, 
        'Height':float(height), 
        'name':'','L':None, 'W':None,  'Floors1':None,'Floors2':None, 'func1':'', 'func2':'', 
        'plan1':'', 'plan2':'', 'FoundDepth':None,'FoundType':'', 'SiteType':''}
    input_data = {cols[i]: vals[i] for i in range(len(cols))}
    df = pd.DataFrame(input_data, index=[0])
    result = predictor(df)
    st.dataframe(result)

def batch_results():
    print(data_file)
    test_df = pd.read_excel(data_file)
    st.caption('Test data')
    st.dataframe(test_df.head())
    res_df = predictor(test_df)
    st.caption('Prediction results')
    st.dataframe(res_df)

if st.button('Predict'):
    show_result()
    
data_file = st.file_uploader('Batch Prediction', type=['.xlsx', 'xls'])
if data_file is not None:
    batch_results()


