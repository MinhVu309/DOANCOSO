import { useState, useEffect } from 'react';
import client from '../api/client';

// 28 ViGoEmotions → Material Symbols icon
const MOOD_ICON = {
  // Tích cực
  amusement: 'sentiment_very_satisfied', excitement: 'sentiment_very_satisfied',
  joy: 'sentiment_very_satisfied', love: 'favorite', desire: 'sentiment_satisfied',
  optimism: 'sentiment_satisfied', caring: 'volunteer_activism',
  pride: 'emoji_events', admiration: 'star', gratitude: 'sentiment_very_satisfied',
  relief: 'sentiment_satisfied', approval: 'thumb_up',
  // Trung tính / bất ngờ
  realization: 'lightbulb', surprise: 'sentiment_excited',
  curiosity: 'search', confusion: 'help', neutral: 'sentiment_neutral',
  // Lo lắng / sợ
  fear: 'sentiment_worried', nervousness: 'sentiment_worried',
  // Buồn bã
  remorse: 'sentiment_sad', embarrassment: 'sentiment_sad',
  disappointment: 'sentiment_sad', sadness: 'sentiment_sad', grief: 'sentiment_sad',
  // Tiêu cực
  disgust: 'sentiment_dissatisfied', disapproval: 'thumb_down',
  anger: 'sentiment_stressed', annoyance: 'sentiment_stressed',
};

// Tên tiếng Việt casual cho từng nhãn (hiện trong chip cảm xúc)
const EMOTION_VI = {
  amusement: 'Vui vẻ', excitement: 'Hứng khởi', joy: 'Hạnh phúc',
  love: 'Yêu thương', desire: 'Khao khát', optimism: 'Lạc quan',
  caring: 'Quan tâm', pride: 'Tự hào', admiration: 'Ngưỡng mộ',
  gratitude: 'Biết ơn', relief: 'Nhẹ nhõm', approval: 'Đồng tình',
  realization: 'Nhận ra', surprise: 'Ngạc nhiên', curiosity: 'Tò mò',
  confusion: 'Bối rối', fear: 'Lo âu', nervousness: 'Hồi hộp',
  remorse: 'Hối hận', embarrassment: 'Xấu hổ', disappointment: 'Thất vọng',
  sadness: 'Buồn bã', grief: 'Đau khổ', disgust: 'Chán nản',
  anger: 'Tức giận', annoyance: 'Khó chịu', disapproval: 'Phản đối',
  neutral: 'Bình yên',
};

// Màu chip theo nhóm cảm xúc
const EMOTION_CHIP_CLASS = {
  amusement: 'bg-green-50 text-green-700 border-green-200',
  excitement: 'bg-green-50 text-green-700 border-green-200',
  joy: 'bg-green-50 text-green-700 border-green-200',
  love: 'bg-pink-50 text-pink-700 border-pink-200',
  desire: 'bg-green-50 text-green-700 border-green-200',
  optimism: 'bg-green-50 text-green-700 border-green-200',
  caring: 'bg-green-50 text-green-700 border-green-200',
  pride: 'bg-green-50 text-green-700 border-green-200',
  admiration: 'bg-green-50 text-green-700 border-green-200',
  gratitude: 'bg-green-50 text-green-700 border-green-200',
  relief: 'bg-green-50 text-green-700 border-green-200',
  approval: 'bg-green-50 text-green-700 border-green-200',
  realization: 'bg-purple-50 text-purple-700 border-purple-200',
  surprise: 'bg-purple-50 text-purple-700 border-purple-200',
  curiosity: 'bg-purple-50 text-purple-700 border-purple-200',
  confusion: 'bg-gray-100 text-gray-600 border-gray-300',
  neutral: 'bg-gray-100 text-gray-600 border-gray-300',
  fear: 'bg-orange-50 text-orange-700 border-orange-200',
  nervousness: 'bg-orange-50 text-orange-700 border-orange-200',
  remorse: 'bg-blue-50 text-blue-700 border-blue-200',
  embarrassment: 'bg-blue-50 text-blue-700 border-blue-200',
  disappointment: 'bg-blue-50 text-blue-700 border-blue-200',
  sadness: 'bg-blue-50 text-blue-700 border-blue-200',
  grief: 'bg-blue-50 text-blue-700 border-blue-200',
  disgust: 'bg-amber-50 text-amber-700 border-amber-200',
  disapproval: 'bg-amber-50 text-amber-700 border-amber-200',
  anger: 'bg-red-50 text-red-700 border-red-200',
  annoyance: 'bg-red-50 text-red-700 border-red-200',
};

