import streamlit as st
from datetime import datetime

st.set_page_config(page_title="MarketMind", page_icon="📈", layout="wide")

DEMO_VIDEO_URL = "PASTE-YOUR-DEMO-VIDEO-LINK-HERE"
PRESENTATION_URL = "PASTE-YOUR-PRESENTATION-LINK-HERE"

st.markdown("""
<style>
.lock-card{max-width:760px;margin:7rem auto 2rem;padding:3rem;border-radius:24px;border:1px solid rgba(128,128,128,.25);text-align:center;background:rgba(128,128,128,.06)}
.lock-icon{font-size:4.5rem}.lock-title{font-size:2rem;font-weight:800}.lock-description{color:#777;line-height:1.7}
.main-title{font-size:3rem;font-weight:800}.subtitle{color:#777;font-size:1.1rem}
.footer{text-align:center;color:#888;padding:2rem}
</style>
""", unsafe_allow_html=True)

if "unlocked" not in st.session_state:
    st.session_state.unlocked = False

if not st.session_state.unlocked:
    st.markdown("""
    <div class="lock-card">
      <div class="lock-icon">🔐</div>
      <div class="lock-title">MarketMind AI is Locked</div>
      <div class="lock-description">
        Welcome to <b>MarketMind</b>, an agentic market-intelligence application.<br><br>
        The application remains locked until an OpenAI API key is provided.
      </div>
    </div>
    """, unsafe_allow_html=True)

    key = st.text_input("🔑 Enter your OpenAI API key", type="password", placeholder="sk-...")
    if st.button("🚀 Unlock MarketMind", type="primary", use_container_width=True):
        if not key.strip():
            st.error("Please provide an OpenAI API key.")
        else:
            st.session_state.api_key = key.strip()
            st.session_state.unlocked = True
            st.rerun()

    a, b = st.columns(2)
    with a:
        if PRESENTATION_URL.startswith("http"):
            st.link_button("📊 Open Presentation", PRESENTATION_URL, use_container_width=True)
        else:
            st.info("Presentation link will be added here.")
    with b:
        if DEMO_VIDEO_URL.startswith("http"):
            st.link_button("🎥 Watch Demo Video", DEMO_VIDEO_URL, use_container_width=True)
        else:
            st.info("Demo video link will be added here.")
    st.stop()

st.markdown('<div class="main-title">📈 MarketMind</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Agentic Market Intelligence & AI Research Assistant</div>', unsafe_allow_html=True)

with st.sidebar:
    st.success("🔓 Application unlocked")
    agent = st.selectbox("Choose an Agent", [
        "📊 Market Analyst",
        "📰 News & Sentiment Analyst",
        "🔎 Fundamental Researcher",
        "⚠️ Risk Analyst",
        "🧠 MarketMind Full Investigation"
    ])
    model = st.selectbox("AI Model", ["gpt-4o-mini", "gpt-4o"])
    temperature = st.slider("Analysis creativity", 0.0, 1.0, 0.2, 0.1)
    if st.button("🔒 Lock Application", use_container_width=True):
        st.session_state.clear()
        st.rerun()

tabs = st.tabs(["🤖 Agent Workspace", "📊 Market Dashboard", "📚 Notes", "🎓 Presentation", "🎥 Demo Video", "ℹ️ About"])

with tabs[0]:
    st.subheader("🤖 Agent Workspace")
    prompt = st.text_area("Ask MarketMind", placeholder="Example: Analyze the opportunities and risks in the market information below.", height=130)
    context = st.text_area("Optional market context", placeholder="Paste company information, financial data, news text, or research notes.", height=120)
    if st.button("🧠 Run Agent Analysis", type="primary", use_container_width=True):
        if not prompt.strip():
            st.warning("Enter a task first.")
        else:
            try:
                from langchain_openai import ChatOpenAI
                from langchain_core.messages import SystemMessage, HumanMessage
                roles = {
                    "📊 Market Analyst":"Analyze trends, opportunities, competition, and business implications.",
                    "📰 News & Sentiment Analyst":"Analyze supplied news/text for themes, sentiment, catalysts, and market implications. Do not invent news.",
                    "🔎 Fundamental Researcher":"Analyze supplied company information, business model, revenue, profitability, strengths, and weaknesses.",
                    "⚠️ Risk Analyst":"Identify and rank financial, market, operational, competitive, and regulatory risks.",
                    "🧠 MarketMind Full Investigation":"Combine market, sentiment, fundamental, and risk perspectives into one structured investigation."
                }
                llm = ChatOpenAI(model=model, temperature=temperature, api_key=st.session_state.api_key)
                response = llm.invoke([
                    SystemMessage(content=roles[agent]),
                    HumanMessage(content=f"Task:\n{prompt}\n\nSupplied context:\n{context or 'None'}\n\nClearly separate supplied facts from inference. Do not claim real-time data unless supplied. Do not provide personalized financial advice.")
                ])
                st.success("Analysis completed.")
                st.markdown(response.content)
            except Exception as e:
                st.error("The AI analysis could not be completed.")
                st.exception(e)

