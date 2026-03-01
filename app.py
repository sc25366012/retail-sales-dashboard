import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Meiryo'
st.set_page_config(page_title="小売店舗売上分析", layout="wide")

st.title("小売店舗売上データ分析ダッシュボード")

# ==============================
# ① 研究目的
# ==============================
st.subheader("① 研究目的")
st.markdown("""
本分析の目的は、小売店舗の取引データを用いて、
売上傾向および顧客属性（性別・年代）による購買行動の違いを明らかにすることである。
""")

# ==============================
# ② データ概要
# ==============================
st.subheader("② データ概要")

st.markdown("""
データ出典：  
Mohammad Talib (Kaggle)  
Retail Sales Dataset  
https://www.kaggle.com/datasets/mohammadtalib786/retail-sales-dataset  

上記データを用いて筆者作成。
""")

@st.cache_data
def load_data():
    df = pd.read_csv("retail_sales_dataset.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

st.write("データ件数:", len(df))
st.dataframe(df.head())

# ==============================
# サイドバー
# ==============================
st.sidebar.header("分析条件")

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
    (df["Product Category"].isin(selected_category)) &
    (df["Gender"].isin(selected_gender))
].copy()

# ==============================
# ③ 売上分析
# ==============================
st.subheader("③ 売上分析")

# ---- 図1 ----
st.markdown("### 日別売上推移")

daily_sales = filtered_df.groupby("Date")["Total Amount"].sum()

fig1, ax1 = plt.subplots(figsize=(5,3))
ax1.plot(daily_sales.index, daily_sales.values)
ax1.set_xlabel("Date")
ax1.set_ylabel("Sales (円)")
ax1.grid(alpha=0.3)
st.pyplot(fig1)

st.markdown("""
図1 日別売上推移  
データ出典：Kaggle Retail Sales Datasetより筆者作成
""")

total_sales = filtered_df["Total Amount"].sum()

st.markdown(f"""
<p style="color:red; font-weight:bold;">
期間中の総売上は {total_sales:,.0f} 円であり、
日ごとに売上変動が確認された。
</p>
""", unsafe_allow_html=True)

# ---- 図2 ----
st.markdown("### 商品カテゴリ別売上")

category_sales = filtered_df.groupby("Product Category")["Total Amount"].sum()

fig2, ax2 = plt.subplots(figsize=(5,3))
ax2.bar(category_sales.index, category_sales.values)
ax2.set_xlabel("Category")
ax2.set_ylabel("Sales (円)")
ax2.grid(alpha=0.3)
st.pyplot(fig2)

st.markdown("""
図2 商品カテゴリ別売上  
データ出典：Kaggle Retail Sales Datasetより筆者作成
""")

top_category = category_sales.idxmax()

st.markdown(f"""
<p style="color:red; font-weight:bold;">
{top_category} が最も高い売上を記録しており、
売上構造の中心となっている。
</p>
""", unsafe_allow_html=True)

# ==============================
# ④ 顧客属性分析
# ==============================
st.subheader("④ 顧客属性分析")

# ---- 図3 ----
st.markdown("### 性別別売上")

gender_sales = filtered_df.groupby("Gender")["Total Amount"].sum()

fig3, ax3 = plt.subplots(figsize=(5,3))
ax3.bar(gender_sales.index, gender_sales.values)
ax3.set_xlabel("Gender")
ax3.set_ylabel("Sales (円)")
ax3.grid(alpha=0.3)
st.pyplot(fig3)

st.markdown("""
図3 性別別売上  
データ出典：Kaggle Retail Sales Datasetより筆者作成
""")

top_gender = gender_sales.idxmax()

st.markdown(f"""
<p style="color:red; font-weight:bold;">
{top_gender} の購買額が比較的高く、
主要顧客層である可能性が示唆される。
</p>
""", unsafe_allow_html=True)

# ---- 図4 ----
st.markdown("### 年代別売上")

bins = [0,20,30,40,50,60,100]
labels = ["~20","20代","30代","40代","50代","60代以上"]
filtered_df["Age Group"] = pd.cut(filtered_df["Age"], bins=bins, labels=labels)

age_sales = filtered_df.groupby("Age Group")["Total Amount"].sum()

fig4, ax4 = plt.subplots(figsize=(5,3))
ax4.bar(age_sales.index.astype(str), age_sales.values)
ax4.set_xlabel("Age Group")
ax4.set_ylabel("Sales (円)")
ax4.grid(alpha=0.3)
st.pyplot(fig4)

st.markdown("""
図4 年代別売上  
データ出典：Kaggle Retail Sales Datasetより筆者作成
""")

top_age = age_sales.idxmax()

st.markdown(f"""
<p style="color:red; font-weight:bold;">
{top_age} が最も高い売上を記録しており、
主要顧客層として売上に貢献している。
</p>
""", unsafe_allow_html=True)