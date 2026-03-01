import streamlit as st
import pandas as pd

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

# ---- 図1 日別売上 ----
st.markdown("### 図1 日別売上推移")

daily_sales = filtered_df.groupby("Date")["Total Amount"].sum()
st.line_chart(daily_sales)

st.markdown("""
データ出典：Kaggle Retail Sales Datasetより筆者作成
""")

total_sales = filtered_df["Total Amount"].sum()

st.markdown(f"""
<p style="color:red; font-weight:bold;">
期間中の総売上は {total_sales:,.0f} 円であり、
日ごとに売上変動が確認された。
</p>
""", unsafe_allow_html=True)

# ---- 図2 カテゴリ別 ----
st.markdown("### 図2 商品カテゴリ別売上")

category_sales = filtered_df.groupby("Product Category")["Total Amount"].sum()
st.bar_chart(category_sales)

st.markdown("""
データ出典：Kaggle Retail Sales Datasetより筆者作成
""")

top_category = category_sales.idxmax() if not category_sales.empty else "N/A"

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

# ---- 図3 性別 ----
st.markdown("### 図3 性別別売上")

gender_sales = filtered_df.groupby("Gender")["Total Amount"].sum()
st.bar_chart(gender_sales)

st.markdown("""
データ出典：Kaggle Retail Sales Datasetより筆者作成
""")

top_gender = gender_sales.idxmax() if not gender_sales.empty else "N/A"

st.markdown(f"""
<p style="color:red; font-weight:bold;">
{top_gender} の購買額が比較的高く、
主要顧客層である可能性が示唆される。
</p>
""", unsafe_allow_html=True)

# ---- 図4 年代別 ----
st.markdown("### 図4 年代別売上")

bins = [0,20,30,40,50,60,100]
labels = ["~20","20代","30代","40代","50代","60代以上"]
filtered_df["Age Group"] = pd.cut(filtered_df["Age"], bins=bins, labels=labels)

age_sales = filtered_df.groupby("Age Group")["Total Amount"].sum()
st.bar_chart(age_sales)

st.markdown("""
データ出典：Kaggle Retail Sales Datasetより筆者作成
""")

top_age = age_sales.idxmax() if not age_sales.empty else "N/A"

st.markdown(f"""
<p style="color:red; font-weight:bold;">
{top_age} が最も高い売上を記録しており、
主要顧客層として売上に貢献している。
</p>
""", unsafe_allow_html=True)

# ==============================
# ⑤ 売上傾向まとめ
# ==============================
st.subheader("⑤ 売上傾向まとめ")

if not category_sales.empty and not gender_sales.empty and not age_sales.empty:
    st.markdown(f"""
    <p style="color:red; font-weight:bold;">
    分析結果の要約：売上は {top_category} に集中しており、
    {top_age} が主要顧客層であることが確認された。
    また、{top_gender} の購買額が比較的高い傾向が見られる。
    </p>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <p style="color:red; font-weight:bold;">
    選択条件に該当するデータが存在しません。
    </p>
    """, unsafe_allow_html=True)

# ==============================
# ⑥ 結論
# ==============================
st.subheader("⑥ 結論")

st.markdown("""
<p style="color:red; font-weight:bold;">
本分析より、売上は特定の商品カテゴリおよび特定の年代層に依存する傾向が確認された。
今後は時間帯別や季節別の分析を追加することで、
より詳細な購買傾向の把握が可能になると考えられる。
</p>
""", unsafe_allow_html=True)