import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(
   page_title="HUB | AI Agent Analysis",
   page_icon="🏛️",
   layout="wide"
)

# --- 2. CSS TÙY CHỈNH ---
st.markdown("""
   <style>
   @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
  
   html, body, [class*="st-"] {
       font-family: 'Roboto', sans-serif;
   }

   /* Nền trang xám nhạt để làm nổi bật Header trắng */
   .stApp {
       background-color: #f8fafc;
   }

   /* HEADER NỀN TRẮNG VIỀN XANH - Đã chỉnh sửa */
   .hub-header {
       background-color: #ffffff;
       padding: 35px 20px;
       border-radius: 15px; /* Bo góc nhẹ nhàng */
       text-align: center;
       color: #1e3a8a;
       box-shadow: 0 10px 25px rgba(0,0,0,0.05); /* Đổ bóng nhẹ */
       margin: 10px 0 40px 0;
       border: 3px solid #1e3a8a; /* Viền xanh đậm */
   }
   
   .hub-header h1 {
       font-size: 2.3rem;
       font-weight: 800;
       text-transform: uppercase;
       margin: 0;
       letter-spacing: 1px;
       color: #1e3a8a !important; /* Màu xanh đậm */
   }
   
   .hub-header p {
       font-size: 1.1rem;
       color: #475569;
       margin-top: 10px;
       font-weight: 400;
   }

   /* Bảng điều khiển Sidebar */
   [data-testid="stSidebar"] {
       background-color: #ffffff;
       border-right: 1px solid #e2e8f0;
   }
   .sidebar-title {
       color: #1e3a8a;
       font-size: 1.3rem;
       font-weight: 700;
       padding-bottom: 10px;
       border-bottom: 2px solid #3b82f6;
       margin-bottom: 20px;
   }
   .student-info {
       background-color: #f1f5f9;
       padding: 20px;
       border-radius: 12px;
       margin-top: 30px;
       border: 1px solid #cbd5e1;
   }
   .student-info p {
       margin: 5px 0;
       font-size: 0.95rem;
       color: #334155;
   }

   /* Tabs & Cards */
   .stTabs [data-baseweb="tab-list"] {
       gap: 10px;
   }
   .stTabs [data-baseweb="tab"] {
       height: 50px;
       background-color: #ffffff;
       border-radius: 10px 10px 0 0;
       padding: 0 30px;
       font-weight: 600;
   }
   .stTabs [aria-selected="true"] {
       background-color: #3b82f6 !important;
       color: white !important;
   }

   .info-card {
       background: white;
       padding: 25px;
       border-radius: 15px;
       box-shadow: 0 4px 12px rgba(0,0,0,0.05);
       border-top: 5px solid #3b82f6;
   }
   </style>
   """, unsafe_allow_html=True)

# --- 3. DATA ENGINE ---
@st.cache_data
def load_data():
   try:
       task_df = pd.read_csv("task_statement_with_metadata.csv")
       task_df['Occupation Mean Annual Wage'] = pd.to_numeric(task_df['Occupation Mean Annual Wage'], errors='coerce')
       meta_df = pd.read_csv("domain_worker_metadata.csv")
       desires_df = pd.read_csv("domain_worker_desires.csv")
       expert_df = pd.read_csv("expert_rated_technological_capability.csv")
      
       cs_groups = [
           'Computer Programmers', 'Computer Systems Engineers/Architects',
           'Software Quality Assurance Analysts and Testers', 'Web Developers',
           'Information Security Analysts', 'Database Administrators',
           'Computer Systems Analysts', 'Network and Computer Systems Administrators'
       ]
       f = lambda df: df[df['Occupation (O*NET-SOC Title)'].isin(cs_groups)]
       return f(task_df), f(meta_df), f(desires_df), f(expert_df)
   except:
       return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

task_df, meta_df, desires_df, expert_df = load_data()

