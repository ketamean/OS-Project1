1. Trong các file có các class, mỗi class sẽ bao gồm một số method
    các method có "raise NotImplementedError" là các abstract method, không gọi được và có vai trò như interface
    các method có "pass" là một số method gợi ý có thể gọi nhưng chưa được implement, nếu cần thì implement sau đó nếu ai cần (chứ hiện tại cũng chưa hình dung được nó nên implement ra sao :)))

2. Khi chọn partition xong thì xây hết directory tree của partition đó luôn (giữ thông tin các file, folder và data nếu là text {nếu không phải text thì None => cho chọn tool đọc})

3. Khi implement, các class có AbstractClass làm interface (như OSItem đại diện cho OSFile và OSFolder) khi có thêm các properties riêng thì cần note ra và chú thích tương tự như template có sẵn. Cú pháp:
    ```python
    var_name    = initial_value_represent_the_datatype       # [datatype] chức năng
    ```

    có gì tab cho đều đẹp dễ đọc :))

4. Trong file PartitionType.py:
    - AbstractPartition chỉ có sẵn các thông tin chung cho partition và được lấy ý tưởng từ bảng bootsector của FAT32.
    - Khi làm việc, nếu NTFS hoặc FAT32 có sự thêm thông tin gì riêng thì chủ động thêm
 
5. Trong file OSItem.py:
    - Hiện chưa chắc chắn lắm về behaviour của method access(): không biết nên cho nó hoạt động ra sao và trả về giá trị gì
    - Nếu có ý tưởng implement thì note that behaviour của access() ở class OSFile và OSFolder cần tương đồng nhau và cần có cùng số lượng return values

## Hướng dẫn cách chạy chương trình
1. Clone repo này về từ Github
2. `cd` vào trong repo và sử dụng các câu lệnh sau để khởi tạo môi trường ảo
- `py -3 -m venv .venv`
- `.venv\Scripts\activate`
3. Tải các package về với câu lệnh `pip install -r requirements.txt`
4. `cd` vào `src` và khởi chạy file `main.py` để bắt đầu chương trình.