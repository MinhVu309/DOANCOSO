import { useState, useEffect } from 'react';
import client from '../api/client';

const DAYS_VI = ['CN', 'Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7'];

function buildSvgPath(dataPoints) {
  if (!dataPoints || dataPoints.length === 0) return { path: '', area: '', dots: [] };
  const W = 700, H = 200, PAD_TOP = 20, PAD_BOTTOM = 30;
  const usableH = H - PAD_TOP - PAD_BOTTOM;

  const pts = dataPoints.map((pt, i) => ({
    x: dataPoints.length === 1 ? W / 2 : (i / (dataPoints.length - 1)) * W,
    y: PAD_TOP + (1 - pt.mood_score) * usableH,
  }));

  if (pts.length === 1) {
    return { path: `M0,${pts[0].y} L${W},${pts[0].y}`, area: `M0,${pts[0].y} L${W},${pts[0].y} L${W},${H} L0,${H} Z`, dots: pts };
  }

  let path = `M${pts[0].x},${pts[0].y}`;
  let area = `M${pts[0].x},${pts[0].y}`;
  for (let i = 1; i < pts.length; i++) {
    const dx = (pts[i].x - pts[i - 1].x) / 3;
    const seg = ` C${pts[i-1].x+dx},${pts[i-1].y} ${pts[i].x-dx},${pts[i].y} ${pts[i].x},${pts[i].y}`;
    path += seg;
    area += seg;
  }
  area += ` L${pts[pts.length-1].x},${H} L${pts[0].x},${H} Z`;
  return { path, area, dots: pts };
}

function getLevelColor(level) {
  return level === 'Cao' ? 'bg-error' : level === 'Trung bình' ? 'bg-tertiary' : 'bg-primary';
}

const WARNING_CONFIG = {
  watch:  { label: 'Theo dõi',  classes: 'bg-primary-container text-on-primary-container' },
  alert:  { label: 'Chú ý',     classes: 'bg-tertiary-container text-on-tertiary-container' },
  urgent: { label: 'Khẩn cấp',  classes: 'bg-error text-on-error' },
};

function formatDate(isoString) {
  if (!isoString) return '—';
  const d = new Date(isoString);
  return `${d.getDate().toString().padStart(2, '0')}/${(d.getMonth() + 1).toString().padStart(2, '0')}`;
}