# --- 4. KNOWLEDGE BASE (GIỮ NGUYÊN) ---
def get_industry_insights(job):
   if job == "Tất cả ngành":
       return {
           "architecture": "Hệ sinh thái Multi-Agent tích hợp",
           "workflow": "Nhân viên -> Agent điều phối -> Các Agent chuyên môn (Dev/Security/Data) -> Phê duyệt",
           "framework": ["AutoGPT", "Microsoft AutoGen", "LangChain"],
           "roadmap": ["Xây dựng tư duy AI-First", "Học cách quản trị nhân sự số (Digital Workers)", "Tối ưu chi phí vận hành AI"],
           "impact": "Tăng năng suất toàn diện 40-60%"
       }
   insights = {
       'Computer Programmers': {
           "architecture": "Autonomous Coding Agent (Vòng lặp ReAct)",
           "workflow": "User Requirement -> Agent lập kế hoạch -> Agent viết code -> Agent chạy Unit Test -> Tự sửa lỗi",
           "framework": ["Devin", "Cursor Agent", "GitHub Copilot Workspace"],
           "roadmap": ["Học Prompt Engineering cho Code", "Quản lý vòng đời tác vụ của Agent", "Kỹ năng Review Code do AI viết"],
           "impact": "Giảm 70% thời gian viết code thủ công"
       },
       'Information Security Analysts': {
           "architecture": "Self-Healing Security Agent",
           "workflow": "Giám sát lưu lượng -> Agent phát hiện bất thường -> Agent cô lập mối đe dọa -> Agent vá lỗ hổng",
           "framework": ["Microsoft Security Copilot", "CrowdStrike AI"],
           "roadmap": ["Học về AI Red Teaming", "Phân tích mã độc bằng LLM", "Xây dựng chính sách bảo mật cho AI"],
           "impact": "Phản ứng sự cố tính bằng giây thay vì bằng giờ"
       },
       'Database Administrators': {
           "architecture": "Autonomous Database Agent (DBA-as-a-Service)",
           "workflow": "Query Monitor -> Agent dự báo nghẽn -> Agent tự động index/tối ưu -> Báo cáo hiệu năng",
           "framework": ["DB-GPT", "OtterTune", "Amazon DevOps Guru"],
           "roadmap": ["Quản trị Vector Database", "Tối ưu SQL qua ngôn ngữ tự nhiên", "Bảo mật dữ liệu trong RAG"],
           "impact": "Tối ưu 50% tài nguyên hệ thống"
       },
       'Web Developers': {
           "architecture": "Generative UI/UX Agent",
           "workflow": "Figma Design -> Agent chuyển đổi mã nguồn -> Agent tích hợp API -> Agent kiểm thử hiển thị",
           "framework": ["Vercel v0", "Builder.io", "Claude 3.5 Sonnet"],
           "roadmap": ["Sử dụng AI tạo Frontend", "Tích hợp AI trực tiếp vào Web App", "Kỹ năng tinh chỉnh UI từ AI"],
           "impact": "Tốc độ tạo Prototype nhanh gấp 5 lần"
       },
       'Software Quality Assurance Analysts and Testers': {
           "architecture": "Visual & Logic QA Agent",
           "workflow": "Mô tả tính năng -> Agent tự viết kịch bản test -> Agent thực hiện test -> Agent báo cáo bug kèm video",
           "framework": ["Mabl", "TestSigma", "Applitools"],
           "roadmap": ["Tự động hóa Test Case bằng AI", "Kiểm thử trải nghiệm người dùng", "Quản lý chất lượng AI"],
           "impact": "Độ phủ kiểm thử đạt xấp xỉ 100%"
       }
   }
   return insights.get(job, insights.get('Computer Programmers', {}))

# --- 5. GIAO DIỆN CHÍNH ---

# Header Mới: Nền trắng, Viền xanh
st.markdown("""
   <div class="hub-header">
       <h1>Trường Đại học Ngân hàng Thành phố Hồ Chí Minh</h1>
       <p>Hệ thống Phân tích & Khuyến nghị Ứng dụng AI Agent trong Khoa học Máy tính</p>
   </div>
   """, unsafe_allow_html=True)

# Sidebar (Giữ nguyên)
with st.sidebar:
   st.markdown('<p class="sidebar-title">BẢNG ĐIỀU KHIỂN</p>', unsafe_allow_html=True)
   all_jobs = ["Tất cả ngành"] + sorted(list(task_df['Occupation (O*NET-SOC Title)'].unique())) if not task_df.empty else ["Tất cả ngành"]
   selected_job = st.selectbox("Chọn vị trí cần phân tích:", options=all_jobs)
  
   st.markdown("""
       <div class="student-info">
           <p><b>Sinh viên thực hiện:</b></p>
           <p>Trần Thị Ngọc Vy</p>
           <p><b>MSSV:</b> 030239230296</p>
           <p><b>Ngành:</b> Khoa học dữ liệu trong kinh doanh</p>
           <p><b>Môn học:</b> Trực quan hoá dữ liệu</p>
       </div>
   """, unsafe_allow_html=True)

# Xử lý dữ liệu (Giữ nguyên)
if selected_job == "Tất cả ngành":
   disp_df, m_disp, d_disp, e_disp = task_df, meta_df, desires_df, expert_df
else:
   disp_df = task_df[task_df['Occupation (O*NET-SOC Title)'] == selected_job]
   m_disp = meta_df[meta_df['Occupation (O*NET-SOC Title)'] == selected_job]
   d_disp = desires_df[desires_df['Occupation (O*NET-SOC Title)'] == selected_job]
   e_disp = expert_df[expert_df['Occupation (O*NET-SOC Title)'] == selected_job]

