# 系统初始化配置
import streamlit as st
import pandas as pd
import plotly.express as px

# 页面基础配置
st.set_page_config(
    page_title="智能家庭理财系统",
    page_icon="👨👩👧👦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 注入自定义CSS样式
st.markdown("""
<style>
    .stSlider [data-baseweb="slider"] {
        padding: 0.8rem;
    }
    div[data-testid="stExpander"] div[role="button"] p {
        font-size: 1.2rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


# 核心计算函数（带缓存优化）
@st.cache_data(ttl=3600, show_spinner="正在优化资产配置方案...")
def calculate(age, risk, family_members, features, edu_priority):
    family_factor = 0.5 if "有赡养老人" in features else 1.0
    edu_weight = 0.2 * edu_priority

    allocation = {
        '现金类': max(0.1, 0.3 - 0.05 * risk),
        '固收类': 0.4 * family_factor,
        '权益类': 0.2 + 0.05 * risk,
        '保险类': 0.1 + edu_weight
    }

    df = pd.DataFrame(allocation.items(), columns=['类别', '比例'])
    fig = px.pie(df, names='类别', values='比例',
                 title=f"{family_members}口之家资产配置方案",
                 hole=0.3,
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    return fig


# 主界面布局
st.title("👨👩👧👦 家庭资产配置比例建议")

# 参数输入面板
with st.expander("⚙️ 家庭参数配置", expanded=True):
    col1, col2 = st.columns([1, 2])

    with col1:
        age = st.slider("年龄", 20, 60, 30,
                        help="请选择家庭主要收入成员的年龄")
        risk = st.slider("风险承受力", 1, 10, 5,
                         help="1代表保守型，10代表激进型")

    with col2:
        family_members = st.number_input("家庭成员数", 1, 10, 3,
                                         help="包含所有共同生活的家庭成员")
        features = st.multiselect("家庭特征",
                                  ["有学龄儿童", "有赡养老人", "有房贷"],
                                  help="可多选家庭特殊需求")
        edu_priority = st.select_slider("教育支出优先级",
                                        options=range(1, 6),
                                        value=3,
                                        help="1为最低优先级，5为最高优先级")

# 可视化展示区
if st.button("生成智能方案", use_container_width=True):
    with st.spinner("正在生成最优配置方案..."):
        fig = calculate(age, risk, family_members, features, edu_priority)
        st.plotly_chart(fig, use_container_width=True)

# 侧边栏附加功能
with st.sidebar:
    st.header("历史方案")
    # 此处可添加数据库连接功能
    # 示例占位内容
    st.caption("暂无历史记录")
    st.divider()
    st.download_button("导出配置方案",
                       data=pd.DataFrame().to_csv().encode('utf-8'),
                       file_name='asset_allocation.csv',
                       disabled=True)
