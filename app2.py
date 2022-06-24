import streamlit as st
import pickle
import numpy as np
from haversine import haversine

data = pickle.load(open('dataset.pkl', 'rb'))
model = pickle.load(open('logistic_reg.pkl', 'rb'))


project = st.sidebar.radio('SELECT AN OPTION', ['HOME', 'PREDICTION'])

if project == 'PREDICTION':
    st.sidebar.image('https://www.rabkindermpath.com/blog/admin/uploads/2020/rabkindx3.jpg')
    st.title('Pathology Specimen Collection')
    agent_id = st.selectbox('Select Agent ID', data['Agent ID'].unique())
    slot = st.selectbox('Select Booking Slot', ['06:00 to 21:00 (Home)' , '19:00 to 22:00 (working person)', '06:00 to 18:00 (Collect at work place)'])
    gender = st.radio('Select Gender', ['Female', 'Male'])
    storage = st.selectbox('Specimen Storage', ['Vacuum blood collection tube', 'Urine culture transport tube', 'Disposable plastic container'])
    distance = np.log(st.number_input('Distance Between Patient and Agent in Meters'))
    collection_time = st.number_input('Specimen collection Time in minutes')
    patient_from = st.number_input('PATIENT AVAILABLE FROM', min_value=1, value=20)
    if st.checkbox('Show Instruction 1'):
        st.text('In "PATIENT AVAILABLE FROM" input the time when patient is available for test\n'
                'Eg.: patient is available from 13(1PM) to 14(2PM)\n'
                'Note: value should be in 24-hour format')
    patient_to = st.number_input('PATIENT AVAILABLE TO', min_value=1, value=21)
    if st.checkbox('Show Instruction 2'):
        st.text('In "PATIENT AVAILABLE TO" input the time when patient is available upto for test\n'
                'Eg.: patient is available from 13(1PM) to 14(2PM)\n'
                'Note: value should be in 24-hour format')
    agent_before = st.number_input('PATIENT ARRIVED BEFORE', min_value=1, value=21)
    if st.checkbox('Show Instruction 3'):
        st.text('Eg.: agent will reach before 14(2PM)')

    if st.button('Predict Timing'):

        if slot == '06:00 to 18:00 (Collect at work place)':
            slot = 0
        elif slot == '06:00 to 21:00 (Home)':
            slot = 1
        elif slot == '19:00 to 22:00 (working person)':
            slot = 2

        if gender == 'Female':
            gender = 0
        elif gender == 'Male':
            gender = 1

        if storage == 'Disposable plastic container':
            storage = 0
        elif storage == 'Urine culture transport tube':
            storage = 1
        elif storage == 'Vacuum blood collection tube':
            storage = 2

        query = np.array([agent_id, slot, gender, storage, distance, collection_time, patient_from, patient_to, agent_before])
        query = query.reshape(1, 9)

        result = model.predict(query)

        if result == 24:
            st.success(f'Agent will reached within {24} minutes')
        elif result == 34:
            st.success(f'Agent will reached within {34} minutes')
        elif result == 39:
            st.success(f'Agent will reached within {39} minutes')
        elif result == 49:
            st.success(f'Agent will reached within {49} minutes')
        elif result == 54:
            st.success(f'Agent will reached within {54} minutes')
        else:
            st.success(f'Agent will reached within {64} minutes')
            st.write('Your Location is to far')

if project == 'HOME':
    st.image('https://upload.wikimedia.org/wikipedia/commons/6/62/Latitude_and_Longitude_of_the_Earth.svg')
    if st.checkbox('HOW TO CALCULATE LATITUDES AND LONGITUDES ?'):
        st.subheader('STEP 1 : Open Maps\n')
        st.image('https://raw.githubusercontent.com/datasciritwik/test/main/step1.png')
        st.subheader('STEP 2 : Choose Agent Location then select coordinates\n')
        st.image('https://raw.githubusercontent.com/datasciritwik/test/main/Agent.png')
        st.write('Select and copy the coordinates appears on sidebar, eg: 17.431024, 78.373442')
        st.subheader('STEP 3 : Choose Patient Location then select coordinates\n')
        st.image('https://raw.githubusercontent.com/datasciritwik/test/main/patient.png')
        st.write('Select and copy the coordinates appears on sidebar, eg: 17.440018, 78.356908')
        st.subheader('STEP 4 : Input those coordinates into our formula')
    st.write("Click Above only you don't know how to calculate latitudes and longitudes else select below !")
    if st.checkbox('SHOW FORMULA'):
        st.subheader('HAVERSINE DISTANCE FORMULA')
        lat1 = round((st.number_input('AGENT LATITUDE')), 6)
        st.write('Enter up to minimum six decimal places')
        lon1 = round((st.number_input('AGENT LONGITUDE')), 6)
        st.write('Enter up to minimum six decimal places')
        lat2 = round((st.number_input('PATIENT LATITUDE')), 6)
        st.write('Enter up to minimum six decimal places')
        lon2 = round((st.number_input('PATIENT LONGITUDE')), 6)
        st.write('Enter up to minimum six decimal places')

        loc1 = (lat1, lon1)
        loc2 = (lat2, lon2)
        if st.checkbox('Show Coordinates'):
            st.write('Agent Location Coordinates', loc1)
            st.write('Patient Location Coordinates', loc2)
        if st.button('Calculate'):
            distance = int(haversine(loc1, loc2, unit='m'))
            st.success(f'Shortest Distance Between Agent and Patient is {distance} meters')