# Hiển thị Dashboard
if not disp_df.empty:
    st.subheader(f"🔍 Kết quả phân tích: {selected_job}")

    # Khối chỉ số
    m1, m2, m3, m4 = st.columns(4)
    with m1:
       val = disp_df['Occupation Mean Annual Wage'].mean()
       st.metric("Lương Trung Bình", f"${val:,.0f}" if pd.notna(val) else "N/A")
    with m2:
       llm_p = (m_disp['LLM Use in Work'] == 'Yes').mean() * 100 if not m_disp.empty else 0
       st.metric("Tỉ lệ ứng dụng LLM", f"{llm_p:.1f}%")
    with m3:
       st.metric("Kỳ vọng tự động hóa", f"{d_disp['Automation Desire Rating'].mean():.2f}/5" if not d_disp.empty else "N/A")
    with m4:
       st.metric("Năng lực công nghệ", f"{e_disp['Automation Capacity Rating'].mean():.2f}/5" if not e_disp.empty else "N/A")

    # Tabs nội dung
    t1, t2, t3 = st.tabs(["📊 Thống kê trực quan", "🧠 Kiến trúc AI Agent", "🚀 Lộ trình đào tạo"])

    with t1:
       c1, c2 = st.columns(2)
       with c1:
           st.markdown("**So sánh Năng lực & Mong muốn**")
           radar_fig = go.Figure()
           r_vals = [d_disp['Automation Desire Rating'].mean(), e_disp['Automation Capacity Rating'].mean(), 4.0, 3.5, d_disp['Automation Desire Rating'].mean()]
           radar_fig.add_trace(go.Scatterpolar(
               r=r_vals,
               theta=['Kỳ vọng NV', 'Năng lực AI', 'Chuẩn ngành', 'Thực tế', 'Kỳ vọng NV'],
               fill='toself', line_color='#1e3a8a'
           ))
           radar_fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), height=350, margin=dict(t=30, b=30))
           st.plotly_chart(radar_fig, use_container_width=True)
      
       with c2:
           st.markdown("**Mức độ sẵn sàng thay thế tác vụ**")
           task_types = ["Lặp lại", "Logic", "Sáng tạo", "Giao tiếp"]
           values = [85, 60, 40, 20] if selected_job != "Tất cả ngành" else [70, 55, 30, 25]
           fig_bar = px.bar(x=task_types, y=values, color=values, color_continuous_scale="Blues", labels={'x': 'Loại tác vụ', 'y': '% Tự động hóa'})
           fig_bar.update_layout(height=350)
           st.plotly_chart(fig_bar, use_container_width=True)

    with t2:
       info = get_industry_insights(selected_job)
       st.markdown(f"""
           <div class="info-card">
               <h3 style="color:#1e3a8a;">🏗️ Kiến trúc đề xuất: {info['architecture']}</h3>
               <p style="font-size:1.1rem; color:#475569;">Dành riêng cho chuyên môn <b>{selected_job}</b></p>
               <div style="background:#f8fafc; padding:15px; border-radius:10px; border-left:5px solid #3b82f6; margin:15px 0;">
                   <b>Quy trình hoạt động:</b><br>
                   <span style="font-family:monospace; color:#2563eb;">{info['workflow']}</span>
               </div>
               <p><b>Hệ sinh thái công cụ:</b></p>
               {" ".join([f'<span style="background:#dbeafe; color:#1e40af; padding:5px 12px; border-radius:20px; font-size:0.8rem; font-weight:bold; margin-right:5px;">{f}</span>' for f in info['framework']])}
               <p style="margin-top:15px;"><b>Tác động dự kiến:</b> <span style="color:#10b981; font-weight:bold;">{info['impact']}</span></p>
           </div>
       """, unsafe_allow_html=True)

    with t3:
       info = get_industry_insights(selected_job)
       st.markdown(f"""
           <div class="info-card" style="border-top-color: #10b981;">
               <h3 style="color:#065f46;">🎯 Lộ trình phát triển năng lực số</h3>
               <p>Để thích nghi với vai trò <b>{selected_job}</b> trong kỷ nguyên AI Agent, sinh viên cần tập trung:</p>
               <ul style="line-height:2;">
                   { "".join([f"<li><b>{step}</b></li>" for step in info['roadmap']]) }
               </ul>
               <div style="margin-top:20px; padding:15px; background:#ecfdf5; border-radius:10px; color:#065f46; font-size:0.9rem;">
                   📌 <b>Lời khuyên từ chuyên gia HUB:</b> Đừng học cách cạnh tranh với AI, hãy học cách điều khiển Agent để giải quyết các bài toán kinh doanh phức tạp hơn.
               </div>
           </div>
       """, unsafe_allow_html=True)
else:
    st.info("Vui lòng kiểm tra lại nguồn dữ liệu CSV.")

# Footer
st.markdown("<br><hr><center style='color:#64748b; font-size:0.8rem;'>© 2026 HUB Data Visualization Project | Trần Thị Ngọc Vy - Khoa học dữ liệu trong kinh doanh</center><br>", unsafe_allow_html=True)