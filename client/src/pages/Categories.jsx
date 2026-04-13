import { useState } from 'react';

const ICONS = ['folder', 'favorite', 'work', 'eco'];
const COLORS = [
  { name: 'primary', bg: 'bg-primary', ring: 'ring-primary' },
  { name: 'tertiary', bg: 'bg-tertiary', ring: '' },
  { name: 'stone', bg: 'bg-stone-400', ring: '' },
  { name: 'error', bg: 'bg-error', ring: '' },
];

const categories = [
  {
    id: 1,
    icon: 'work',
    iconBg: 'bg-primary-container',
    iconColor: 'text-primary',
    count: '24 ENTRIES',
    name: 'Công việc',
    desc: 'Professional growth and milestones',
    watermark: 'work',
    span: '',
  },
  {
    id: 2,
    icon: 'home',
    iconBg: 'bg-tertiary-container',
    iconColor: 'text-tertiary',
    count: '18 ENTRIES',
    name: 'Gia đình',
    desc: 'Connections and shared moments',
    watermark: 'home',
    span: '',
  },
  {
    id: 3,
    icon: 'self_improvement',
    iconBg: 'bg-primary-fixed',
    iconColor: 'text-primary-dim',
    count: '42 ENTRIES',
    name: 'Bản thân',
    desc: 'Mental health and inner reflection',
    watermark: 'self_improvement',
    span: '',
  },
  {
    id: 4,
    icon: 'palette',
    iconBg: 'bg-surface-container-highest',
    iconColor: 'text-on-surface-variant',
    count: '12 ENTRIES',
    name: 'Sáng tạo',
    desc: 'Ideas, art, and inspiration sparks',
    watermark: 'palette',
    span: '',
  },
  {
    id: 5,
    icon: 'explore',
    iconBg: 'bg-primary-fixed',
    iconColor: 'text-primary',
    count: '07 ENTRIES',
    name: 'Du lịch',
    desc: 'Wanderlust memories and future destinations',
    watermark: 'map',
    span: 'md:col-span-2',
  },
];

export default function Categories() {
  const [selectedIcon, setSelectedIcon] = useState('folder');
  const [selectedColor, setSelectedColor] = useState('primary');

  return (
    <main className="md:ml-72 flex-grow pt-20 md:pt-12 px-4 md:px-12 pb-12 overflow-y-auto">
      {/* Header */}
      <header className="mb-12 max-w-5xl mx-auto flex flex-col md:flex-row md:justify-between md:items-end gap-4">
        <div>
          <span className="text-xs font-bold tracking-[0.2em] text-primary uppercase mb-2 block">Organization</span>
          <h2 className="text-5xl font-extrabold tracking-tight text-on-background">Categories</h2>
        </div>
        <div className="text-right">
          <p className="text-on-surface-variant max-w-xs leading-relaxed">
            Organize your reflections into curated sanctuaries of thought and intent.
          </p>
        </div>
      </header>

      <div className="max-w-5xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* New Category Form */}
        <section className="lg:col-span-4 flex flex-col gap-8">
          <div className="bg-surface-container-low rounded-[2rem] p-8 flex flex-col gap-6 border border-outline-variant/20">
            <div className="flex items-center gap-3">
              <span className="material-symbols-outlined text-primary">folder_zip</span>
              <h3 className="text-xl font-semibold">New Category</h3>
            </div>
            <form className="flex flex-col gap-6" onSubmit={e => e.preventDefault()}>
              <div className="space-y-2">
                <label className="text-xs font-bold tracking-widest uppercase text-on-surface-variant">Category Name</label>
                <input
                  className="w-full bg-surface-container-lowest border border-outline-variant/30 rounded-xl p-4 focus:ring-2 focus:ring-primary/20 text-on-surface transition-all placeholder:text-stone-300"
                  placeholder="e.g. Dream Journaling"
                  type="text"
                />
              </div>

              {/* Icon Picker */}
              <div className="space-y-2">
                <label className="text-xs font-bold tracking-widest uppercase text-on-surface-variant">Icon</label>
                <div className="grid grid-cols-4 gap-2">
                  {ICONS.map(icon => (
                    <button
                      key={icon}
                      type="button"
                      onClick={() => setSelectedIcon(icon)}
                      className={`aspect-square rounded-xl flex items-center justify-center transition-colors ${
                        selectedIcon === icon
                          ? 'bg-primary text-on-primary'
                          : 'bg-surface-container-lowest border border-outline-variant/30 hover:bg-surface-container'
                      }`}
                    >
                      <span className="material-symbols-outlined">{icon}</span>
                    </button>
                  ))}
                </div>
              </div>

              {/* Color Picker */}
              <div className="space-y-2">
                <label className="text-xs font-bold tracking-widest uppercase text-on-surface-variant">Color Theme</label>
                <div className="flex gap-3">
                  {COLORS.map(color => (
                    <span
                      key={color.name}
                      onClick={() => setSelectedColor(color.name)}
                      className={`w-6 h-6 rounded-full cursor-pointer transition-transform hover:scale-110 ${color.bg} ${
                        selectedColor === color.name ? 'ring-2 ring-offset-2 ' + color.ring : ''
                      }`}
                    />
                  ))}
                </div>
              </div>

              <button className="mt-4 w-full py-4 bg-primary text-on-primary rounded-xl font-medium text-sm flex items-center justify-center gap-2 hover:shadow-lg hover:shadow-primary/20 transition-all">
                Create Sanctuary
              </button>
            </form>
          </div>

          {/* Quote */}
          <div className="bg-surface-container-highest rounded-[2rem] p-8 border border-outline-variant/20">
            <p className="text-sm leading-relaxed text-on-surface-variant italic">
              "The way we categorize our thoughts defines the geography of our inner world."
            </p>
          </div>
        </section>

        {/* Categories Grid */}
        <section className="lg:col-span-8 grid grid-cols-1 md:grid-cols-2 gap-6 content-start">
          {categories.map(cat => (
            <div
              key={cat.id}
              className={`group bg-surface-container-low border border-outline-variant/20 hover:bg-white hover:shadow-xl hover:shadow-stone-200/50 transition-all duration-500 rounded-[2rem] p-8 flex flex-col justify-between h-64 cursor-pointer relative overflow-hidden ${cat.span}`}
            >
              <div className="flex justify-between items-start z-10">
                <div className={`w-12 h-12 ${cat.iconBg} rounded-2xl flex items-center justify-center ${cat.iconColor}`}>
                  <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 1" }}>{cat.icon}</span>
                </div>
                <span className="text-xs font-bold tracking-widest text-on-surface-variant">{cat.count}</span>
              </div>
              <div className="z-10">
                <h4 className="text-2xl font-bold mb-1">{cat.name}</h4>
                <p className="text-sm text-on-surface-variant">{cat.desc}</p>
              </div>
              <div className="absolute -right-4 -bottom-4 opacity-[0.03] group-hover:opacity-[0.07] transition-opacity">
                <span className="material-symbols-outlined text-[10rem]">{cat.watermark}</span>
              </div>
            </div>
          ))}
        </section>
      </div>

      {/* Footer Decoration */}
      <footer className="mt-24 max-w-5xl mx-auto flex items-center justify-center border-t border-outline-variant/20 pt-12">
        <div className="flex items-center gap-6 text-on-surface-variant/40">
          <span className="w-2 h-2 rounded-full bg-outline-variant"></span>
          <span className="text-[10px] tracking-[0.5em] uppercase">Quiet Your Mind</span>
          <span className="w-2 h-2 rounded-full bg-outline-variant"></span>
        </div>
      </footer>
    </main>
  );
}
