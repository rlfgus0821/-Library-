import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud
import seaborn as sns
from konlpy.tag import Okt
from nltk.corpus import stopwords
from matplotlib import font_manager, rc
font_name = font_manager.FontProperties(fname='C:/Windows/Fonts/malgun.ttf').get_name()
rc('font', family = font_name)

# 뉴스 데이터 kor_news_20240326.xlsx를 이용하여 스트림릿으로 구현하기
df = pd.read_excel('data\kor_news_240326.xlsx')

# 1. 뉴스데이터를 dataframe으로 표시하기
st.data_editor(df, use_container_width=True, hide_index=True)
st.divider()
# 2. 뉴스데이터의 url 컬럼을 실제 뉴스기사 페이지로 이동하도록 적절한 column configuration 사용
st.data_editor(df,column_config={'URL': st.column_config.LinkColumn()}, hide_index=True)

# 3. 분류 컬럼 중 대분류 컬럼에 대한 빈도를 bar chart로 그리기
df['대분류'] =[i.split('>')[0] for i in df['분류']]
data = df['대분류'].value_counts()
st.bar_chart(data)

# 4. 제목 컬럼에 대하여 텍스트 전처리를 진행한 결과를 토대로 경제, 사회 분야의 빈도가 많은 주요 키워드 20위를 bar chart로 그리기

def news_dist(names, column='제목', n=10):
    okt = Okt()
    stopwords_kr = pd.read_csv('data/한국어 불용어 리스트.csv', encoding='CP949')
    stopwords_list = stopwords_kr.values.tolist()

    # '대분류'로 그룹화
    group_news = df.groupby('대분류')
    stop_words = stopwords_list

    for name, data in group_news:
        if name == names:
            # 그룹별 제목을 합치기
            title = ' '.join(data[column])
            # 단어 토큰화
            word_tokens = okt.pos(title)
            # 명사만 추출 / 1글자 이하 제거 / 불용어 제거
            token_sw = [word for word, tag in word_tokens if len(word) > 1 if tag == 'Noun' if word not in stop_words]
            freq = pd.DataFrame(pd.Series(Counter(token_sw)).sort_values(ascending=False), columns=['freq'])
            print(f'{name}:\n {freq.head(n)}')

            # 바그래프 시각화
            data = freq.iloc[:n]
            st.bar_chart(data)
            plt.title(f'{name}의 TOP{n} 그래프')
            plt.show()

            # 워드 클라우드 시각화
            font_path = 'C:/Windows/Fonts/malgun.ttf'
            wordcloud = WordCloud(font_path=font_path).generate(title)
            plt.axis('off')
            st.image(wordcloud.to_array(), caption='WordCloud')
            plt.show()

news_dist('경제',n=20)
news_dist('사회',n=20)
