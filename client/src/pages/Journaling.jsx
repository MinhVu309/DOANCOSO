import { useState, useEffect } from 'react';
import client from '../api/client';

const MOOD_ICON = {
  Enjoyment: 'sentiment_very_satisfied',
  Sadness: 'sentiment_sad',
  Anger: 'sentiment_stressed',
  Fear: 'sentiment_worried',
  Disgust: 'sentiment_dissatisfied',
  Surprise: 'sentiment_excited',
  Other: 'sentiment_neutral',
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
        {result && (
          <div className="p-8 rounded-[2rem] bg-surface-container-low border border-outline-variant/20 flex flex-col gap-6 animate-in slide-in-from-bottom-4 duration-500">
            <div className="flex items-center gap-3">
              <span className="material-symbols-outlined text-primary" style={{ fontVariationSettings: "'FILL' 1" }}>
                {MOOD_ICON[result.emotion_label] || 'sentiment_neutral'}
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

            <div className="flex flex-wrap gap-4">
              <div className="flex flex-col items-center px-6 py-4 bg-surface-container rounded-2xl">
                <span className="text-2xl font-black text-primary">{result.mood_label_vi}</span>
                <span className="text-xs text-on-surface-variant mt-1">Tâm trạng</span>
              </div>
              <div className="flex flex-col items-center px-6 py-4 bg-surface-container rounded-2xl">
                <span className="text-2xl font-black text-on-surface">
                  {Math.round(result.emotion_score * 100)}%
                </span>
                <span className="text-xs text-on-surface-variant mt-1">Độ chắc chắn</span>
              </div>
              {result.hate_label !== 'Clean' && (
                <div className="flex flex-col items-center px-6 py-4 bg-error/5 border border-error/20 rounded-2xl">
                  <span className="text-sm font-bold text-error">{result.hate_label}</span>
                  <span className="text-xs text-on-surface-variant mt-1">Nội dung</span>
                </div>
              )}
            </div>

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
