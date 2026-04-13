const DAYS = ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'CN'];

const emotions = [
  { label: 'Bình yên', className: 'bg-primary-container text-on-primary-container shadow-sm' },
  { label: 'Hào hứng', className: 'bg-surface-container-lowest text-on-surface border border-outline-variant/30' },
  { label: 'Trầm tư', className: 'bg-surface-container-lowest text-on-surface border border-outline-variant/30' },
  { label: 'Biết ơn', className: 'bg-tertiary-container text-on-tertiary-container shadow-sm' },
  { label: 'Mệt mỏi', className: 'bg-surface-container-lowest text-on-surface border border-outline-variant/30' },
  { label: 'Vui vẻ', className: 'bg-surface-container-lowest text-on-surface border border-outline-variant/30' },
];

const mentalIndices = [
  { label: 'Căng thẳng', level: 'Thấp', percent: 25, color: 'bg-primary' },
  { label: 'Lo âu', level: 'Trung bình', percent: 45, color: 'bg-tertiary' },
  { label: 'Trầm cảm', level: 'Thấp', percent: 15, color: 'bg-primary' },
];

export default function Trends() {
  return (
    <main className="flex-1 md:ml-72 overflow-y-auto min-h-screen pb-12 pt-16 md:pt-0">
      {/* Header */}
      <header className="sticky top-0 z-30 px-6 md:px-12 py-5 md:py-8 bg-background/80 backdrop-blur-xl flex justify-between items-center">
        <div>
          <h2 className="text-3xl font-extrabold tracking-tight text-on-background">Phân tích xu hướng</h2>
          <p className="text-on-surface-variant font-medium">Khám phá hành trình tâm trí của bạn</p>
        </div>
        <div className="flex gap-4">
          <button className="p-3 rounded-full hover:bg-surface-container-high transition-colors text-on-surface-variant">
            <span className="material-symbols-outlined">local_fire_department</span>
          </button>
          <button className="p-3 rounded-full hover:bg-surface-container-high transition-colors text-on-surface-variant">
            <span className="material-symbols-outlined">settings</span>
          </button>
        </div>
      </header>

      <div className="px-4 md:px-12 grid grid-cols-1 md:grid-cols-12 gap-8">
        {/* Left: Mood Chart & Emotions */}
        <section className="md:col-span-8 flex flex-col gap-8">
          {/* Mood Chart */}
          <div className="bg-surface-container-low p-8 rounded-[2.5rem] relative overflow-hidden border border-outline-variant/20">
            <div className="flex justify-between items-center mb-10">
              <div>
                <h3 className="text-xl font-bold">Biến động tâm trạng</h3>
                <p className="text-sm text-on-surface-variant">Thống kê 7 ngày qua</p>
              </div>
              <span className="px-3 py-1 rounded-full bg-surface-container-lowest text-xs font-semibold uppercase tracking-wider text-on-surface-variant border border-outline-variant/30">
                Tuần này
              </span>
            </div>
            <div className="h-64 flex items-end justify-between gap-4 relative">
              <div className="absolute inset-0 flex items-end pb-8">
                <svg className="w-full h-full" preserveAspectRatio="none" viewBox="0 0 700 200">
                  <path
                    d="M0,150 C100,120 150,180 250,140 S400,60 500,100 S650,40 700,60"
                    fill="none" stroke="#5b614d" strokeLinecap="round" strokeWidth="4"
                  />
                  <path
                    className="opacity-10"
                    d="M0,150 C100,120 150,180 250,140 S400,60 500,100 S650,40 700,60 L700,200 L0,200 Z"
                    fill="#5b614d"
                  />
                  <circle cx="250" cy="140" fill="#5b614d" r="6" />
                  <circle cx="500" cy="100" fill="#5b614d" r="6" />
                </svg>
              </div>
              <div className="w-full flex justify-between absolute bottom-0 left-0 text-[10px] uppercase tracking-widest text-on-surface-variant/60 font-bold">
                {DAYS.map(d => <span key={d}>{d}</span>)}
              </div>
            </div>
          </div>

          {/* Common Emotions */}
          <div className="bg-surface-container-low p-8 rounded-[2.5rem] border border-outline-variant/20">
            <h3 className="text-xl font-bold mb-6">Cảm xúc phổ biến</h3>
            <div className="flex flex-wrap gap-3">
              {emotions.map(e => (
                <span key={e.label} className={`px-6 py-3 rounded-full font-medium text-sm ${e.className}`}>
                  {e.label}
                </span>
              ))}
            </div>
          </div>
        </section>

        {/* Right: Streak & Indices */}
        <section className="md:col-span-4 flex flex-col gap-8">
          {/* Streak Card */}
          <div className="fire-gradient p-8 rounded-[2.5rem] text-on-primary shadow-xl shadow-tertiary/10 relative overflow-hidden group">
            <div className="relative z-10">
              <div className="flex justify-between items-start mb-6">
                <span className="material-symbols-outlined text-4xl" style={{ fontVariationSettings: "'FILL' 1" }}>
                  local_fire_department
                </span>
                <span className="text-xs font-bold uppercase tracking-widest opacity-80">Streak</span>
              </div>
              <h4 className="text-2xl font-extrabold mb-1">Chuỗi lửa</h4>
              <p className="text-4xl font-black mb-4">
                1 ngày <span className="text-lg font-medium opacity-80">liên tiếp</span>
              </p>
              <p className="text-sm opacity-90 leading-relaxed">
                Tiếp tục duy trì thói quen viết nhật ký để thấu hiểu bản thân hơn nhé!
              </p>
            </div>
            <span className="material-symbols-outlined absolute -bottom-10 -right-10 text-[180px] opacity-10 rotate-12 group-hover:rotate-0 transition-transform duration-700">
              local_fire_department
            </span>
          </div>

          {/* Mental Health Indices */}
          <div className="bg-surface-container-low p-8 rounded-[2.5rem] flex flex-col gap-8 border border-outline-variant/20">
            <h3 className="text-xl font-bold">Chỉ số tinh thần</h3>
            <div className="space-y-6">
              {mentalIndices.map(index => (
                <div key={index.label} className="space-y-2">
                  <div className="flex justify-between items-center text-sm font-semibold">
                    <span>{index.label}</span>
                    <span className="text-on-surface-variant">{index.level}</span>
                  </div>
                  <div className="h-2 w-full bg-surface-container-highest rounded-full overflow-hidden">
                    <div className={`h-full ${index.color} rounded-full`} style={{ width: `${index.percent}%` }} />
                  </div>
                </div>
              ))}
            </div>
            <div className="mt-4 p-4 rounded-2xl bg-surface-container-high/40 border border-outline-variant/10">
              <p className="text-xs leading-relaxed text-on-surface-variant italic">
                * Các chỉ số này mang tính chất tham khảo dựa trên từ ngữ trong nhật ký của bạn. Hãy tìm sự giúp đỡ chuyên nghiệp nếu cần thiết.
              </p>
            </div>
          </div>

          {/* Insight Card */}
          <div className="bg-surface-container-high p-8 rounded-[2.5rem] flex items-start gap-4 border border-outline-variant/20">
            <span className="material-symbols-outlined text-tertiary">lightbulb</span>
            <div>
              <h4 className="font-bold mb-1">Gợi ý hôm nay</h4>
              <p className="text-sm text-on-surface-variant leading-relaxed">
                Bạn thường cảm thấy <strong>Bình yên</strong> vào buổi sáng. Hãy thử thiền 5 phút trước khi làm việc.
              </p>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}