function ConditionCard({ item }) {
  const isConfirmed = item.confirmed;
  const warnCfg = WARNING_CONFIG[item.warning_level];
  const hasCodes = item.dsm5_code || item.icd11_code;

  return (
    <div className={`flex items-start gap-4 p-5 rounded-2xl border transition-all ${
      isConfirmed
        ? 'bg-error-container/40 border-error/20 text-on-error-container'
        : 'bg-surface-container border-outline-variant/20 text-on-surface'
    }`}>
      <span
        className={`material-symbols-outlined text-2xl mt-0.5 shrink-0 ${
          isConfirmed ? 'text-error' : 'text-on-surface-variant'
        }`}
        style={{ fontVariationSettings: "'FILL' 1" }}
      >
        {isConfirmed ? 'warning' : 'monitoring'}
      </span>

      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 flex-wrap mb-2">
          <span className={`text-[10px] font-black uppercase tracking-widest px-2.5 py-0.5 rounded-full ${
            isConfirmed
              ? 'bg-error text-on-error'
              : 'bg-surface-container-high text-on-surface-variant'
          }`}>
            {isConfirmed ? 'Cần chú ý' : 'Đang theo dõi'}
          </span>
          {warnCfg && (
            <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${warnCfg.classes}`}>
              {warnCfg.label}
            </span>
          )}
          <span className="font-bold text-sm truncate">{item.condition_name}</span>
        </div>

        <div className="flex flex-wrap items-center gap-x-4 gap-y-1 text-xs">
          <span className="font-semibold">{item.occurrence_count} lần</span>
          <span className="opacity-70">
            TB {Math.round((item.intensity_score ?? item.avg_confidence) * 100)}%
          </span>
          {item.consecutive_days != null && (
            <span className="opacity-70">{item.consecutive_days} ngày liên tiếp</span>
          )}
          <span className="opacity-60">
            {formatDate(item.first_seen_at)} → {formatDate(item.last_seen_at)}
          </span>
        </div>

        {hasCodes && (
          <div className="flex gap-3 mt-2 text-[10px] font-mono opacity-50">
            {item.dsm5_code && <span>DSM-5: {item.dsm5_code}</span>}
            {item.icd11_code && <span>ICD-11: {item.icd11_code}</span>}
          </div>
        )}
      </div>
    </div>
  );
}

export default function Trends() {
  const [period, setPeriod] = useState('week');
  const [moodChart, setMoodChart] = useState(null);
  const [streak, setStreak] = useState(null);
  const [mentalIndex, setMentalIndex] = useState(null);
  const [topEmotions, setTopEmotions] = useState(null);
  const [mentalHealth, setMentalHealth] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    Promise.all([
      client.get(`/api/trends/mood-chart?period=${period}`),
      client.get('/api/trends/streak'),
      client.get(`/api/trends/mental-index?period=${period}`),
      client.get(`/api/trends/top-emotions?period=${period}`),
      client.get('/api/trends/mental-health'),
    ]).then(([chartRes, streakRes, mentalRes, emotionsRes, mhRes]) => {
      setMoodChart(chartRes.data);
      setStreak(streakRes.data);
      setMentalIndex(mentalRes.data);
      setTopEmotions(emotionsRes.data);
      setMentalHealth(mhRes.data);
    }).catch(() => {}).finally(() => setLoading(false));
  }, [period]);

  const svgData = buildSvgPath(moodChart?.data_points || []);
  const primaryColor = '#5b614d';

  const xLabels = moodChart?.data_points?.map(pt => {
    const d = new Date(pt.date);
    return DAYS_VI[d.getDay()];
  }) || DAYS_VI;

  const mentalRows = mentalIndex ? [
    { label: 'Căng thẳng', level: mentalIndex.stress_level,     percent: Math.round(mentalIndex.stress_score * 100) },
    { label: 'Lo âu',       level: mentalIndex.anxiety_level,    percent: Math.round(mentalIndex.anxiety_score * 100) },
    { label: 'Trầm cảm',   level: mentalIndex.depression_level, percent: Math.round(mentalIndex.depression_score * 100) },
  ] : [
    { label: 'Căng thẳng', level: '—', percent: 0 },
    { label: 'Lo âu',       level: '—', percent: 0 },
    { label: 'Trầm cảm',   level: '—', percent: 0 },
  ];

  const confirmedConditions = mentalHealth?.conditions?.filter(c => c.confirmed) ?? [];
  const pendingConditions   = mentalHealth?.conditions?.filter(c => !c.confirmed) ?? [];

  return (
    <main className="flex-1 md:ml-72 overflow-y-auto min-h-screen pb-12 pt-16 md:pt-0">
      {/* Header */}
      <header className="sticky top-0 z-30 px-6 md:px-12 py-5 md:py-8 bg-background/80 backdrop-blur-xl flex justify-between items-center">
        <div>
          <h2 className="text-3xl font-extrabold tracking-tight text-on-background">Phân tích xu hướng</h2>
          <p className="text-on-surface-variant font-medium">Khám phá hành trình tâm trí của bạn</p>
        </div>
        <div className="flex gap-2">
          {['week', 'month'].map(p => (
            <button
              key={p}
              onClick={() => setPeriod(p)}
              className={`px-4 py-2 rounded-full text-xs font-bold uppercase tracking-wider transition-all ${
                period === p
                  ? 'bg-primary text-on-primary'
                  : 'bg-surface-container text-on-surface-variant hover:bg-surface-container-high'
              }`}
            >
              {p === 'week' ? 'Tuần' : 'Tháng'}
            </button>
          ))}
        </div>
      </header>

      <div className="px-4 md:px-12 flex flex-col gap-8">
        {/* Two-column grid */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-8">
          {/* Left */}
          <section className="md:col-span-8 flex flex-col gap-8">
            {/* Mood Chart */}
            <div className="bg-surface-container-low p-8 rounded-[2.5rem] relative overflow-hidden border border-outline-variant/20">
              <div className="flex justify-between items-center mb-10">
                <div>
                  <h3 className="text-xl font-bold">Biến động tâm trạng</h3>
                  <p className="text-sm text-on-surface-variant">
                    {period === 'week' ? 'Thống kê 7 ngày qua' : 'Thống kê 30 ngày qua'}
                  </p>
                </div>
                <span className="px-3 py-1 rounded-full bg-surface-container-lowest text-xs font-semibold uppercase tracking-wider text-on-surface-variant border border-outline-variant/30">
                  {period === 'week' ? 'Tuần này' : 'Tháng này'}
                </span>
              </div>
              <div className="h-64 flex items-end justify-between gap-4 relative">
                <div className="absolute inset-0 flex items-end pb-8">
                  {loading ? (
                    <div className="w-full h-full flex items-center justify-center">
                      <span className="material-symbols-outlined text-primary animate-spin">progress_activity</span>
                    </div>
                  ) : moodChart?.data_points?.length > 0 ? (
                    <svg className="w-full h-full" preserveAspectRatio="none" viewBox="0 0 700 200">
                      <path d={svgData.area} fill={primaryColor} className="opacity-10" />
                      <path d={svgData.path} fill="none" stroke={primaryColor} strokeWidth="4" strokeLinecap="round" />
                      {svgData.dots.map((pt, i) => (
                        <circle key={i} cx={pt.x} cy={pt.y} r="5" fill={primaryColor} />
                      ))}
                    </svg>
                  ) : (
                    <div className="w-full flex items-center justify-center">
                      <p className="text-sm text-on-surface-variant">Chưa có dữ liệu trong kỳ này</p>
                    </div>
                  )}
                </div>
                <div className="w-full flex justify-between absolute bottom-0 left-0 text-[10px] uppercase tracking-widest text-on-surface-variant/60 font-bold">
                  {xLabels.map((d, i) => <span key={i}>{d}</span>)}
                </div>
              </div>
            </div>

            {/* Top Emotions */}
            <div className="bg-surface-container-low p-8 rounded-[2.5rem] border border-outline-variant/20">
              <h3 className="text-xl font-bold mb-6">Cảm xúc phổ biến</h3>
              {loading ? (
                <span className="material-symbols-outlined text-primary animate-spin">progress_activity</span>
              ) : (
                <div className="flex flex-wrap gap-3">
                  {topEmotions?.emotions?.length > 0 ? topEmotions.emotions.map((e, i) => (
                    <span
                      key={e.label}
                      className={`px-6 py-3 rounded-full font-medium text-sm ${
                        i === 0 ? 'bg-primary-container text-on-primary-container shadow-sm' :
                        i === 3 ? 'bg-tertiary-container text-on-tertiary-container shadow-sm' :
                        'bg-surface-container-lowest text-on-surface border border-outline-variant/30'
                      }`}
                    >
                      {e.label_vi}
                      <span className="ml-2 text-xs opacity-60">({e.count})</span>
                    </span>
                  )) : (
                    <p className="text-sm text-on-surface-variant">Chưa có dữ liệu cảm xúc</p>
                  )}
                </div>
              )}
            </div>
          </section>

          {/* Right */}
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
                <p className="text-4xl font-black mb-2">
                  {streak ? streak.current_streak : '—'} <span className="text-lg font-medium opacity-80">ngày liên tiếp</span>
                </p>
                {streak && (
                  <p className="text-sm opacity-80 mb-3">
                    Dài nhất: {streak.longest_streak} ngày · Tổng: {streak.total_entries} bài
                  </p>
                )}
                <p className="text-sm opacity-90 leading-relaxed">
                  {streak?.current_streak > 0
                    ? 'Tuyệt vời! Hãy tiếp tục duy trì thói quen này.'
                    : 'Hãy bắt đầu chuỗi của bạn ngay hôm nay!'}
                </p>
              </div>
              <span className="material-symbols-outlined absolute -bottom-10 -right-10 text-[180px] opacity-10 rotate-12 group-hover:rotate-0 transition-transform duration-700">
                local_fire_department
              </span>
            </div>

            {/* Mental Indices */}
            <div className="bg-surface-container-low p-8 rounded-[2.5rem] flex flex-col gap-8 border border-outline-variant/20">
              <h3 className="text-xl font-bold">Chỉ số tinh thần</h3>
              <div className="space-y-6">
                {mentalRows.map(row => (
                  <div key={row.label} className="space-y-2">
                    <div className="flex justify-between items-center text-sm font-semibold">
                      <span>{row.label}</span>
                      <span className="text-on-surface-variant">{row.level}</span>
                    </div>
                    <div className="h-2 w-full bg-surface-container-highest rounded-full overflow-hidden">
                      <div
                        className={`h-full rounded-full transition-all duration-500 ${getLevelColor(row.level)}`}
                        style={{ width: `${Math.max(row.percent, 2)}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
              <div className="mt-4 p-4 rounded-2xl bg-surface-container-high/40 border border-outline-variant/10">
                <p className="text-xs leading-relaxed text-on-surface-variant italic">
                  {mentalIndex?.note || '* Các chỉ số này mang tính chất tham khảo dựa trên từ ngữ trong nhật ký của bạn.'}
                </p>
              </div>
            </div>

            {/* Insight */}
            <div className="bg-surface-container-high p-8 rounded-[2.5rem] flex items-start gap-4 border border-outline-variant/20">
              <span className="material-symbols-outlined text-tertiary">lightbulb</span>
              <div>
                <h4 className="font-bold mb-1">Gợi ý hôm nay</h4>
                <p className="text-sm text-on-surface-variant leading-relaxed">
                  {topEmotions?.emotions?.[0]
                    ? `Bạn thường cảm thấy "${topEmotions.emotions[0].label_vi}" nhất. Hãy quan tâm đến sức khoẻ tinh thần của mình.`
                    : 'Hãy viết nhật ký đều đặn để nhận gợi ý cá nhân hoá.'}
                </p>
              </div>
            </div>
          </section>
        </div>

        {/* Mental Health Conditions — full width */}
        <section className="bg-surface-container-low p-8 rounded-[2.5rem] border border-outline-variant/20">
          <div className="flex items-start justify-between gap-4 mb-6">
            <div>
              <h3 className="text-xl font-bold flex items-center gap-2">
                <span
                  className="material-symbols-outlined text-2xl text-secondary"
                  style={{ fontVariationSettings: "'FILL' 1" }}
                >
                  psychology
                </span>
                Dự đoán tình trạng tâm thần
              </h3>
              <p className="text-sm text-on-surface-variant mt-1">
                Tích lũy từ nhiều bài viết trong {mentalHealth?.window_days ?? 30} ngày qua
              </p>
            </div>
          </div>

          {loading ? (
            <div className="flex items-center gap-3 text-on-surface-variant py-4">
              <span className="material-symbols-outlined animate-spin">progress_activity</span>
              <span className="text-sm">Đang phân tích...</span>
            </div>
          ) : mentalHealth?.conditions?.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-10 gap-3 text-on-surface-variant">
              <span
                className="material-symbols-outlined text-5xl opacity-30"
                style={{ fontVariationSettings: "'FILL' 1" }}
              >
                sentiment_satisfied
              </span>
              <p className="text-sm font-medium">Chưa phát hiện tình trạng đáng lo ngại</p>
              <p className="text-xs opacity-60">Tiếp tục viết nhật ký để AI theo dõi xu hướng của bạn</p>
            </div>
          ) : (
            <div className="space-y-6">
              {/* Confirmed */}
              {confirmedConditions.length > 0 && (
                <div>
                  <p className="text-xs font-black uppercase tracking-widest text-error mb-3 flex items-center gap-1.5">
                    <span className="material-symbols-outlined text-base">warning</span>
                    Cần chú ý ({confirmedConditions.length})
                  </p>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {confirmedConditions.map(item => (
                      <ConditionCard key={item.condition_name} item={item} />
                    ))}
                  </div>
                </div>
              )}

              {/* Pending */}
              {pendingConditions.length > 0 && (
                <div>
                  <p className="text-xs font-black uppercase tracking-widest text-on-surface-variant mb-3 flex items-center gap-1.5">
                    <span className="material-symbols-outlined text-base">monitoring</span>
                    Đang theo dõi ({pendingConditions.length})
                  </p>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {pendingConditions.map(item => (
                      <ConditionCard key={item.condition_name} item={item} />
                    ))}
                  </div>
                </div>
              )}

              {/* Disclaimer */}
              <div className="flex items-start gap-2 pt-2 border-t border-outline-variant/20">
                <span className="material-symbols-outlined text-base text-on-surface-variant opacity-60 shrink-0 mt-0.5">info</span>
                <div>
                  <p className="text-xs text-on-surface-variant opacity-60 leading-relaxed">
                    {mentalHealth?.disclaimer?.vi || 'Đây là dự đoán từ AI dựa trên ngôn ngữ trong nhật ký, không phải chẩn đoán y tế. Nếu lo lắng về sức khoẻ tâm thần, hãy tham khảo ý kiến chuyên gia.'}
                  </p>
                  {mentalHealth?.disclaimer?.source && (
                    <p className="text-[10px] text-on-surface-variant opacity-40 mt-1 font-mono">
                      {mentalHealth.disclaimer.source}
                    </p>
                  )}
                </div>
              </div>
            </div>
          )}
        </section>
      </div>
    </main>
  );
}
