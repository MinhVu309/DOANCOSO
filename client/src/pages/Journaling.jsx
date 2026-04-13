import { useState } from 'react';

const DEFAULT_TAGS = ['Công việc', 'Gia đình', 'Bản thân', 'Buồn', 'Hạnh phúc', 'Sáng tạo'];

export default function Journaling() {
  const [selectedTags, setSelectedTags] = useState([]);

  function toggleTag(tag) {
    setSelectedTags(prev =>
      prev.includes(tag) ? prev.filter(t => t !== tag) : [...prev, tag]
    );
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
          {/* Emotional Tags */}
          <div className="flex flex-wrap gap-3 items-center">
            <span className="text-xs font-bold text-on-surface-variant uppercase tracking-widest mr-2">Tags:</span>
            {DEFAULT_TAGS.map(tag => (
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
            <button className="w-10 h-10 rounded-full flex items-center justify-center bg-surface-container-high text-primary hover:bg-primary hover:text-on-primary transition-all">
              <span className="material-symbols-outlined">add</span>
            </button>
          </div>

          {/* Editor */}
          <div className="relative group">
            <div className="absolute -inset-1 bg-gradient-to-br from-primary/5 to-surface-container-highest/10 rounded-[2rem] blur-xl opacity-30 group-focus-within:opacity-100 transition-opacity"></div>
            <div className="relative bg-surface-container-lowest rounded-[2rem] p-8 md:p-12 shadow-sm border border-surface-variant/20 min-h-[450px] flex flex-col">
              <textarea
                className="w-full flex-grow bg-transparent border-none focus:ring-0 text-lg md:text-xl text-on-surface placeholder:text-stone-300 leading-relaxed resize-none text-area-glow"
                placeholder="Hãy bắt đầu dòng suy nghĩ của bạn tại đây..."
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
                <button className="flex items-center gap-3 px-8 py-4 bg-primary text-on-primary rounded-xl font-semibold shadow-xl shadow-primary/10 hover:scale-[1.02] active:scale-[0.98] transition-all">
                  <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 1" }}>psychology</span>
                  <span>Analyze Sentiment</span>
                </button>
              </div>
            </div>
          </div>

          {/* Bento Hints */}
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
        </section>
    </main>
  );
}
