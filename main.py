import streamlit as st
import pandas as pd
import io
import pandas as pd

import preprocessing
from processing import tao_file_up_web

if __name__ == "__main__":
    st.title("Phần mềm Xử lý Vi phạm Học sinh")

    danh_sach_tuan = [str(i) for i in range(1, 6)]
    danh_sach_thang = [f'Tháng {j}' for j in range(1,6)]
    
    # 1. Giao diện chọn file
    uploaded_file = st.file_uploader("Chọn file Excel dữ liệu tuần này", type=["xls"])
    uploaded_file_pre = st.file_uploader("Chọn file CSV dữ liệu up web tuần trước", type=["csv"])

    input_tuan = st.selectbox(
        "Chọn số tuần cần xử lý:",
        options=danh_sach_tuan,
        index=0  # Mặc định chọn phần tử đầu tiên (Tuần 1)
    )
    input_thang = st.selectbox(
        "Chọn số tháng cần xử lý:",
        options=danh_sach_thang,
        index=0  # Mặc định chọn phần tử đầu tiên (Tháng 1)
    )

    if uploaded_file is not None and uploaded_file_pre is not None:
        # 2. Đọc dữ liệu
        df1 = pd.read_excel(uploaded_file, engine='calamine')
        df_up_web = pd.read_csv(uploaded_file_pre)
        
        st.write("Xem trước dữ liệu đã tải lên:")
        st.dataframe(df1.head())

        if st.button("Bắt đầu xử lý"):
            # --- CHÈN LOGIC XỬ LÝ CỦA BẠN VÀO ĐÂY ---
            # Giả sử sau khi xử lý bạn có df_ketqua
            df_thucte = preprocessing.xu_ly_du_lieu(df1)
            df_ketqua = tao_file_up_web(df_thucte, df_up_web, input_tuan,input_thang)
            
            # Ví dụ logic bạn đã viết:
            # df_ketqua['Loi_format'] = np.where(...) 
            
            st.success("Xử lý thành công!")
            st.write("Dữ liệu sau khi xử lý:")
            st.dataframe(df_ketqua.head())

            # 3. Xuất file để tải về
            # Dùng BytesIO để tạo file trong bộ nhớ mà không cần lưu xuống ổ cứng
            towrite = io.BytesIO()
            df_ketqua.to_csv(towrite, index=False, encoding='utf-8-sig')
            towrite.seek(0)
            
            st.download_button(
                label="Tải file kết quả (CSV)",
                data=towrite,
                file_name=f"Ket_qua_Tuan_{input_tuan}_{input_thang}.csv",
                mime="text/csv"
            )