export default function Journaling() {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [selectedTags, setSelectedTags] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [categories, setCategories] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null); // analysis result
  const [error, setError] = useState('');
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    client.get('/api/categories').then(res => setCategories(res.data)).catch(() => {});
  }, []);

  const availableTags = [
    'Công việc', 'Gia đình', 'Bản thân', 'Buồn', 'Hạnh phúc', 'Sáng tạo',
    ...categories.map(c => c.name).filter(n => !['Công việc', 'Gia đình', 'Bản thân'].includes(n)),
  ];
  const uniqueTags = [...new Set(availableTags)];

  function toggleTag(tag) {
    setSelectedTags(prev =>
      prev.includes(tag) ? prev.filter(t => t !== tag) : [...prev, tag]
    );
  }

  async function handleSubmit() {
    if (!content.trim()) { setError('Hãy viết điều gì đó trước.'); return; }
    setIsLoading(true);
    setError('');
    setResult(null);
    setSaved(false);
    try {
      // 1. Create entry
      const entryRes = await client.post('/api/entries', {
        content: content.trim(),
        title: title.trim() || undefined,
        user_tags: selectedTags,
        category_id: selectedCategory || undefined,
      });
      const entryId = entryRes.data.id;

      // 2. Trigger analysis
      const analysisRes = await client.post(`/api/entries/${entryId}/analyze`);
      setResult(analysisRes.data);
      setSaved(true);

      // Reset form
      setTitle('');
      setContent('');
      setSelectedTags([]);
      setSelectedCategory('');
    } catch (err) {
      const msg = err.response?.data?.detail;
      setError(typeof msg === 'string' ? msg : 'Có lỗi xảy ra, vui lòng thử lại.');
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="md:ml-72 min-h-screen flex flex-col pt-20 md:pt-12 px-6 md:px-16 pb-20">
      {/* Header */}
      <header className="max-w-4xl w-full mx-auto mb-12">
        <span className="text-sm font-medium text-primary uppercase tracking-[0.2em] mb-4 block">
          {new Date().toLocaleDateString('vi-VN', { weekday: 'long', day: 'numeric', month: 'long' })}
        </span>
        <h2 className="text-4xl md:text-5xl lg:text-6xl font-light text-on-background leading-tight">
          Hôm nay của bạn thế nào?
        </h2>
      </header>

      <section className="max-w-4xl w-full mx-auto grid grid-cols-1 gap-12">
        {/* Tags */}
        <div className="flex flex-wrap gap-3 items-center">
          <span className="text-xs font-bold text-on-surface-variant uppercase tracking-widest mr-2">Tags:</span>
          {uniqueTags.map(tag => (
            <button
              key={tag}
              onClick={() => toggleTag(tag)}
              className={`px-6 py-2 rounded-full border text-on-surface text-sm transition-all ${
                selectedTags.includes(tag)
                  ? 'bg-primary/10 border-primary/30 text-primary font-medium'
                  : 'bg-surface-container border-surface-variant/30 hover:border-primary/30'
              }`}
            >
              {tag}
            </button>
          ))}
        </div>

        {/* Category selector (if categories exist) */}
        {categories.length > 0 && (
          <div className="flex items-center gap-3">
            <span className="text-xs font-bold text-on-surface-variant uppercase tracking-widest">Danh mục:</span>
            <select
              value={selectedCategory}
              onChange={e => setSelectedCategory(e.target.value)}
              className="bg-surface-container border border-outline-variant/30 rounded-xl px-4 py-2 text-on-surface text-sm focus:outline-none focus:ring-2 focus:ring-primary/20"
            >
              <option value="">— Không có —</option>
              {categories.map(c => (
                <option key={c.id} value={c.id}>{c.name}</option>
              ))}
            </select>
          </div>
        )}

        {/* Editor */}
        <div className="relative group">
          <div className="absolute -inset-1 bg-gradient-to-br from-primary/5 to-surface-container-highest/10 rounded-[2rem] blur-xl opacity-30 group-focus-within:opacity-100 transition-opacity"></div>
          <div className="relative bg-surface-container-lowest rounded-[2rem] p-8 md:p-12 shadow-sm border border-surface-variant/20 min-h-[450px] flex flex-col">
            {/* Title input */}
            <input
              className="w-full bg-transparent border-none focus:ring-0 text-2xl font-semibold text-on-surface placeholder:text-stone-200 mb-4"
              placeholder="Tiêu đề (tùy chọn)"
              value={title}
              onChange={e => setTitle(e.target.value)}
            />
            <div className="w-12 h-px bg-surface-variant/40 mb-6" />
            <textarea
              className="w-full flex-grow bg-transparent border-none focus:ring-0 text-lg md:text-xl text-on-surface placeholder:text-stone-300 leading-relaxed resize-none"
              placeholder="Hãy bắt đầu dòng suy nghĩ của bạn tại đây..."
              value={content}
              onChange={e => { setContent(e.target.value); setError(''); }}
            />
            <div className="mt-12 flex flex-col md:flex-row items-center justify-between gap-6 border-t border-surface-variant/20 pt-8">
              <div className="flex gap-4">
                {['format_bold', 'format_italic', 'format_list_bulleted', 'attach_file'].map(icon => (
                  <button
                    key={icon}
                    className="w-12 h-12 flex items-center justify-center rounded-xl hover:bg-surface-container transition-colors text-on-surface-variant"
                  >
                    <span className="material-symbols-outlined">{icon}</span>
                  </button>
                ))}
              </div>
              <button
                onClick={handleSubmit}
                disabled={isLoading}
                className="flex items-center gap-3 px-8 py-4 bg-primary text-on-primary rounded-xl font-semibold shadow-xl shadow-primary/10 hover:scale-[1.02] active:scale-[0.98] disabled:opacity-50 transition-all"
              >
                {isLoading ? (
                  <span className="material-symbols-outlined animate-spin" style={{ fontVariationSettings: "'FILL' 1" }}>progress_activity</span>
                ) : (
                  <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 1" }}>psychology</span>
                )}
                <span>{isLoading ? 'Đang phân tích...' : 'Analyze Sentiment'}</span>
              </button>
            </div>
          </div>
        </div>

        {/* Error */}
        {error && (
          <div className="p-4 bg-error/5 border border-error/20 rounded-2xl text-sm text-error">
            {error}
          </div>
        )}

        {/* Analysis Result */}
        {result && (() => {
          const emotions = result.raw_response?.emotions?.length > 0
            ? result.raw_response.emotions
            : [result.emotion_label].filter(Boolean);
          const primaryEmotion = emotions[0] || 'neutral';
          return (
            <div className="p-8 rounded-[2rem] bg-surface-container-low border border-outline-variant/20 flex flex-col gap-6 animate-in slide-in-from-bottom-4 duration-500">
              <div className="flex items-center gap-3">
                <span className="material-symbols-outlined text-primary text-3xl" style={{ fontVariationSettings: "'FILL' 1" }}>
                  {MOOD_ICON[primaryEmotion] || 'sentiment_neutral'}
                </span>
                <div>
                  <h4 className="font-bold text-on-surface">Kết quả phân tích</h4>
                  <p className="text-sm text-on-surface-variant">AI đã đọc và hiểu nhật ký của bạn</p>
                </div>
                {saved && (
                  <div className="ml-auto flex items-center gap-1.5 text-xs text-primary">
                    <span className="material-symbols-outlined text-base">check_circle</span>
                    Đã lưu
                  </div>
                )}
              </div>

              {/* Mood label + hate badge */}
              <div className="flex flex-wrap gap-3 items-center">
                <div className="flex flex-col items-center px-6 py-4 bg-surface-container rounded-2xl">
                  <span className="text-2xl font-black text-primary">{result.mood_label_vi}</span>
                  <span className="text-xs text-on-surface-variant mt-1">Tâm trạng tổng thể</span>
                </div>
                {result.hate_label !== 'Clean' && (
                  <div className="flex flex-col items-center px-6 py-4 bg-error/5 border border-error/20 rounded-2xl">
                    <span className="text-sm font-bold text-error">{result.hate_label}</span>
                    <span className="text-xs text-on-surface-variant mt-1">Nội dung</span>
                  </div>
                )}
              </div>

              {/* Multi-label emotion chips */}
              {emotions.length > 0 && (
                <div>
                  <p className="text-xs font-bold text-on-surface-variant uppercase tracking-widest mb-3">
                    Cảm xúc được phát hiện
                  </p>
                  <div className="flex flex-wrap gap-2">
                    {emotions.map(e => (
                      <span
                        key={e}
                        className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full border text-xs font-semibold ${
                          EMOTION_CHIP_CLASS[e] || 'bg-surface-container text-on-surface border-outline-variant/30'
                        }`}
                      >
                        <span className="material-symbols-outlined text-sm" style={{ fontVariationSettings: "'FILL' 1" }}>
                          {MOOD_ICON[e] || 'circle'}
                        </span>
                        {EMOTION_VI[e] || e}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              <div className="p-4 bg-surface-container/80 rounded-2xl flex items-start gap-3 border border-outline-variant/20">
                <span className="material-symbols-outlined text-primary" style={{ fontVariationSettings: "'FILL' 1" }}>auto_awesome</span>
                <p className="text-sm italic text-on-surface-variant">{result.ai_summary}</p>
              </div>

              {result.ai_tags?.length > 0 && (
                <div className="flex flex-wrap gap-2">
                  {result.ai_tags.map(tag => (
                    <span key={tag} className="px-3 py-1 bg-surface-container text-[10px] font-bold uppercase tracking-widest rounded-full text-on-primary-fixed-variant border border-outline-variant/30">
                      {tag}
                    </span>
                  ))}
                </div>
              )}
            </div>
          );
        })()}

        {/* Mental Health Assessment - chỉ hiện khi Module-2 có kết quả */}
        {result?.needs_assessment && result?.conditions?.length > 0 && (
          <div className="p-8 rounded-[2rem] bg-surface-container-low border border-outline-variant/20 flex flex-col gap-6 animate-in slide-in-from-bottom-4 duration-700">
            <div className="flex items-center gap-3">
              <span className="material-symbols-outlined text-tertiary" style={{ fontVariationSettings: "'FILL' 1" }}>neurology</span>
              <div>
                <h4 className="font-bold text-on-surface">Đánh giá sức khỏe tâm thần</h4>
                <p className="text-sm text-on-surface-variant">Các tình trạng có thể liên quan</p>
              </div>
            </div>

            <div className="flex flex-col gap-4">
              {result.conditions.map((c, i) => (
                <div key={c.label} className="flex items-center gap-4">
                  <span className={`text-xs font-bold w-5 shrink-0 ${i === 0 ? 'text-tertiary' : 'text-on-surface-variant'}`}>
                    {i + 1}
                  </span>
                  <div className="flex-1">
                    <div className="flex justify-between mb-1.5">
                      <span className={`text-sm ${i === 0 ? 'font-semibold text-on-surface' : 'font-medium text-on-surface-variant'}`}>
                        {c.label}
                      </span>
                      <span className="text-xs text-on-surface-variant tabular-nums">
                        {Math.round(c.confidence * 100)}%
                      </span>
                    </div>
                    <div className="h-1.5 bg-surface-variant/30 rounded-full overflow-hidden">
                      <div
                        className={`h-full rounded-full transition-all duration-500 ${i === 0 ? 'bg-tertiary' : 'bg-tertiary/40'}`}
                        style={{ width: `${Math.round(c.confidence * 100)}%` }}
                      />
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <p className="text-xs text-on-surface-variant/50 italic">
              * Đây là gợi ý từ AI, không thay thế chẩn đoán y tế chuyên nghiệp.
            </p>
          </div>
        )}

        {/* Bento Hints */}
        {!result && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-12">
            <div className="p-8 rounded-[2rem] bg-surface-container-low border border-surface-variant/30 flex flex-col gap-4 group hover:bg-surface-container transition-all">
              <div className="w-12 h-12 rounded-2xl bg-tertiary-container/20 flex items-center justify-center text-tertiary">
                <span className="material-symbols-outlined">auto_awesome</span>
              </div>
              <div>
                <h4 className="text-lg font-bold text-on-surface mb-1">Gợi ý chủ đề</h4>
                <p className="text-on-surface-variant text-sm leading-relaxed">Điều gì làm bạn cảm thấy biết ơn nhất trong ngày hôm nay?</p>
              </div>
            </div>
            <div className="p-8 rounded-[2rem] bg-surface-container-low border border-surface-variant/30 flex flex-col gap-4 group hover:bg-surface-container transition-all">
              <div className="w-12 h-12 rounded-2xl bg-primary-container/30 flex items-center justify-center text-primary">
                <span className="material-symbols-outlined">history_edu</span>
              </div>
              <div>
                <h4 className="text-lg font-bold text-on-surface mb-1">Cảm hứng cũ</h4>
                <p className="text-on-surface-variant text-sm leading-relaxed">Hôm nay của bạn có nét tương đồng nào với nhật ký ngày này năm ngoái không?</p>
              </div>
            </div>
          </div>
        )}
      </section>
    </main>
  );
}
