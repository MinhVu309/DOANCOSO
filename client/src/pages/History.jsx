import { useState, useEffect } from 'react';
import client from '../api/client';

// Maps backend mood_color → inline style values
const MOOD_STYLE = {
  green:  { color: '#5b614d', bg: 'rgba(91,97,77,0.08)',  border: 'rgba(91,97,77,0.15)' },
  gray:   { color: '#6D6B62', bg: 'rgba(240,238,230,0.6)', border: 'rgba(217,216,205,0.4)' },
  purple: { color: '#6B538A', bg: 'rgba(107,83,138,0.08)', border: 'rgba(107,83,138,0.15)' },
  blue:   { color: '#2D6A8A', bg: 'rgba(45,106,138,0.08)', border: 'rgba(45,106,138,0.15)' },
  orange: { color: '#885a30', bg: 'rgba(136,90,48,0.08)',  border: 'rgba(136,90,48,0.15)' },
  red:    { color: '#a54731', bg: 'rgba(165,71,49,0.12)',  border: '' },
  brown:  { color: '#7a5c3a', bg: 'rgba(122,92,58,0.08)', border: 'rgba(122,92,58,0.15)' },
};

function formatDate(isoString) {
  if (!isoString) return { day: '—', month: '—' };
  const d = new Date(isoString);
  return {
    day: String(d.getDate()).padStart(2, '0'),
    month: d.toLocaleDateString('en-US', { month: 'short' }).toUpperCase(),
  };
}

