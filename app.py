import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="小売店舗売上分析", layout="wide")

st.title("小売店舗売上データ分析レポート")

# ==============================
# ① 研究目的
# ==============================
st.header("① 研究目的")
st.markdown("""
本研究の目的は、小売店舗の販売データを用いて、
売上傾向および顧客属性（性別・年代）による購買行動の違いを明らかにすることである。
""")

# ==============================
# ② データ概要
# ==============================
st.header("② データ概要")

@st.cache_data
def load_data():
    df = pd.read_csv("retail_sales_dataset.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

st.markdown("""
データ出典：  
Mohammad Talib (Kaggle)  
Retail Sales Dataset  
https://www.kaggle.com/datasets/mohammadtalib786/retail-sales-dataset  
""")

st.write("データ件数:", len(df))
st.dataframe(df.head())

# ==============================
# ③ 分析方法
# ==============================
st.header("③ 分析方法")

st.markdown("""
本分析では以下の方法を用いた。

・日別売上の時系列分析  
・商品カテゴリ別売上分析  
・性別および年代別売上分析  
・売上構成比分析  
・商品カテゴリと性別のクロス分析  
""")

# ==============================
# フィルター設定
# ==============================
st.sidebar.header("分析条件")

start_date = st.sidebar.date_input("開始日", df["Date"].min())
end_date = st.sidebar.date_input("終了日", df["Date"].max())

selected_category = st.sidebar.multiselect(
    "商品カテゴリ",
    df["Product Category"].unique(),
    default=df["Product Category"].unique()
)

selected_gender = st.sidebar.multiselect(
    "性別",
    df["Gender"].unique(),
    default=df["Gender"].unique()
)

filtered_df = df[
    (df["Date"] >= pd.to_datetime(start_date)) &
    (df["Date"] <= pd.to_datetime(end_date)) &
    (df["Product Category"].isin(selected_category)) &
    (df["Gender"].isin(selected_gender))
].copy()

# ==============================
# ④ 分析結果
# ==============================
st.header("④ 分析結果")

# KPI
total_sales = filtered_df["Total Amount"].sum()

col1, col2 = st.columns(2)
col1.metric("総売上", f"{total_sales:,.0f} 円")

# ---- 日別売上 ----
st.subheader("4-1 日別売上推移")

daily_sales = filtered_df.groupby("Date")["Total Amount"].sum().reset_index()

fig_daily = px.line(
    daily_sales,
    x="Date",
    y="Total Amount",
    title="日別売上推移",
    markers=True
)
fig_daily.update_layout(
    xaxis_title="日付",
    yaxis_title="売上（円）",
    template="plotly_white"
)
st.plotly_chart(fig_daily, use_container_width=True)

# ---- カテゴリ別 ----
st.subheader("4-2 商品カテゴリ別売上")

category_sales = filtered_df.groupby("Product Category")["Total Amount"].sum().reset_index()

fig_cat = px.bar(
    category_sales,
    x="Product Category",
    y="Total Amount",
    color="Product Category",
    title="カテゴリ別売上"
)
fig_cat.update_layout(
    xaxis_title="商品カテゴリ",
    yaxis_title="売上（円）",
    template="plotly_white"
)
st.plotly_chart(fig_cat, use_container_width=True)

# ---- 性別 ----
st.subheader("4-3 性別別売上")

gender_sales = filtered_df.groupby("Gender")["Total Amount"].sum().reset_index()

fig_gender = px.bar(
    gender_sales,
    x="Gender",
    y="Total Amount",
    color="Gender",
    title="性別別売上"
)
fig_gender.update_layout(
    xaxis_title="性別",
    yaxis_title="売上（円）",
    template="plotly_white"
)
st.plotly_chart(fig_gender, use_container_width=True)

# ---- 年代 ----
st.subheader("4-4 年代別売上")

bins = [0,20,30,40,50,60,100]
labels = ["~20","20代","30代","40代","50代","60代以上"]
filtered_df["Age Group"] = pd.cut(filtered_df["Age"], bins=bins, labels=labels)

age_sales = filtered_df.groupby("Age Group")["Total Amount"].sum().reset_index()

fig_age = px.bar(
    age_sales,
    x="Age Group",
    y="Total Amount",
    color="Age Group",
    title="年代別売上"
)
fig_age.update_layout(
    xaxis_title="年代",
    yaxis_title="売上（円）",
    template="plotly_white"
)
st.plotly_chart(fig_age, use_container_width=True)

# ---- 構成比 ----
st.subheader("4-5 売上構成比")

fig_pie = px.pie(
    category_sales,
    names="Product Category",
    values="Total Amount",
    title="売上構成比"
)
st.plotly_chart(fig_pie, use_container_width=True)

# ---- クロス分析 ----
st.subheader("4-6 商品カテゴリ × 性別分析")

cross = pd.crosstab(
    filtered_df["Product Category"],
    filtered_df["Gender"],
    values=filtered_df["Total Amount"],
    aggfunc="sum"
).fillna(0)

st.dataframe(cross)

# ==============================
# ⑤ 考察
# ==============================
st.header("⑤ 考察")

top_category = category_sales.loc[
    category_sales["Total Amount"].idxmax()
]["Product Category"] if not category_sales.empty else "N/A"

top_gender = gender_sales.loc[
    gender_sales["Total Amount"].idxmax()
]["Gender"] if not gender_sales.empty else "N/A"

st.markdown(f"""
本分析の結果、売上は主に **{top_category}** に集中していることが確認された。
また、**{top_gender}** の購買額が比較的高い傾向が見られ、
顧客層による購買行動の差異が示唆された。
""")

# ==============================
# ⑥ 結論
# ==============================
st.header("⑥ 結論")

st.markdown("""
本研究より、売上は特定の商品カテゴリおよび顧客属性に依存する傾向が確認された。
今後は時間帯別分析や顧客リピート率の分析を行うことで、
より精度の高い販売戦略立案が可能になると考えられる。
""")