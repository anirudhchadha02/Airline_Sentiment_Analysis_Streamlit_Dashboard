import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title("Sentimental Analysis of tweets about US Airlines")
st.sidebar.title("Sentimental Analysis of tweets about US Airlines")

st.markdown("This is a streamlit dashboard used to analyse sentiments of tweets")
st.sidebar.markdown("This is a streamlit dashboard used to analyse sentiments of tweets")

DATA_URL= ("Tweets.csv")
@st.cache_data(persist=True)
def load_data():
    data=pd.read_csv(DATA_URL)
    data['tweet_created']=pd.to_datetime(data['tweet_created'])
    return data

data=load_data()

st.sidebar.subheader("Show random tweet")
random_tweet = st.sidebar.radio('Sentiment', ('positive' , 'negative', 'neutral'))
st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[["text"]].sample(n=1).iat[0,0])

st.sidebar.markdown("### No. of tweets by sentiment")
select = st.sidebar.selectbox('Visualisation type', ['Histogram','Pie Chart'],key='1')
sentiment_count=data['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame({'Sentiment':sentiment_count.index, 'Tweets':sentiment_count.values})

if not st.sidebar.checkbox("Hide", True):
    st.markdown("### No. of tweets by sentiment")
    if select == 'Histogram':
        fig=px.bar(sentiment_count, x='Sentiment', y='Tweets', color='Tweets', height =500)
        st.plotly_chart(fig)
    else:
        fig=px.pie(sentiment_count, values='Tweets', names='Sentiment')
        st.plotly_chart(fig)

st.sidebar.subheader("When and where are users tweeting from?")
hour= st.sidebar.slider("Hour of day",0,23)
modified_data=data[data['tweet_created'].dt.hour == hour]
if not st.sidebar.checkbox("Close", True):
    st.markdown("### Tweet Locations by time of day")
    st.markdown("%i tweets between %i:00 and %i:00" %(len(modified_data),hour, (hour+1)))
    st.map(modified_data)
    if st.sidebar.checkbox("Show raw data", False):
        st.write(modified_data)