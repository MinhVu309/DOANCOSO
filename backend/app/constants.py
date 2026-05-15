EMOTION_MAPPING = {
    # ── Legacy VSMEC labels (PascalCase) — giữ cho backward compat ────────────
    "Enjoyment": {"vi": "HẠNH PHÚC", "vi_casual": "Vui vẻ",    "color": "green",  "mood_score": 1.0},
    "Other":     {"vi": "BÌNH YÊN",  "vi_casual": "Bình yên",  "color": "gray",   "mood_score": 0.6},
    "Surprise":  {"vi": "NGẠC NHIÊN","vi_casual": "Hào hứng",  "color": "purple", "mood_score": 0.7},
    "Sadness":   {"vi": "ÁP LỰC",   "vi_casual": "Trầm tư",   "color": "blue",   "mood_score": 0.3},
    "Fear":      {"vi": "LO LẮNG",  "vi_casual": "Lo âu",     "color": "orange", "mood_score": 0.25},
    "Anger":     {"vi": "TỨC GIẬN", "vi_casual": "Mệt mỏi",   "color": "red",    "mood_score": 0.2},
    "Disgust":   {"vi": "CHÁN NẢN", "vi_casual": "Chán nản",  "color": "brown",  "mood_score": 0.15},
    # ── 28 ViGoEmotions labels (lowercase) ────────────────────────────────────
    # Tích cực
    "amusement":   {"vi": "VUI VẺ",     "vi_casual": "Vui vẻ",     "color": "green",  "mood_score": 0.95},
    "excitement":  {"vi": "HỨNG KHỞI",  "vi_casual": "Hứng khởi",  "color": "green",  "mood_score": 0.9},
    "joy":         {"vi": "HẠNH PHÚC",  "vi_casual": "Vui vẻ",     "color": "green",  "mood_score": 1.0},
    "love":        {"vi": "YÊU THƯƠNG", "vi_casual": "Yêu thương",  "color": "green",  "mood_score": 1.0},
    "desire":      {"vi": "MONG MUỐN",  "vi_casual": "Khao khát",   "color": "green",  "mood_score": 0.75},
    "optimism":    {"vi": "LẠC QUAN",   "vi_casual": "Lạc quan",    "color": "green",  "mood_score": 0.9},
    "caring":      {"vi": "QUAN TÂM",   "vi_casual": "Quan tâm",    "color": "green",  "mood_score": 0.85},
    "pride":       {"vi": "TỰ HÀO",     "vi_casual": "Tự hào",      "color": "green",  "mood_score": 0.85},
    "admiration":  {"vi": "NGƯỠNG MỘ",  "vi_casual": "Ngưỡng mộ",   "color": "green",  "mood_score": 0.8},
    "gratitude":   {"vi": "BIẾT ƠN",    "vi_casual": "Biết ơn",     "color": "green",  "mood_score": 0.9},
    "relief":      {"vi": "NHẸ NHÕM",   "vi_casual": "Nhẹ nhõm",    "color": "green",  "mood_score": 0.8},
    "approval":    {"vi": "ĐỒNG TÌNH",  "vi_casual": "Đồng tình",   "color": "green",  "mood_score": 0.75},
    # Trung tính / bất ngờ
    "realization": {"vi": "NHẬN THỨC",  "vi_casual": "Nhận ra",     "color": "purple", "mood_score": 0.6},
    "surprise":    {"vi": "NGẠC NHIÊN", "vi_casual": "Ngạc nhiên",  "color": "purple", "mood_score": 0.65},
    "curiosity":   {"vi": "TÒ MÒ",      "vi_casual": "Tò mò",       "color": "purple", "mood_score": 0.65},
    "confusion":   {"vi": "BỐI RỐI",    "vi_casual": "Bối rối",     "color": "gray",   "mood_score": 0.45},
    "neutral":     {"vi": "BÌNH YÊN",   "vi_casual": "Bình yên",    "color": "gray",   "mood_score": 0.6},
    # Lo lắng / sợ hãi
    "fear":        {"vi": "SỢ HÃI",     "vi_casual": "Lo âu",       "color": "orange", "mood_score": 0.25},
    "nervousness": {"vi": "HỒI HỘP",    "vi_casual": "Hồi hộp",     "color": "orange", "mood_score": 0.35},
    # Buồn bã
    "remorse":        {"vi": "HỐI HẬN",    "vi_casual": "Hối hận",     "color": "blue",   "mood_score": 0.2},
    "embarrassment":  {"vi": "XẤU HỔ",     "vi_casual": "Xấu hổ",      "color": "blue",   "mood_score": 0.25},
    "disappointment": {"vi": "THẤT VỌNG",  "vi_casual": "Thất vọng",   "color": "blue",   "mood_score": 0.2},
    "sadness":        {"vi": "BUỒN BÃ",    "vi_casual": "Buồn bã",     "color": "blue",   "mood_score": 0.3},
    "grief":          {"vi": "ĐAU KHỔ",    "vi_casual": "Đau khổ",     "color": "blue",   "mood_score": 0.1},
    # Tiêu cực khác
    "disgust":      {"vi": "CHÁN NẢN",  "vi_casual": "Chán nản",    "color": "brown",  "mood_score": 0.15},
    "disapproval":  {"vi": "PHẢN ĐỐI",  "vi_casual": "Không đồng ý","color": "brown",  "mood_score": 0.2},
    "anger":        {"vi": "TỨC GIẬN",  "vi_casual": "Tức giận",    "color": "red",    "mood_score": 0.2},
    "annoyance":    {"vi": "KHÓ CHỊU",  "vi_casual": "Khó chịu",    "color": "red",    "mood_score": 0.25},
}

