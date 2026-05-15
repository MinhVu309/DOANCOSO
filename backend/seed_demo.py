"""
Seed a demo account covering all DSM-5/ICD-11 warning tiers.

Run from backend/:
    source venv/bin/activate && python seed_demo.py
"""
import uuid
from datetime import datetime, timedelta, timezone

from app.database import SessionLocal
from app.services.auth_service import get_password_hash
from app.models.analysis_result import AnalysisResult
from app.models.category import Category  # noqa: F401 — needed for SQLAlchemy relationship resolution
from app.models.entry import Entry
from app.models.entry_tag import EntryTag  # noqa: F401
from app.models.user import User
from app.services.condition_service import aggregate_user_conditions

EMAIL    = "demo@nhatki.vn"
USERNAME = "DemoUser"
PASSWORD = "Demo@123"



def _ago(days: float) -> datetime:
    return datetime.now(timezone.utc) - timedelta(days=days)


def _entry(db, user_id, days_ago, title, content):
    e = Entry(
        id=uuid.uuid4(),
        user_id=user_id,
        title=title,
        content=content,
        created_at=_ago(days_ago),
    )
    db.add(e)
    db.flush()
    return e


def _analysis(db, entry_id, emotion_label, emotion_score,
               hate_label, hate_score, conditions, mood_label_vi, ai_summary):
    db.add(AnalysisResult(
        id=uuid.uuid4(),
        entry_id=entry_id,
        emotion_label=emotion_label,
        emotion_score=emotion_score,
        hate_label=hate_label,
        hate_score=hate_score,
        needs_assessment=True,
        conditions=conditions,
        mood_label_vi=mood_label_vi,
        mood_color="#5b614d",
        ai_summary=ai_summary,
        ai_tags=[],
    ))


