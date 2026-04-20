EMOTION_MAPPING = {
    "Enjoyment": {"vi": "HẠNH PHÚC", "vi_casual": "Vui vẻ",    "color": "green",  "mood_score": 1.0},
    "Other":     {"vi": "BÌNH YÊN",  "vi_casual": "Bình yên",  "color": "gray",   "mood_score": 0.6},
    "Surprise":  {"vi": "NGẠC NHIÊN","vi_casual": "Hào hứng",  "color": "purple", "mood_score": 0.7},
    "Sadness":   {"vi": "ÁP LỰC",   "vi_casual": "Trầm tư",   "color": "blue",   "mood_score": 0.3},
    "Fear":      {"vi": "LO LẮNG",  "vi_casual": "Lo âu",     "color": "orange", "mood_score": 0.25},
    "Anger":     {"vi": "TỨC GIẬN", "vi_casual": "Mệt mỏi",   "color": "red",    "mood_score": 0.2},
    "Disgust":   {"vi": "CHÁN NẢN", "vi_casual": "Chán nản",  "color": "brown",  "mood_score": 0.15},
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