AI_SUMMARY_TEMPLATES = {
    ("Enjoyment", "Clean"):    "Tâm trạng tích cực, vui vẻ và tràn đầy năng lượng.",
    ("Enjoyment", "Offensive"):"Tâm trạng vui nhưng có những suy nghĩ cần chú ý.",
    ("Enjoyment", "Hate"):     "Tâm trạng vui nhưng có những suy nghĩ tiêu cực cần xem xét.",
    ("Sadness", "Clean"):      "Tâm trạng có chút buồn bã, cần thời gian nghỉ ngơi.",
    ("Sadness", "Offensive"):  "Tâm trạng tiêu cực, có dấu hiệu cần chú ý.",
    ("Sadness", "Hate"):       "Tâm trạng tiêu cực rõ rệt, nên tìm người trò chuyện.",
    ("Anger", "Clean"):        "Cảm xúc có phần căng thẳng, cần tìm cách giải tỏa.",
    ("Anger", "Offensive"):    "Tâm trạng căng thẳng với những suy nghĩ tiêu cực.",
    ("Anger", "Hate"):         "Cảm xúc rất tiêu cực, hãy tìm sự hỗ trợ từ người thân.",
    ("Fear", "Clean"):         "Có những lo lắng nhất định, nên chia sẻ cùng ai đó.",
    ("Fear", "Offensive"):     "Lo lắng kèm suy nghĩ tiêu cực, cần được quan tâm.",
    ("Fear", "Hate"):          "Lo lắng và căng thẳng cao, nên tìm hỗ trợ chuyên nghiệp.",
    ("Disgust", "Clean"):      "Tâm trạng không thoải mái, có thể cần thay đổi góc nhìn.",
    ("Disgust", "Offensive"):  "Tâm trạng tiêu cực, có dấu hiệu cần chú ý.",
    ("Disgust", "Hate"):       "Tâm trạng rất tiêu cực, nên tìm sự hỗ trợ.",
    ("Surprise", "Clean"):     "Có sự bất ngờ hoặc thay đổi trong ngày hôm nay.",
    ("Surprise", "Offensive"): "Bất ngờ kèm theo những cảm xúc phức tạp.",
    ("Surprise", "Hate"):      "Bất ngờ với những phản ứng tiêu cực mạnh.",
    ("Other", "Clean"):        "Tâm trạng ổn định, một ngày bình thường.",
    ("Other", "Offensive"):    "Tâm trạng trung tính nhưng có vài suy nghĩ cần chú ý.",
    ("Other", "Hate"):         "Có những suy nghĩ tiêu cực cần được xem xét lại.",
}

AI_TAGS_BY_EMOTION = {
    "Enjoyment": ["#TÍCH_CỰC", "#HẠNH_PHÚC"],
    "Sadness":   ["#BUỒN_BÃ", "#CẦN_CHĂM_SÓC"],
    "Anger":     ["#CĂNG_THẲNG", "#CẦN_GIẢI_TOẢ"],
    "Fear":      ["#LO_LẮNG", "#CẦN_HỖ_TRỢ"],
    "Disgust":   ["#KHÓ_CHỊU", "#KHÔNG_THOẢI_MÁI"],
    "Surprise":  ["#BẤT_NGỜ", "#THAY_ĐỔI"],
    "Other":     ["#BÌNH_THƯỜNG", "#ỔN_ĐỊNH"],
}
