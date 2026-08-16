import streamlit as st
import pandas as pd
from datetime import datetime

# --- إعدادات صفحة الموقع ---
st.set_page_config(page_title="نظام المتابعة الفنية - ريموتك", page_icon="📡", layout="wide")

# --- ترويسة الموقع ---
st.markdown("<h1 style='text-align: center; color: #1f77b4;'>شركة ريموتك للاتصالات والأنظمة الذكية</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>بوابة المتابعة الفنية (FTTH / WiFiber) - منطقة خلة المية</h3>", unsafe_allow_html=True)
st.markdown("---")

# ملاحظة: عند رفع الموقع على الإنترنت، سنقوم بتغيير هذا المسار ليتصل بـ Google Sheets
FILE_PATH = "ملف المتابعة الفنية -  خلة المية.xlsx"
SHEET_NAME = "Remotech1-1"

# --- دالة جلب البيانات ---
@st.cache_data(ttl=30)
def load_data():
    try:
        return pd.read_excel(FILE_PATH, sheet_name=SHEET_NAME)
    except Exception as e:
        st.error("تعذر الاتصال بقاعدة البيانات.")
        return pd.DataFrame()

df = load_data()

# --- تبويبات الموقع (Tabs) ---
tab1, tab2 = st.tabs(["📋 استعراض السجلات الحالية", "➕ إضافة زيارة فنية جديدة"])

# --- التبويب الأول: القراءة ---
with tab1:
    st.subheader("سجل الزيارات الفنية")
    # شريط بحث بسيط
    search_query = st.text_input("🔍 ابحث برقم الهوية أو اسم المشترك:")
    
    if search_query:
        # تصفية البيانات بناءً على البحث
        filtered_df = df[df.astype(str).apply(lambda x: x.str.contains(search_query, case=False, na=False)).any(axis=1)]
        st.dataframe(filtered_df, use_container_width=True)
    else:
        st.dataframe(df, use_container_width=True)

# --- التبويب الثاني: الإضافة ---
with tab2:
    st.subheader("إدخال تفاصيل الزيارة")
    
    with st.form("new_entry_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            id_num = st.number_input("الرقم التسلسلي", min_value=1, step=1)
            customer_name = st.text_input("اسم المشترك")
            id_card = st.text_input("رقم الهوية")
            mobile_num = st.text_input("رقم الجوال")
            
        with col2:
            visit_date = st.date_input("التاريخ")
            team = st.selectbox("فريق العمل", ["مؤمن", "عبد الله", "فريق آخر"])
            work_type = st.selectbox("طبيعة العمل", ["تركيب جديد", "صيانة", "نقل خدمة"])
            service_type = st.selectbox("نوع الخدمة", ["سلكي FTTH", "لا سلكي WiFiber"])
            
        with col3:
            region = st.text_input("المنطقة", value="خلة المية")
            olt = st.text_input("جهاز OLT")
            main_box = st.text_input("رقم الصندوق الرئيسي")
            sub_box = st.text_input("رقم الصندوق الفرعي")
            
        st.markdown("---")
        col4, col5 = st.columns(2)
        with col4:
            sn = st.text_input("السيريال نمبر (SN)")
            splitting = st.text_input("نوع الحشوة Splitting")
        with col5:
            status = st.selectbox("حالة الزيارة", ["تم التركيب", "قيد الانتظار", "تأجيل", "ملغى"])
            notes = st.text_area("ملاحظات إضافية")
            
        submitted = st.form_submit_button("إرسال وحفظ البيانات 💾")
        
        if submitted:
            # هنا يتم كتابة كود الحفظ (سيتم تفعيله ليتصل بالسحابة عند رفع الموقع)
            st.success(f"تم تسجيل الزيارة للمشترك {customer_name} بنجاح!")