function EntryCard({ entry }) {
  const { day, month } = formatDate(entry.created_at);
  const analysis = entry.analysis;
  const moodStyle = MOOD_STYLE[analysis?.mood_color] || MOOD_STYLE.gray;
  const moodLabel = analysis?.mood_label_vi || '—';

  return (
    <div className="bg-surface-container-highest p-8 rounded-3xl flex flex-col gap-6 shadow-sm border border-outline-variant/20 hover:-translate-y-1 transition-transform duration-300">
      <div className="flex justify-between items-start">
        <div className="flex flex-col">
          <span className="text-3xl font-extrabold text-primary">{day}</span>
          <span className="text-xs font-bold tracking-widest uppercase text-on-surface-variant">{month}</span>
        </div>
        <div
          className="px-4 py-1 rounded-full border"
          style={{ backgroundColor: moodStyle.bg, borderColor: moodStyle.border || 'transparent' }}
        >
          <span className="text-xs font-semibold uppercase tracking-tighter" style={{ color: moodStyle.color }}>
            {moodLabel}
          </span>
        </div>
      </div>

      <div className="space-y-3">
        {entry.title && <h4 className="text-xl font-bold text-on-surface">{entry.title}</h4>}
        <p className="text-on-surface-variant leading-relaxed line-clamp-3">{entry.content}</p>
      </div>

      {analysis?.ai_summary && (
        <div className="p-4 bg-surface-container-low/80 rounded-2xl flex items-center gap-3 border border-outline-variant/20">
          <span className="material-symbols-outlined text-primary" style={{ fontVariationSettings: "'FILL' 1" }}>
            auto_awesome
          </span>
          <p className="text-sm italic text-on-surface-variant">"{analysis.ai_summary}"</p>
        </div>
      )}

      {analysis?.condition && (
        <div className="flex items-center gap-2 pt-2 border-t border-outline-variant/20">
          <span className="material-symbols-outlined text-sm" style={{ color: '#6B538A', fontVariationSettings: "'FILL' 1" }}>neurology</span>
          <span className="text-xs text-on-surface-variant">
            <span className="font-semibold text-on-surface">{analysis.condition}</span>
            {analysis.condition_confidence != null && (
              <span className="ml-1 opacity-60">· {Math.round(analysis.condition_confidence * 100)}%</span>
            )}
          </span>
        </div>
      )}

      {entry.user_tags?.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {entry.user_tags.map(tag => (
            <span key={tag} className="px-3 py-1 bg-surface-container-low text-[10px] font-bold uppercase tracking-widest rounded-full text-on-primary-fixed-variant border border-outline-variant/30">
              #{tag}
            </span>
          ))}
          {analysis?.ai_tags?.map(tag => (
            <span key={tag} className="px-3 py-1 bg-primary/5 text-[10px] font-bold uppercase tracking-widest rounded-full text-primary border border-primary/15">
              {tag}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}

function EntryCardSmall({ entry }) {
  const d = new Date(entry.created_at);
  const dateStr = `${String(d.getDate()).padStart(2, '0')} ${d.toLocaleDateString('en-US', { month: 'short' }).toUpperCase()}`;
  const analysis = entry.analysis;
  const moodLabel = analysis?.mood_label_vi || '—';
  const moodStyle = MOOD_STYLE[analysis?.mood_color] || MOOD_STYLE.gray;

  return (
    <div className="bg-surface-container p-6 rounded-3xl flex flex-col gap-4 border border-outline-variant/30 shadow-sm">
      <div className="flex justify-between items-center">
        <span className="text-xl font-bold text-primary">{dateStr}</span>
        <span className="text-[10px] font-bold uppercase tracking-widest" style={{ color: moodStyle.color }}>{moodLabel}</span>
      </div>
      <p className="text-sm text-on-surface-variant line-clamp-2">{entry.content}</p>
      {analysis && (
        <div className="flex gap-2">
          <div className="w-1.5 h-1.5 rounded-full bg-primary" />
          <div className="w-1.5 h-1.5 rounded-full bg-primary-container" />
        </div>
      )}
    </div>
  );
}

export default function History() {
  const [groups, setGroups] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    setLoading(true);
    client.get('/api/entries?grouped=true')
      .then(res => setGroups(res.data))
      .catch(() => setError('Không thể tải lịch sử. Vui lòng thử lại.'))
      .finally(() => setLoading(false));
  }, []);

  return (
    <main className="md:ml-72 flex-grow min-h-screen flex flex-col custom-scrollbar overflow-y-auto">
      {/* TopAppBar */}
      <header className="fixed top-16 md:top-0 left-0 md:left-72 right-0 z-30 flex justify-between items-center px-6 md:px-12 py-4 md:py-6 bg-background/80 backdrop-blur-xl">
        <div>
          <h2 className="text-2xl font-bold tracking-tight text-on-background">History</h2>
          <p className="text-sm text-on-surface-variant">Reviewing your mindful journey</p>
        </div>
        <div className="flex items-center gap-6">
          <button className="p-2 text-on-surface-variant hover:bg-surface-variant rounded-full transition-colors">
            <span className="material-symbols-outlined">local_fire_department</span>
          </button>
        </div>
      </header>

      <div className="mt-36 md:mt-28 px-4 md:px-12 pb-24 max-w-6xl w-full mx-auto">
        {loading && (
          <div className="flex justify-center items-center py-24">
            <span className="material-symbols-outlined text-primary text-4xl animate-spin">progress_activity</span>
          </div>
        )}

        {error && (
          <div className="p-6 bg-error/5 border border-error/20 rounded-2xl text-sm text-error text-center">
            {error}
          </div>
        )}

        {!loading && !error && groups.length === 0 && (
          <div className="flex flex-col items-center justify-center py-24 gap-4">
            <span className="material-symbols-outlined text-on-surface-variant text-6xl">history_edu</span>
            <p className="text-on-surface-variant">Chưa có nhật ký nào. Hãy bắt đầu viết!</p>
          </div>
        )}

        {groups.map((group, gi) => {
          const [monthName, year] = group.month.split(' ');
          const entries = group.entries || [];
          const featured = entries.slice(0, 2);
          const rest = entries.slice(2);

          return (
            <section key={group.month} className={gi < groups.length - 1 ? 'mb-16' : ''}>
              <div className="flex items-baseline gap-4 mb-10">
                <h3 className="text-4xl font-light text-primary">{monthName}</h3>
                <span className="text-lg text-outline font-medium tracking-widest uppercase">{year}</span>
              </div>

              {featured.length > 0 && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-10 mb-10">
                  {featured.map(entry => <EntryCard key={entry.id} entry={entry} />)}
                </div>
              )}

              {rest.length > 0 && (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {rest.map(entry => <EntryCardSmall key={entry.id} entry={entry} />)}
                </div>
              )}
            </section>
          );
        })}
      </div>

      <div className="fixed bottom-12 right-12 pointer-events-none opacity-20">
        <div className="w-48 h-48 bg-primary/10 blur-[100px] rounded-full"></div>
      </div>
    </main>
  );
}
