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
売上傾向および顧客属性による購買行動の違いを明らかにすることである。
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
データ出典：Mohammad Talib (Kaggle)  
Retail Sales Dataset  
https://www.kaggle.com/datasets/mohammadtalib786/retail-sales-dataset  
""")

# ==============================
# ③ 分析方法
# ==============================
st.header("③ 分析方法")
st.markdown("""
日別売上分析、カテゴリ別分析、性別・年代別分析、
売上構成比分析およびクロス分析を行った。
""")

# ==============================
# フィルター
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

st.header("④ 分析結果")

total_sales = filtered_df["Total Amount"].sum()
st.metric("総売上", f"{total_sales:,.0f} 円")

# ---------------- 図1 ----------------
st.subheader("日別売上推移")

daily_sales = filtered_df.groupby("Date")["Total Amount"].sum().reset_index()
fig1 = px.line(daily_sales, x="Date", y="Total Amount")
st.plotly_chart(fig1, use_container_width=True)

st.caption("グラフ 1 日別売上は日ごとに変動しており、一定の増減傾向が確認できる。")

# ---------------- 図2 ----------------
st.subheader("商品カテゴリ別売上")

category_sales = filtered_df.groupby("Product Category")["Total Amount"].sum().reset_index()
fig2 = px.bar(category_sales, x="Product Category", y="Total Amount", color="Product Category")
st.plotly_chart(fig2, use_container_width=True)

st.caption("グラフ 2 カテゴリによって売上規模に差があり、特定カテゴリが高い売上を示している。")

# ---------------- 図3 ----------------
st.subheader("売上構成比")

fig3 = px.pie(category_sales, names="Product Category", values="Total Amount")
st.plotly_chart(fig3, use_container_width=True)

st.caption("グラフ 3 売上は一部の主要カテゴリに集中している傾向が見られる。")

# ---------------- 図4 ----------------
st.subheader("性別別売上")

gender_sales = filtered_df.groupby("Gender")["Total Amount"].sum().reset_index()
fig4 = px.bar(gender_sales, x="Gender", y="Total Amount", color="Gender")
st.plotly_chart(fig4, use_container_width=True)

st.caption("グラフ 4 性別によって購買金額に差が確認された。")

# ---------------- 図5 ----------------
st.subheader("年代別売上")

bins = [0,20,30,40,50,60,100]
labels = ["~20","20代","30代","40代","50代","60代以上"]
filtered_df["Age Group"] = pd.cut(filtered_df["Age"], bins=bins, labels=labels)

age_sales = filtered_df.groupby("Age Group")["Total Amount"].sum().reset_index()
fig5 = px.bar(age_sales, x="Age Group", y="Total Amount", color="Age Group")
st.plotly_chart(fig5, use_container_width=True)

st.caption("グラフ 5 特定の年代層が主要な顧客層である可能性が示唆される。")

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
売上は主に **{top_category}** に集中している。
また、**{top_gender}** の購買額が比較的高い傾向が見られる。
""")

# ==============================
# ⑥ 結論
# ==============================
st.header("⑥ 結論")

st.markdown("""
本分析より、売上は特定カテゴリおよび特定顧客層に依存する傾向が確認された。
今後は時間帯別分析などを追加することで、より詳細な販売戦略の検討が可能である。
""")