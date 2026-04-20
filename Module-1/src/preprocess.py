import re
import pandas as pd
import emoji

class TextCleaner:
    def __init__(self, dict_path):
        df_dict = pd.read_excel(dict_path)
        
        # CHỈ nạp những từ có Phân loại là 'Viết tắt' vào từ điển replace
        # Những từ 'Viết lóng' sẽ KHÔNG bị replace để giữ sắc thái cho PhoBERT
        self.teencode_dict = {
            str(k).lower().strip(): str(v).lower().strip() 
            for k, v, t in zip(df_dict['Teencode - GenZ'], df_dict['Ý nghĩa'], df_dict['Phân loại']) 
            if pd.notna(k) and str(t).strip() == 'Viết tắt'
        }

    def clean(self, text):
        if not text or pd.isna(text): return ""
        
        text = text.lower().strip()

        # TUYỆT ĐỐI KHÔNG nạp 'Viết lóng' vào đây để tránh mất 'vl', 'cuteee'
        sorted_keys = sorted(self.teencode_dict.keys(), key=len, reverse=True)
        for teencode in sorted_keys:
            pattern = r'\b' + re.escape(teencode) + r'\b'
            text = re.sub(pattern, self.teencode_dict[teencode], text)

        # BƯỚC 3: GIỮ LẠI DẤU CÂU BIỂU CẢM
        # Thay vì xóa hết, chỉ xóa các ký tự rác, giữ lại .,!? và các icon : ) =
        # Regex này an toàn hơn cho các icon :)))
        text = re.sub(r'[^\w\s.,!?::)(/=+]', ' ', text)
        
        return " ".join(text.split())
    
if __name__ == "__main__":
    # Test nhanh
    cleaner = TextCleaner('C:\\Users\\ASPIRE A715 - 42G\\Downloads\\MentalHealth_AI_Project\\data\\external\\Xử lý teencode.xlsx')
    sample_text = "Hôm nay t cảm thấy vl :)))" 
    print(cleaner.clean(sample_text))
