"""
Seed data mẫu cho NhatKi.
Chạy: cd backend && python -m app.seed
"""
import uuid
from datetime import datetime, timedelta, timezone

from .database import SessionLocal
from .models.user import User
from .models.category import Category
from .models.entry import Entry
from .models.entry_tag import EntryTag
from .models.analysis_result import AnalysisResult
from .services.auth_service import get_password_hash
from .constants import EMOTION_MAPPING, AI_SUMMARY_TEMPLATES, AI_TAGS_BY_EMOTION


SAMPLE_ENTRIES = [
    {
        "title": "Ngày làm việc hiệu quả",
        "content": "Hôm nay tôi hoàn thành được rất nhiều việc. Cảm thấy vui vẻ và tràn đầy năng lượng sau một ngày dài.",
        "emotion": "Enjoyment",
        "tags": ["Công việc"],
    },
    {
        "title": "Nhớ nhà",
        "content": "Nhìn ảnh gia đình mà thấy buồn quá. Lâu rồi chưa về thăm bố mẹ.",
        "emotion": "Sadness",
        "tags": ["Gia đình"],
    },
    {
        "title": "Bực bội vì traffic",
        "content": "Kẹt xe 2 tiếng đồng hồ, về tới nhà mà vẫn còn tức. Thành phố này đông quá.",
        "emotion": "Anger",
        "tags": ["Bản thân"],
    },
    {
        "title": "Lo lắng về deadline",
        "content": "Tuần tới nộp báo cáo mà còn nhiều việc chưa xong. Cảm thấy khá lo lắng.",
        "emotion": "Fear",
        "tags": ["Công việc"],
    },
    {
        "title": "Buổi sáng bình yên",
        "content": "Dậy sớm, uống cà phê, nghe nhạc. Không có gì đặc biệt nhưng cảm thấy ổn.",
        "emotion": "Other",
        "tags": ["Bản thân"],
    },
]

CATEGORIES = [
    {"name": "Công việc",  "icon": "bag",     "color_theme": "#4A90D9"},
    {"name": "Bản thân",   "icon": "heart",   "color_theme": "#E57373"},
    {"name": "Gia đình",   "icon": "leaf",    "color_theme": "#81C784"},
]


def seed():
    db = SessionLocal()
    try:
        # 1. Tạo user test nếu chưa có
        user = db.query(User).filter(User.email == "test@nhatki.app").first()
        if user is None:
            user = User(
                email="test@nhatki.app",
                username="testuser",
                hashed_password=get_password_hash(" "),
                display_name="Test User",
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            print(f"Created user: {user.email}")
        else:
            print(f"User already exists: {user.email}")

        # 2. Tạo 3 categories mặc định
        cat_map = {}
        for cat_data in CATEGORIES:
            existing = db.query(Category).filter(
                Category.user_id == user.id,
                Category.name == cat_data["name"]
            ).first()
            if existing is None:
                cat = Category(user_id=user.id, **cat_data)
                db.add(cat)
                db.commit()
                db.refresh(cat)
                cat_map[cat_data["name"]] = cat
                print(f"Created category: {cat.name}")
            else:
                cat_map[cat_data["name"]] = existing
                print(f"Category already exists: {existing.name}")

        # 3. Tạo 5 entries mẫu với analysis giả
        for i, e_data in enumerate(SAMPLE_ENTRIES):
            existing = db.query(Entry).filter(
                Entry.user_id == user.id,
                Entry.title == e_data["title"],
            ).first()
            if existing:
                print(f"Entry already exists: {e_data['title']}")
                continue

            # Gán category nếu tag khớp với tên category
            cat_name = e_data["tags"][0] if e_data["tags"] else None
            cat = cat_map.get(cat_name)

            created_at = datetime.now(timezone.utc) - timedelta(days=i * 2)

            entry = Entry(
                user_id=user.id,
                title=e_data["title"],
                content=e_data["content"],
                category_id=cat.id if cat else None,
                created_at=created_at,
                updated_at=created_at,
            )
            db.add(entry)
            db.flush()

            # Tags
            for tag_name in e_data["tags"]:
                db.add(EntryTag(entry_id=entry.id, tag_name=tag_name, tag_type="user_defined"))

            # Analysis giả
            emotion = e_data["emotion"]
            mapping = EMOTION_MAPPING[emotion]
            summary = AI_SUMMARY_TEMPLATES.get((emotion, "Clean"), "Một ngày bình thường.")
            ai_tags = AI_TAGS_BY_EMOTION.get(emotion, [])

            analysis = AnalysisResult(
                entry_id=entry.id,
                emotion_label=emotion,
                emotion_score=0.80 + i * 0.02,
                hate_label="Clean",
                hate_score=0.95,
                needs_assessment=emotion not in ("Enjoyment", "Other"),
                mood_label_vi=mapping["vi"],
                mood_color=mapping["color"],
                ai_summary=summary,
                ai_tags=ai_tags,
                raw_response={"seeded": True},
                analyzed_at=created_at,
            )
            db.add(analysis)
            db.commit()
            print(f"Created entry: {e_data['title']}")

        print("\nSeed hoàn tất!")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
