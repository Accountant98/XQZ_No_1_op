import streamlit as st

# Hiển thị một nút trong ứng dụng Streamlit
confirmation_button = st.button("Nhấn vào đây để thực hiện xử lý")

# JavaScript để tạo hộp thoại xác nhận khi nút được nhấn
if confirmation_button:
    confirmation = st.button("Xác nhận xử lý")
    if confirmation:
        # Thực hiện xử lý của bạn ở đây
        st.write("Xử lý đã được thực hiện thành công!")
