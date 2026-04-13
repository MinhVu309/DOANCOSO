const aprilEntries = [
  {
    id: 1,
    day: '05',
    month: 'APR',
    mood: 'Bình yên',
    moodClass: 'text-tertiary',
    moodBg: 'bg-surface-container-lowest',
    moodBorder: 'border-outline-variant/30',
    title: 'Buổi sáng bên cửa sổ',
    excerpt: 'Sáng nay thức dậy, ánh nắng len lỏi qua khe cửa sổ thật nhẹ nhàng. Tôi đã dành 15 phút chỉ để ngồi im lặng và cảm nhận hương vị cà phê...',
    aiSummary: { icon: 'auto_awesome', iconClass: 'text-primary', text: '"Tâm trạng thư thái, tích cực và đầy hy vọng cho ngày mới."' },
    tags: ['#MINDFULNESS', '#GRATITUDE'],
    cardBg: 'bg-surface-container-highest',
  },
  {
    id: 2,
    day: '03',
    month: 'APR',
    mood: 'Áp lực',
    moodClass: 'text-error',
    moodBg: 'bg-error-container/40',
    moodBorder: '',
    title: 'Những suy nghĩ dồn dập',
    excerpt: 'Công việc dạo này thật sự khiến tôi cảm thấy quá tải. Những deadline cứ nối tiếp nhau khiến giấc ngủ không còn được trọn vẹn...',
    aiSummary: { icon: 'psychology_alt', iconClass: 'text-error', text: '"Tâm trạng buồn bã, có dấu hiệu căng thẳng cao độ cần nghỉ ngơi."' },
    tags: ['#WORK', '#STRESS'],
    cardBg: 'bg-surface-container-lowest',
  },
];

const marchEntries = [
  { id: 3, date: '28 MAR', mood: 'Sáng tạo', excerpt: 'Ý tưởng về một dự án cá nhân mới vừa nảy ra...', dots: ['bg-tertiary', 'bg-primary-container'] },
  { id: 4, date: '24 MAR', mood: 'Trầm lắng', excerpt: 'Một ngày mưa buồn, tôi ngồi đọc sách một mình...', dots: ['bg-primary'] },
  { id: 5, date: '20 MAR', mood: 'Hạnh phúc', excerpt: 'Buổi gặp mặt gia đình thật ấm cúng và đầy tiếng cười...', dots: ['bg-tertiary-container', 'bg-primary'] },
];

export default function History() {
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
          <div className="w-10 h-10 rounded-full bg-surface-container-high overflow-hidden border-2 border-white shadow-sm">
            <img
              alt="User profile"
              className="w-full h-full object-cover"
              src="https://lh3.googleusercontent.com/aida-public/AB6AXuCyCs0-nIx8XzK_AK7KB7o5mHcI6f5fxgq8ZMyn0OC8qWoioTxffnDrvXXJWCWmmR6oizt3VqUgwVRGgHEaMA0PF5O7-29VppgfLlv_F4i5WpRDFUJ7CxKTcpWNKiXgM3DbeIGhFtm5gJDLWE8my0gOSynDYeud1YAh03_0kuhh0sL_SCxRaDq25XT3ZY3xAOy3Wwkh2edWG9ldhTgUAIAkMqoskjfjg4WYrjGhwBsy2GnO8tPTC41k6Ibf5w3fwDQxzukG2KOMsdE"
            />
          </div>
        </div>
      </header>

      {/* Content Canvas */}
      <div className="mt-36 md:mt-28 px-4 md:px-12 pb-24 max-w-6xl w-full mx-auto">
        {/* April 2024 */}
        <section className="mb-16">
          <div className="flex items-baseline gap-4 mb-10">
            <h3 className="text-4xl font-light text-primary">April</h3>
            <span className="text-lg text-outline font-medium tracking-widest uppercase">2024</span>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
            {aprilEntries.map(entry => (
              <div
                key={entry.id}
                className={`${entry.cardBg} p-8 rounded-3xl flex flex-col gap-6 shadow-sm border border-outline-variant/20 hover:-translate-y-1 transition-transform duration-300`}
              >
                <div className="flex justify-between items-start">
                  <div className="flex flex-col">
                    <span className="text-3xl font-extrabold text-primary">{entry.day}</span>
                    <span className="text-xs font-bold tracking-widest uppercase text-on-surface-variant">{entry.month}</span>
                  </div>
                  <div className={`px-4 py-1 ${entry.moodBg} rounded-full ${entry.moodBorder ? `border ${entry.moodBorder}` : ''}`}>
                    <span className={`text-xs font-semibold uppercase tracking-tighter ${entry.moodClass}`}>{entry.mood}</span>
                  </div>
                </div>
                <div className="space-y-3">
                  <h4 className="text-xl font-bold text-on-surface">{entry.title}</h4>
                  <p className="text-on-surface-variant leading-relaxed line-clamp-3">{entry.excerpt}</p>
                </div>
                <div className="p-4 bg-surface-container-low/80 rounded-2xl flex items-center gap-3 border border-outline-variant/20">
                  <span className={`material-symbols-outlined ${entry.aiSummary.iconClass}`} style={{ fontVariationSettings: "'FILL' 1" }}>
                    {entry.aiSummary.icon}
                  </span>
                  <p className="text-sm italic text-on-surface-variant">{entry.aiSummary.text}</p>
                </div>
                <div className="flex flex-wrap gap-2">
                  {entry.tags.map(tag => (
                    <span key={tag} className="px-3 py-1 bg-surface-container-low text-[10px] font-bold uppercase tracking-widest rounded-full text-on-primary-fixed-variant border border-outline-variant/30">
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* March 2024 */}
        <section>
          <div className="flex items-baseline gap-4 mb-10">
            <h3 className="text-4xl font-light text-primary">March</h3>
            <span className="text-lg text-outline font-medium tracking-widest uppercase">2024</span>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {marchEntries.map(entry => (
              <div key={entry.id} className="bg-surface-container p-6 rounded-3xl flex flex-col gap-4 border border-outline-variant/30 shadow-sm">
                <div className="flex justify-between items-center">
                  <span className="text-xl font-bold text-primary">{entry.date}</span>
                  <span className="text-[10px] font-bold uppercase tracking-widest text-on-surface-variant">{entry.mood}</span>
                </div>
                <p className="text-sm text-on-surface-variant line-clamp-2">{entry.excerpt}</p>
                <div className="flex gap-2">
                  {entry.dots.map((dotClass, i) => (
                    <div key={i} className={`w-1.5 h-1.5 rounded-full ${dotClass}`} />
                  ))}
                </div>
              </div>
            ))}
          </div>
        </section>
      </div>

      {/* Decoration */}
      <div className="fixed bottom-12 right-12 pointer-events-none opacity-20">
        <div className="w-48 h-48 bg-primary/10 blur-[100px] rounded-full"></div>
      </div>
    </main>
  );
}