def main():
    db = SessionLocal()
    try:
        # ── 1. Tạo / tìm user ──────────────────────────────────────────────
        user = db.query(User).filter(User.email == EMAIL).first()
        if not user:
            user = User(
                email=EMAIL,
                username=USERNAME,
                hashed_password=get_password_hash(PASSWORD),
                display_name="Demo NhatKi",
                is_active=True,
            )
            db.add(user)
            db.flush()
            print(f"[+] Tạo user: {EMAIL}")
        else:
            print(f"[~] User đã tồn tại: {EMAIL}")

        uid = user.id

        # ── 2. Entries ─────────────────────────────────────────────────────

        # --- URGENT: Rối loạn trầm cảm (7 ngày liên tiếp, intensity 0.70) ---
        # --- ALERT : PTSD (7 lần trong 14 ngày, intensity 0.63)            ---
        # --- WATCH : Mất ngủ (7 lần trong 7 ngày, intensity 0.40)          ---
        for day in range(1, 8):
            e = _entry(db, uid, day,
                f"Ngày {day}: Cảm giác không muốn làm gì",
                "Hôm nay lại cảm thấy rất nặng nề. Không có động lực, chỉ muốn nằm im. "
                "Đêm qua mãi không ngủ được, cứ nằm nhìn trần nhà. Mọi thứ đều vô nghĩa.")
            _analysis(db, e.id,
                emotion_label="Sadness", emotion_score=0.72,
                hate_label="Clean",     hate_score=0.05,
                conditions=[
                    {"label": "Rối loạn trầm cảm", "confidence": 0.70},
                    {"label": "PTSD",               "confidence": 0.63},
                    {"label": "Mất ngủ",             "confidence": 0.40},
                ],
                mood_label_vi="Buồn bã",
                ai_summary="Người dùng biểu hiện trạng thái trầm buồn kéo dài, mất ngủ.")

        # --- ALERT: Rối loạn lo âu (5 lần trong 21 ngày, intensity 0.58) ---
        for day in [8, 10, 12, 14, 16]:
            e = _entry(db, uid, day,
                f"Ngày -{day}: Lo lắng không rõ nguyên nhân",
                "Tim đập nhanh, tay chân bứt rứt suốt từ sáng. Cứ lo sợ điều gì đó tệ sẽ xảy ra "
                "dù không có lý do cụ thể. Khó thở, không tập trung được vào công việc.")
            _analysis(db, e.id,
                emotion_label="Fear",   emotion_score=0.62,
                hate_label="Clean",     hate_score=0.04,
                conditions=[
                    {"label": "Rối loạn lo âu", "confidence": 0.58},
                ],
                mood_label_vi="Sợ hãi",
                ai_summary="Người dùng biểu hiện lo âu lan tỏa, khó kiểm soát.")

        # --- WATCH: Rối loạn lưỡng cực (2 lần trong 14 ngày, intensity 0.52) ---
        for day in [9, 11]:
            e = _entry(db, uid, day,
                f"Ngày -{day}: Tâm trạng thất thường",
                "Sáng nay tràn đầy năng lượng, ý tưởng tuôn ra không ngừng, muốn làm hết mọi thứ. "
                "Chiều tối đột ngột sụp xuống, cáu kỉnh vô cớ với mọi người xung quanh.")
            _analysis(db, e.id,
                emotion_label="Anger",  emotion_score=0.58,
                hate_label="Clean",     hate_score=0.06,
                conditions=[
                    {"label": "Rối loạn lưỡng cực", "confidence": 0.52},
                ],
                mood_label_vi="Tức giận",
                ai_summary="Người dùng thay đổi tâm trạng đột ngột giữa hưng phấn và ức chế.")

        # --- WATCH: ADHD (3 lần trong 30 ngày, intensity 0.45) ---
        for day in [20, 25, 28]:
            e = _entry(db, uid, day,
                f"Ngày -{day}: Không tập trung được",
                "Ngồi làm việc nhưng đầu óc cứ lang thang. Bắt đầu việc này chưa xong lại nhảy sang "
                "việc khác. Dễ nổi cáu khi bị ngắt quãng. Quên mất mình định làm gì.")
            _analysis(db, e.id,
                emotion_label="Anger",  emotion_score=0.50,
                hate_label="Clean",     hate_score=0.04,
                conditions=[
                    {"label": "ADHD", "confidence": 0.45},
                ],
                mood_label_vi="Tức giận",
                ai_summary="Người dùng gặp khó khăn tập trung, dễ phân tâm và bốc đồng.")

        # --- URGENT: Cảnh báo khủng hoảng (crisis override) ---
        e = _entry(db, uid, 0.1,
            "Không muốn tiếp tục nữa",
            "Tôi không thể chịu đựng thêm được nữa. Mọi thứ đều vô nghĩa và tôi rất mệt. "
            "Tôi không muốn tồn tại ở đây nữa. Không ai hiểu tôi cả.")
        _analysis(db, e.id,
            emotion_label="Anger",  emotion_score=0.82,
            hate_label="Hate",      hate_score=0.88,
            conditions=[
                {"label": "Rối loạn trầm cảm", "confidence": 0.75},
            ],
            mood_label_vi="Tức giận",
            ai_summary="CẢNH BÁO: Người dùng biểu hiện suy nghĩ tiêu cực nghiêm trọng.")

        db.flush()

        # ── 3. Chạy aggregation ────────────────────────────────────────────
        aggregate_user_conditions(db, uid)

        print("\n✓ Seed hoàn tất!")
        print(f"  Email   : {EMAIL}")
        print(f"  Password: {PASSWORD}")
        print("\nWarning tiers được tạo:")
        print("  urgent  → Rối loạn trầm cảm (F32.1), Cảnh báo khủng hoảng")
        print("  alert   → Rối loạn lo âu (F41.1), PTSD (F43.10)")
        print("  watch   → Mất ngủ (F51.01), Rối loạn lưỡng cực (F31), ADHD (F90.2)")

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
