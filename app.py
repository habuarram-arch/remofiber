import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import json

# --- إعدادات صفحة الموقع ---
st.set_page_config(page_title="نظام المتابعة الفنية - ريموتك", page_icon="📡", layout="wide")

st.markdown("<h1 style='text-align: center; color: #1f77b4;'>شركة ريموتك للاتصالات والأنظمة الذكية</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>بوابة المتابعة الفنية (FTTH / WiFiber) - منطقة خلة المية</h3>", unsafe_allow_html=True)
st.markdown("---")

# --- دالة الاتصال بقاعدة البيانات السحابية ---
@st.cache_resource
def get_google_sheet():
    # قراءة المفاتيح السرية من إعدادات الموقع
    creds_dict = json.loads(st.secrets["google_credentials"])
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    client = gspread.authorize(creds)
    
    # فتح الملف والورقة المحددة
    sheet_url = st.secrets["sheet_url"]
    workbook = client.open_by_url(sheet_url)
    return workbook.worksheet("Remotech1-1")

# --- دالة قراءة البيانات ---
def load_data():
    sheet = get_google_sheet()
    data = sheet.get_all_records()
    return pd.DataFrame(data)

df = load_data()

# --- تبويبات الموقع ---
tab1, tab2 = st.tabs(["📋 استعراض السجلات الحالية", "➕ إضافة زيارة فنية جديدة"])

# --- التبويب الأول: القراءة ---
with tab1:
    st.subheader("سجل الزيارات الفنية")
    search_query = st.text_input("🔍 ابحث برقم الهوية أو اسم المشترك:")
    if search_query:
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
            id_num = st.number_input("الرقم", min_value=1, step=1)
            customer_name = st.text_input("اسم المشترك")
            id_card = st.text_input("رقم الهوية")
            mobile_num = st.text_input("رقم الجوال")
            
        with col2:
            visit_date = st.date_input("التاريخ")
            team = st.selectbox("الفريق", ["مؤمن", "عبد الله", "فريق آخر"])
            work_type = st.selectbox("طبيعة العمل", ["تركيب جديد", "صيانة", "نقل خدمة", "أخرى"])
            service_type = st.selectbox("نوع الخدمة", ["سلكي FTTH", "لا سلكي WiFiber"])
            
        with col3:
            region = st.text_input("المنطقة", value="خلة المية")
            olt = st.text_input("OLT")
            main_box = st.text_input("رقم الصندوق الرئيسي")
            sub_box = st.text_input("رقم الصندوق الفرعي")
            
        st.markdown("---")
        col4, col5 = st.columns(2)
        with col4:
            sn = st.text_input("السيريال نمبر (SN)")
            splitting = st.text_input("نوع الحشوة Splitting")
        with col5:
            status = st.selectbox("حالة الزيارة", ["تم التركيب", "قيد الانتظار", "تأجيل", "ملغى"])
            notes = st.text_area("ملاحظات")
            
        submitted = st.form_submit_button("إرسال وحفظ البيانات 💾")
        
        if submitted:
            sheet = get_google_sheet()
            headers = sheet.row_values(1)
            row_data = [""] * len(headers)
            
            # مطابقة البيانات المدخلة مع أعمدة ملف الإكسيل بدقة
            def assign_val(col_name, val):
                if col_name in headers:
                    row_data[headers.index(col_name)] = val

            assign_val("الرقم ", id_num)
            assign_val("اسم المشترك ", customer_name)
            assign_val("رقم الهوية ", id_card)
            assign_val("رقم الجوال ", mobile_num)
            assign_val("التاريخ ", str(visit_date))
            assign_val("الفريق", team)
            assign_val("طبيعة العمل ", work_type)
            assign_val("نوع الخدمة", service_type)
            assign_val("المنطفة ", region)
            assign_val("OLT", olt)
            assign_val("رقم الصندوق الرئيسي ", main_box)
            assign_val("رقم الصندوق الفرعي ", sub_box)
            assign_val("SN", sn)
            assign_val("نوع الحشوة Splitting ", splitting)
            assign_val("حالة الزيارة ", status)
            assign_val("ملاحظة ", notes)

            # حفظ الصف الجديد
            sheet.append_row(row_data)
            st.success(f"✅ تم تسجيل الزيارة للمشترك {customer_name} بنجاح!")
