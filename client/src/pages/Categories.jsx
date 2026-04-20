import { useState, useEffect } from 'react';
import client from '../api/client';

const ICONS = ['folder', 'favorite', 'work', 'eco', 'explore', 'palette'];

const COLOR_OPTIONS = [
  { label: 'Xanh lá', value: '#5b614d', bg: 'bg-[#5b614d]' },
  { label: 'Nâu ấm',  value: '#885a30', bg: 'bg-[#885a30]' },
  { label: 'Đá xám',  value: '#6D6B62', bg: 'bg-[#6D6B62]' },
  { label: 'Đỏ gạch', value: '#a54731', bg: 'bg-[#a54731]' },
];

function CategoryCard({ cat, onDelete }) {
  return (
    <div className="group bg-surface-container-low border border-outline-variant/20 hover:bg-white hover:shadow-xl hover:shadow-stone-200/50 transition-all duration-500 rounded-[2rem] p-8 flex flex-col justify-between h-64 cursor-pointer relative overflow-hidden">
      <div className="flex justify-between items-start z-10">
        <div
          className="w-12 h-12 rounded-2xl flex items-center justify-center"
          style={{ backgroundColor: cat.color_theme + '22', color: cat.color_theme }}
        >
          <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 1" }}>{cat.icon}</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs font-bold tracking-widest text-on-surface-variant">
            {cat.entry_count} ENTRIES
          </span>
          <button
            onClick={e => { e.stopPropagation(); onDelete(cat.id); }}
            className="opacity-0 group-hover:opacity-100 p-1 rounded-lg hover:bg-error/10 text-error transition-all"
          >
            <span className="material-symbols-outlined text-base">delete</span>
          </button>
        </div>
      </div>
      <div className="z-10">
        <h4 className="text-2xl font-bold mb-1">{cat.name}</h4>
        <div className="flex items-center gap-1.5">
          <div className="w-2 h-2 rounded-full" style={{ backgroundColor: cat.color_theme }} />
          <p className="text-sm text-on-surface-variant">{cat.icon}</p>
        </div>
      </div>
      <div className="absolute -right-4 -bottom-4 opacity-[0.03] group-hover:opacity-[0.07] transition-opacity">
        <span className="material-symbols-outlined text-[10rem]">{cat.icon}</span>
      </div>
    </div>
  );
}

export default function Categories() {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [formName, setFormName] = useState('');
  const [formIcon, setFormIcon] = useState('folder');
  const [formColor, setFormColor] = useState('#5b614d');
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchCategories();
  }, []);

  async function fetchCategories() {
    setLoading(true);
    try {
      const res = await client.get('/api/categories');
      setCategories(res.data);
    } catch {
      // fail silently
    } finally {
      setLoading(false);
    }
  }

  async function handleCreate(e) {
    e.preventDefault();
    if (!formName.trim()) { setError('Vui lòng nhập tên danh mục.'); return; }
    setSaving(true);
    setError('');
    try {
      await client.post('/api/categories', { name: formName.trim(), icon: formIcon, color_theme: formColor });
      setFormName('');
      setFormIcon('folder');
      setFormColor('#5b614d');
      await fetchCategories();
    } catch (err) {
      const msg = err.response?.data?.detail;
      setError(typeof msg === 'string' ? msg : 'Không thể tạo danh mục.');
    } finally {
      setSaving(false);
    }
  }

  async function handleDelete(id) {
    if (!window.confirm('Xoá danh mục này? Các bài viết trong danh mục sẽ không bị xoá.')) return;
    try {
      await client.delete(`/api/categories/${id}`);
      setCategories(prev => prev.filter(c => c.id !== id));
    } catch {
      alert('Không thể xoá danh mục.');
    }
  }

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
        {/* Form */}
        <section className="lg:col-span-4 flex flex-col gap-8">
          <div className="bg-surface-container-low rounded-[2rem] p-8 flex flex-col gap-6 border border-outline-variant/20">
            <div className="flex items-center gap-3">
              <span className="material-symbols-outlined text-primary">folder_zip</span>
              <h3 className="text-xl font-semibold">New Category</h3>
            </div>
            <form className="flex flex-col gap-6" onSubmit={handleCreate}>
              <div className="space-y-2">
                <label className="text-xs font-bold tracking-widest uppercase text-on-surface-variant">Tên danh mục</label>
                <input
                  className="w-full bg-surface-container-lowest border border-outline-variant/30 rounded-xl p-4 focus:ring-2 focus:ring-primary/20 text-on-surface transition-all placeholder:text-stone-300"
                  placeholder="Ví dụ: Du lịch"
                  value={formName}
                  onChange={e => { setFormName(e.target.value); setError(''); }}
                />
              </div>

              {/* Icon Picker */}
              <div className="space-y-2">
                <label className="text-xs font-bold tracking-widest uppercase text-on-surface-variant">Icon</label>
                <div className="grid grid-cols-6 gap-2">
                  {ICONS.map(icon => (
                    <button
                      key={icon}
                      type="button"
                      onClick={() => setFormIcon(icon)}
                      className={`aspect-square rounded-xl flex items-center justify-center transition-colors ${
                        formIcon === icon
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
                <label className="text-xs font-bold tracking-widest uppercase text-on-surface-variant">Màu chủ đề</label>
                <div className="flex gap-3">
                  {COLOR_OPTIONS.map(c => (
                    <button
                      key={c.value}
                      type="button"
                      onClick={() => setFormColor(c.value)}
                      className={`w-7 h-7 rounded-full transition-transform hover:scale-110 ${c.bg} ${
                        formColor === c.value ? 'ring-2 ring-offset-2 ring-on-surface/30' : ''
                      }`}
                      title={c.label}
                    />
                  ))}
                </div>
              </div>

              {error && <p className="text-sm text-error">{error}</p>}

              <button
                type="submit"
                disabled={saving}
                className="mt-4 w-full py-4 bg-primary text-on-primary rounded-xl font-medium text-sm flex items-center justify-center gap-2 hover:shadow-lg hover:shadow-primary/20 disabled:opacity-50 transition-all"
              >
                {saving && <span className="material-symbols-outlined animate-spin text-base">progress_activity</span>}
                Create Sanctuary
              </button>
            </form>
          </div>

          <div className="bg-surface-container-highest rounded-[2rem] p-8 border border-outline-variant/20">
            <p className="text-sm leading-relaxed text-on-surface-variant italic">
              "The way we categorize our thoughts defines the geography of our inner world."
            </p>
          </div>
        </section>

        {/* Grid */}
        <section className="lg:col-span-8 grid grid-cols-1 md:grid-cols-2 gap-6 content-start">
          {loading && (
            <div className="col-span-2 flex justify-center py-12">
              <span className="material-symbols-outlined text-primary text-4xl animate-spin">progress_activity</span>
            </div>
          )}
          {!loading && categories.length === 0 && (
            <div className="col-span-2 flex flex-col items-center justify-center py-16 gap-3 text-on-surface-variant">
              <span className="material-symbols-outlined text-5xl">folder_open</span>
              <p>Chưa có danh mục nào. Hãy tạo danh mục đầu tiên!</p>
            </div>
          )}
          {categories.map(cat => (
            <CategoryCard key={cat.id} cat={cat} onDelete={handleDelete} />
          ))}
        </section>
      </div>

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
