import pandas as pd
import numpy as np

def tao_file_up_web(df_thucte: pd.DataFrame, df_up_web: pd.DataFrame, tuan_input: str, thang_input: str):
    
    #Set lai cot cho df_up_web de dam bao khop voi file up web
    df_up_web.columns = ['Tuần', 'VNEDU', 'Lớp học', 'Họ và tên', 'Ngày sinh','Điểm rèn luyện'] + [f'Tháng {i}' for i in range(1, 6)]

    #Them cot Loi_format vao df_thucte de luu tru thong tin loi format sau khi xu ly (Loi voi so lan kem theo)
    #VD: • Nghỉ phép - 1 lần
    df_thucte['Loi_format'] = np.where(
        df_thucte['Số lần'] == 0, 
        "• Không có lỗi vi phạm tuần này", # Giá trị nếu đúng là 0
        "• " + df_thucte['Hình thức'] + " - " + df_thucte['Số lần'].astype(str) + " lần" # Giá trị nếu khác 0
    )

    #Tao ra 1 bang moi gom Ma HS, Loi format (da xu ly) va Tong diem de tien cho viec update vao file up web
    df_thucte_grouped = df_thucte.groupby('Mã học sinh').agg({'Loi_format': lambda x: '\n'.join(x), 'Tổng': 'sum'}).reset_index()

    #Chuyen doi kieu du lieu de dam bao khop khi update vao file up web
    df_up_web['VNEDU'] = df_up_web['VNEDU'].astype(str) 
    df_thucte_grouped['Mã học sinh'] = df_thucte_grouped['Mã học sinh'].astype(str) 
    df_up_web[f'{thang_input}'] = df_up_web[f'{thang_input}'].astype(object)
    df_up_web['Điểm rèn luyện'] = df_up_web['Điểm rèn luyện'].astype(object)

    for index, row in df_thucte_grouped.iterrows():
        mshs = row['Mã học sinh']
        loi_format = row['Loi_format']

        condition = (df_up_web['VNEDU'] == mshs) & (df_up_web['Tuần'] == tuan_input)
        tong_diem = (df_up_web['VNEDU'] == mshs) & (df_up_web['Tuần'] == 'Điểm')
        if tong_diem.any():
            gia_tri_hien_tai = df_up_web.loc[tong_diem, f'{thang_input}']
            gia_tri_tong_hien_tai = df_up_web.loc[tong_diem, 'Điểm rèn luyện']
            # 2. Chuyển đổi giá trị hiện tại sang số (Nếu lỗi hoặc trống thì coi là 0)
            # pd.to_numeric với errors='coerce' sẽ biến văn bản thành NaN, sau đó fillna(0) biến nó thành số 0
            gia_tri_so = pd.to_numeric(gia_tri_hien_tai, errors='coerce').fillna(0)
            gia_tri_so_tong_hien_tai = pd.to_numeric(gia_tri_tong_hien_tai, errors='coerce').fillna(0)

            # 3. Thực hiện phép cộng và gán ngược lại
            df_up_web.loc[tong_diem, f'{thang_input}'] = gia_tri_so + float(row['Tổng'])
            df_up_web.loc[tong_diem, 'Điểm rèn luyện'] = gia_tri_so_tong_hien_tai + float(row['Tổng'])
            # df_up_web.loc[tong_diem, f'{thang_input}'] = df_up_web.loc[tong_diem, f'{thang_input}'] + row['Tổng']
        if condition.any():
            df_up_web.loc[condition, f'{thang_input}'] = loi_format

    df_up_web['Điểm rèn luyện'] = df_up_web['Điểm rèn luyện'].astype(str)
    df_up_web[f'{thang_input}'] = df_up_web[f'{thang_input}'].astype(str)


    # 2. Xử lý các giá trị NaN/None nếu có để bảng trông sạch hơn
    df_up_web['Điểm rèn luyện'] = df_up_web['Điểm rèn luyện'].replace(['nan', 'None', 'NaN'], '')
    df_up_web[f'{thang_input}'] = df_up_web[f'{thang_input}'].replace(['nan', 'None', 'NaN'], '')
    return df_up_web