with tabs[1]:
    st.subheader("📊 Market Dashboard")
    st.info("This dashboard is input-driven. It does not claim to provide live prices without a connected market-data API.")
    c1,c2,c3=st.columns(3)
    c1.metric("Selected Agent", agent.split(" ",1)[-1])
    c2.metric("AI Model", model)
    c3.metric("Session", datetime.now().strftime("%H:%M"))
    company=st.text_input("Company / Market")
    metric=st.text_input("Price / Key Metric")
    trend=st.selectbox("Observed Trend",["Bullish","Neutral","Bearish","Unknown"])
    note=st.text_area("Observation")
    if st.button("➕ Add Snapshot"):
        if company:
            st.session_state.setdefault("snapshots",[]).append({"Company/Market":company,"Metric":metric,"Trend":trend,"Observation":note})
            st.success("Snapshot added.")
    if st.session_state.get("snapshots"):
        st.dataframe(st.session_state["snapshots"], use_container_width=True)

with tabs[2]:
    st.subheader("📚 MarketMind Notes")
    st.markdown("""
### Agentic AI
An agentic AI application uses task-oriented AI workflows or specialized roles to accomplish a goal.

### RAG vs Agentic AI
**RAG** retrieves relevant information before generation. **Agentic AI** focuses on completing tasks through specialized workflows and can be extended with tools.

### MarketMind Agents
- Market Analyst — trends and opportunities
- News & Sentiment Analyst — supplied news/text
- Fundamental Researcher — company fundamentals
- Risk Analyst — risk identification
- Full Investigation — combines perspectives

### Important Limitation
AI can make mistakes. Market information changes quickly, so important claims should be verified.

### Financial Safety
This is an educational project, not financial advice.
""")

with tabs[3]:
    st.subheader("🎓 Project Presentation")
    st.markdown("""
## MarketMind — Agentic Market Intelligence

**1. Problem:** Market research involves large amounts of information and different analytical tasks.

**2. Solution:** MarketMind provides a single AI workspace with specialized market-analysis agents.

**3. Agentic Concept:** Market, sentiment, fundamental, risk, and full-investigation roles.

**4. Technologies:** Python, Streamlit, LangChain, OpenAI, and optional future market/news APIs.

**5. Security:** Locked interface, user-provided API key, no hard-coded secrets.

**6. Limitations:** AI may be inaccurate; real-time data is not assumed unless connected.

**7. Future Work:** Real-time data, news retrieval, financial-report RAG, multi-agent orchestration, citations, charts, and portfolio analytics.
""")
    if PRESENTATION_URL.startswith("http"):
        st.link_button("📊 Open Full Presentation", PRESENTATION_URL)
    else:
        st.warning("Replace PRESENTATION_URL in app.py with your presentation link.")

with tabs[4]:
    st.subheader("🎥 Project Demo Video")
    if DEMO_VIDEO_URL.startswith("http"):
        st.video(DEMO_VIDEO_URL)
    else:
        st.info("Replace DEMO_VIDEO_URL in app.py after uploading your demo video.")

with tabs[5]:
    st.subheader("ℹ️ About MarketMind")
    st.write("MarketMind is an educational agentic AI project demonstrating specialized AI roles, secure API-key handling, prompt design, and market-research workflows.")

st.markdown('<div class="footer">MarketMind • Agentic Market Intelligence • Educational Project</div>', unsafe_allow_html=True)
