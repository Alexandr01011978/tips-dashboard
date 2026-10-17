
import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px

# Заголовок дашборда
st.title("️ Анализ чаевых в ресторане")
st.markdown("**Автор:** Оганисьянец Александр Александрович, поток САБДИС-804")

# Загрузка данных
tips = sns.load_dataset('tips')
tips['tip_percent'] = tips['tip'] / tips['total_bill'] * 100

# Боковая панель с фильтрами
st.sidebar.header(" Фильтры")
days = st.sidebar.multiselect(
    "Выберите дни недели:",
    options=tips['day'].unique(),
    default=tips['day'].unique()
)
times = st.sidebar.multiselect(
    "Выберите время:",
    options=tips['time'].unique(),
    default=tips['time'].unique()
)

# Фильтрация данных
filtered = tips[(tips['day'].isin(days)) & (tips['time'].isin(times))]

# Статистика
st.subheader(" Общая статистика")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Всего заказов", len(filtered))
col2.metric("Средний счет", f"${filtered['total_bill'].mean():.2f}")
col3.metric("Средние чаевые", f"${filtered['tip'].mean():.2f}")
col4.metric("Средний % чаевых", f"{filtered['tip_percent'].mean():.1f}%")

# График 1: Связь счета и чаевых
st.subheader(" Связь между суммой счета и чаевыми")
fig1 = px.scatter(
    filtered, x='total_bill', y='tip', color='day', size='size',
    hover_data=['sex', 'smoker', 'time', 'tip_percent'],
    title='Интерактивный scatter plot'
)
st.plotly_chart(fig1, use_container_width=True)

# График 2: Средние чаевые по дням
st.subheader("📊 Средние чаевые по дням недели")
fig2 = px.bar(
    filtered.groupby('day')['tip'].mean().reset_index(),
    x='day', y='tip', color='day',
    title='Средний размер чаевых'
)
st.plotly_chart(fig2, use_container_width=True)

# График 3: Boxplot процента чаевых
st.subheader("📦 Распределение % чаевых по дням")
fig3 = px.box(
    filtered, x='day', y='tip_percent', color='day',
    title='Boxplot процента чаевых'
)
st.plotly_chart(fig3, use_container_width=True)

# Таблица данных
st.subheader("📋 Таблица данных")
st.dataframe(filtered.head(20))

# Ссылка на GitHub с кодом
st.sidebar.markdown("---")
st.sidebar.info("Дашборд создан на Streamlit + Plotly")
