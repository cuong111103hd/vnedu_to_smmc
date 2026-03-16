import pandas as pd

data = {
    'Hình thức': [
        'Không có lỗi vi phạm tuần này', 'Nghỉ phép', 'Nghỉ không phép', 
        'Muộn giờ truy bài', 'Muộn sau giờ vào lớp - 15', 'Muộn sau giờ vào lớp - 45', 
        'Lỗi đồng phục', 'Không đội mũ bảo hiểm', 'Ăn trong giờ', 'Xe trên 50cm3', 
        'Lái xe không đủ tuổi', 'Đi xe sân trường', 'Sử dụng điện thoại', 
        'Mất trật tự giờ học', 'Ngủ trong giờ', 'Làm việc riêng', 'Không ghi chép bài', 
        'Thiếu đồ dùng học tập', 'Không thuộc, học bài về nhà', 'Nói tục, chửi bậy', 
        'Bạo lực học đường', 'Thể dục giữa giờ', 'Mât trật tự truy bài', 
        'Đi lại tự do giờ truy bài', 'Ngồi sai sơ đồ lớp', 'Giả mạo chữ kí', 
        'Khai sai tên vi phạm', 'Thuốc lá điện tử', 'Chống đối cán bộ trực ban', 
        'Sang khu vực cấm', 'Hỏng CSVC', 'ĐHM trèo cổng, sai cổng', 
        'Tự ý ra khỏi cổng trưởng', 'Mua bán hàng hóa', 'Ra về giữa buổi học', 
        'Bỏ tiết', 'VP kiểm tra tại lớp', 'Vào lớp muộn truy bài', 
        'Vào lớp muộn tiết học', 'Vô lễ với giáo viên', 'Phê bình trước cờ', 
        'Kiểm tra: Mất trật tự', 'Giao nộp đồ nhặt được', 'Hỗ trợ giáo viên', 
        'Điểm tốt', 'Xe không gương', 'Xe không biển', 'Ý thức kém', 'Không chú ý'
    ],
    'Điểm': [
        0, -1, -5, -2, -3, -4, -3, -3, -3, -10, -10, -2, -5, -3, -3, -3, -3, 
        -2, -3, -5, -15, -2, -1, -1, -1, -10, -7, -15, -5, -5, -2, -5, -5, 
        -3, -1, -5, -3, -1, -2, -5, -5, -5, 5, 2, 3, -3, -3, -3, -3
    ]
}

# Tạo DataFrame
df_quydoi = pd.DataFrame(data)


# def frequency(diem, loi):
#     if diem == 0:
#         return 0
#     if loi == 'Nghỉ học có phép cả ngày (P)' or loi == 'Nghỉ học có phép chiều (CP)' or loi == 'Nghỉ học có phép sáng (CP)':
#         return 1
#     else:
#         return 

# Danh sách các biến thể của lỗi "Nghỉ học có phép"



df_thucte = pd.read_csv("test.csv")


df_thucte.columns = ['STT', 'Mã học sinh', 'Họ và tên', 'Lớp','Hình thức','Ghi chú', 'Ngày', 'NaN', 'Tổng', 'Điểm Thi đua']


bien_the_nghi_phep = [
    'Nghỉ học có phép cả ngày (P)', 
    'Nghỉ học có phép chiều (CP)', 
    'Nghỉ học có phép sáng (CP)'
]

# Thay thế tất cả các biến thể này thành "Nghỉ phép"
df_thucte['Lỗi_Chuan'] = df_thucte['Hình thức'].replace(bien_the_nghi_phep, 'Nghỉ phép')

df_thucte['STT'] = pd.to_numeric(df_thucte.iloc[:,0], errors='coerce')

df_thucte['Tổng'] = pd.to_numeric(df_thucte['Tổng'], errors='coerce')

df_thucte = df_thucte.dropna(subset=['STT'])

df_thucte = df_thucte.drop(columns=['STT'])

# Sau đó bạn thực hiện Map và tính toán trên cột 'Lỗi_Chuan' này
tra_cuu_diem = df_quydoi.set_index('Hình thức')['Điểm']
diem_don_vi = df_thucte['Lỗi_Chuan'].map(tra_cuu_diem)

# Tính số lần và chèn vào vị trí mong muốn
so_lan_values = (df_thucte['Tổng'] / diem_don_vi).abs().fillna(0).astype(int)
df_thucte.insert(df_thucte.columns.get_loc('Hình thức') + 1, 'Số lần', so_lan_values)

df_thucte.drop(columns=['Lỗi_Chuan'], inplace=True)

df_thucte.to_excel("output.xlsx", index=False)
print(df_thucte)
