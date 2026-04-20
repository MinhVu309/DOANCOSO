import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import client from '../api/client';

const SECTIONS = [
  { id: 'profile',        icon: 'person',        label: 'Hồ sơ' },
  { id: 'appearance',    icon: 'palette',        label: 'Giao diện' },
  { id: 'notifications', icon: 'notifications',  label: 'Nhắc nhở' },
  { id: 'privacy',       icon: 'lock',           label: 'Quyền riêng tư' },
  { id: 'journal',       icon: 'menu_book',      label: 'Nhật ký' },
  { id: 'about',         icon: 'info',           label: 'Giới thiệu' },
];

/* ── Profile Section ── */

function ProfileSection({ profile, onSave, onAvatarUpload, onAvatarDelete, saving }) {
  const [form, setForm] = useState({
    display_name: profile?.display_name || '',
    birth_date: profile?.birth_date || '',
    timezone: profile?.timezone || 'Asia/Ho_Chi_Minh',
  });
  const fileRef = useRef();

  useEffect(() => {
    if (profile) {
      setForm({
        display_name: profile.display_name || '',
        birth_date: profile.birth_date || '',
        timezone: profile.timezone || 'Asia/Ho_Chi_Minh',
      });
    }
  }, [profile]);

  return (
    <div className="flex flex-col gap-8">
      <div>
        <h3 className="text-xl font-bold text-on-background mb-1">Hồ sơ cá nhân</h3>
        <p className="text-sm text-on-surface-variant">Thông tin hiển thị trong ứng dụng của bạn.</p>
      </div>

      {/* Avatar */}
      <div className="flex items-center gap-6">
        <div className="w-20 h-20 rounded-2xl overflow-hidden border-2 border-outline-variant/30 flex-shrink-0 bg-primary/10 flex items-center justify-center">
          {profile?.avatar_url ? (
            <img src={`http://localhost:8000${profile.avatar_url}`} alt="Avatar" className="w-full h-full object-cover" />
          ) : (
            <span className="text-primary font-bold text-3xl">
              {(profile?.display_name || 'U')[0]?.toUpperCase()}
            </span>
          )}
        </div>
        <div className="flex flex-col gap-2">
          <input type="file" accept="image/*" ref={fileRef} className="hidden" onChange={e => onAvatarUpload(e.target.files[0])} />
          <button
            onClick={() => fileRef.current?.click()}
            className="px-5 py-2 bg-primary text-on-primary rounded-xl text-sm font-medium hover:opacity-90 transition-opacity"
          >
            Đổi ảnh đại diện
          </button>
          {profile?.avatar_url && (
            <button onClick={onAvatarDelete} className="px-5 py-2 text-on-surface-variant text-sm hover:text-error transition-colors">
              Xoá ảnh
            </button>
          )}
        </div>
      </div>

      {/* Fields */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Field label="Tên hiển thị" value={form.display_name} onChange={v => setForm(f => ({ ...f, display_name: v }))} />
        <Field label="Email" value={profile?.email || ''} disabled />
        <Field label="Ngày sinh" type="date" value={form.birth_date} onChange={v => setForm(f => ({ ...f, birth_date: v }))} />
        <Field label="Múi giờ" value={form.timezone} onChange={v => setForm(f => ({ ...f, timezone: v }))} />
      </div>

      <SaveButton onClick={() => onSave(form)} saving={saving} />
    </div>
  );
}

/* ── Notifications Section ── */

function NotificationsSection({ prefs, onSave, saving }) {
  const [reminder, setReminder] = useState(prefs?.reminder_enabled ?? false);
  const [reminderTime, setReminderTime] = useState(prefs?.reminder_time || '21:00');
  const [streak, setStreak] = useState(true);
  const [weekly, setWeekly] = useState(false);

  useEffect(() => {
    if (prefs) {
      setReminder(prefs.reminder_enabled);
      setReminderTime(prefs.reminder_time || '21:00');
    }
  }, [prefs]);

  return (
    <div className="flex flex-col gap-8">
      <div>
        <h3 className="text-xl font-bold text-on-background mb-1">Nhắc nhở</h3>
        <p className="text-sm text-on-surface-variant">Đặt lịch để không bỏ lỡ ngày nào.</p>
      </div>

      <SettingRow icon="edit_note" label="Nhắc viết nhật ký" desc="Nhắc nhở hàng ngày vào giờ cố định"
        action={<Toggle value={reminder} onChange={setReminder} />} />

      {reminder && (
        <div className="ml-10 flex flex-col gap-2">
          <label className="text-xs font-bold uppercase tracking-widest text-on-surface-variant">Giờ nhắc</label>
          <input type="time" value={reminderTime} onChange={e => setReminderTime(e.target.value)}
            className="w-40 bg-surface-container-lowest border border-outline-variant/30 rounded-xl px-4 py-3 text-on-surface text-sm focus:ring-2 focus:ring-primary/20 transition-all" />
        </div>
      )}

      <SettingRow icon="local_fire_department" label="Nhắc duy trì streak" desc="Cảnh báo khi sắp mất chuỗi ngày viết"
        action={<Toggle value={streak} onChange={setStreak} />} />

      <SettingRow icon="insights" label="Báo cáo hàng tuần" desc="Tóm tắt cảm xúc và xu hướng 7 ngày qua"
        action={<Toggle value={weekly} onChange={setWeekly} />} />

      <SaveButton onClick={() => onSave({ reminder_enabled: reminder, reminder_time: reminderTime })} saving={saving} />
    </div>
  );
}

/* ── Static sections ── */

function AppearanceSection({ prefs, onSave, saving }) {
  const [theme, setTheme] = useState(prefs?.theme || 'light');

  useEffect(() => { if (prefs) setTheme(prefs.theme); }, [prefs]);

  return (
    <div className="flex flex-col gap-8">
      <div>
        <h3 className="text-xl font-bold text-on-background mb-1">Giao diện</h3>
        <p className="text-sm text-on-surface-variant">Tuỳ chỉnh cách hiển thị của ứng dụng.</p>
      </div>
      <SettingRow icon="dark_mode" label="Chế độ tối" desc="Bảo vệ mắt khi dùng ban đêm"
        action={<Toggle value={theme === 'dark'} onChange={v => setTheme(v ? 'dark' : 'light')} />} />
      <SaveButton onClick={() => onSave({ theme })} saving={saving} />
    </div>
  );
}

function PrivacySection() {
  const [pinLock, setPinLock] = useState(false);
  return (
    <div className="flex flex-col gap-8">
      <div>
        <h3 className="text-xl font-bold text-on-background mb-1">Quyền riêng tư</h3>
        <p className="text-sm text-on-surface-variant">Bảo vệ nhật ký của bạn.</p>
      </div>
      <SettingRow icon="pin" label="Khoá bằng mã PIN" desc="Yêu cầu PIN khi mở ứng dụng"
        action={<Toggle value={pinLock} onChange={setPinLock} />} />
      {pinLock && (
        <div className="ml-10">
          <button className="px-5 py-2 bg-surface-container border border-outline-variant/30 rounded-xl text-sm font-medium text-on-surface hover:bg-surface-container-high transition-colors">
            Đặt mã PIN
          </button>
        </div>
      )}
      <div className="pt-2 border-t border-outline-variant/20 flex flex-col gap-4">
        <p className="text-sm font-semibold text-on-surface">Dữ liệu</p>
        <div className="flex flex-col gap-3">
          <button className="flex items-center gap-3 px-5 py-3 rounded-xl border border-outline-variant/30 text-sm text-on-surface hover:bg-surface-container transition-colors">
            <span className="material-symbols-outlined text-primary">download</span>Xuất nhật ký (JSON)
          </button>
          <button className="flex items-center gap-3 px-5 py-3 rounded-xl border border-error/30 text-sm text-error hover:bg-error/5 transition-colors">
            <span className="material-symbols-outlined">delete_forever</span>Xoá toàn bộ dữ liệu
          </button>
        </div>
      </div>
    </div>
  );
}

function JournalSection() {
  const [aiAnalysis, setAiAnalysis] = useState(true);
  const [prompts, setPrompts] = useState(true);
  const [autoSave, setAutoSave] = useState(true);
  return (
    <div className="flex flex-col gap-8">
      <div>
        <h3 className="text-xl font-bold text-on-background mb-1">Cài đặt nhật ký</h3>
        <p className="text-sm text-on-surface-variant">Tuỳ chỉnh trải nghiệm viết của bạn.</p>
      </div>
      <SettingRow icon="psychology" label="Phân tích cảm xúc AI" desc="Tự động phân tích tâm trạng sau mỗi bài viết"
        action={<Toggle value={aiAnalysis} onChange={setAiAnalysis} />} />
      <SettingRow icon="auto_awesome" label="Gợi ý chủ đề" desc="Hiện câu hỏi gợi ý khi bắt đầu viết"
        action={<Toggle value={prompts} onChange={setPrompts} />} />
      <SettingRow icon="save" label="Tự động lưu" desc="Lưu nháp mỗi 30 giây khi đang viết"
        action={<Toggle value={autoSave} onChange={setAutoSave} />} />
    </div>
  );
}

function AboutSection() {
  const { logout } = useAuth();
  const navigate = useNavigate();
  function handleLogout() { logout(); navigate('/login'); }
  return (
    <div className="flex flex-col gap-8">
      <div>
        <h3 className="text-xl font-bold text-on-background mb-1">Giới thiệu</h3>
        <p className="text-sm text-on-surface-variant">Thông tin về ứng dụng Tâm An.</p>
      </div>
      <div className="flex items-center gap-5 p-6 bg-surface-container-low rounded-2xl border border-outline-variant/20">
        <div className="w-16 h-16 rounded-2xl bg-primary/10 flex items-center justify-center text-primary">
          <span className="material-symbols-outlined text-4xl">spa</span>
        </div>
        <div>
          <h4 className="text-lg font-bold text-on-surface">Tâm An</h4>
          <p className="text-sm text-on-surface-variant">Phiên bản 1.0.0</p>
        </div>
      </div>
      <button onClick={handleLogout} className="flex items-center gap-3 px-5 py-4 rounded-xl border border-error/20 text-error hover:bg-error/5 transition-colors text-sm">
        <span className="material-symbols-outlined">logout</span>Đăng xuất
      </button>
    </div>
  );
}

/* ── Shared UI ── */

function Field({ label, value, onChange, type = 'text', disabled }) {
  return (
    <div className="flex flex-col gap-2">
      <label className="text-xs font-bold uppercase tracking-widest text-on-surface-variant">{label}</label>
      <input
        type={type}
        value={value}
        onChange={onChange ? e => onChange(e.target.value) : undefined}
        disabled={disabled}
        className="bg-surface-container-lowest border border-outline-variant/30 rounded-xl px-4 py-3 text-on-surface text-sm focus:ring-2 focus:ring-primary/20 transition-all disabled:opacity-50"
      />
    </div>
  );
}

function Toggle({ value, onChange }) {
  return (
    <button onClick={() => onChange(!value)}
      className={`relative w-12 h-6 rounded-full transition-colors flex-shrink-0 ${value ? 'bg-primary' : 'bg-surface-container-highest'}`}>
      <span className={`absolute top-0.5 w-5 h-5 rounded-full bg-white shadow-sm transition-all ${value ? 'left-6' : 'left-0.5'}`} />
    </button>
  );
}

function SettingRow({ icon, label, desc, action }) {
  return (
    <div className="flex items-center gap-4">
      <div className="w-10 h-10 rounded-xl bg-surface-container flex items-center justify-center text-on-surface-variant flex-shrink-0">
        <span className="material-symbols-outlined">{icon}</span>
      </div>
      <div className="flex-grow">
        <p className="text-sm font-semibold text-on-surface">{label}</p>
        <p className="text-xs text-on-surface-variant">{desc}</p>
      </div>
      {action}
    </div>
  );
}

function SaveButton({ onClick, saving }) {
  return (
    <button
      onClick={onClick}
      disabled={saving}
      className="self-start px-8 py-3 bg-primary text-on-primary rounded-xl font-medium text-sm hover:opacity-90 disabled:opacity-50 transition-opacity shadow-lg shadow-primary/10 flex items-center gap-2"
    >
      {saving && <span className="material-symbols-outlined animate-spin text-base">progress_activity</span>}
      Lưu thay đổi
    </button>
  );
}

/* ── Main Settings Page ── */

export default function Settings() {
  const [active, setActive] = useState('profile');
  const [mobileShowContent, setMobileShowContent] = useState(false);
  const [profile, setProfile] = useState(null);
  const [prefs, setPrefs] = useState(null);
  const [saving, setSaving] = useState(false);
  const [saveMsg, setSaveMsg] = useState('');

  useEffect(() => {
    client.get('/api/users/me/profile').then(r => setProfile(r.data)).catch(() => {});
    client.get('/api/users/me/preferences').then(r => setPrefs(r.data)).catch(() => {});
  }, []);

  function showSuccess() {
    setSaveMsg('Đã lưu!');
    setTimeout(() => setSaveMsg(''), 2000);
  }

  async function handleSaveProfile(data) {
    setSaving(true);
    try {
      const res = await client.put('/api/users/me/profile', {
        display_name: data.display_name || undefined,
        birth_date: data.birth_date || undefined,
        timezone: data.timezone || undefined,
      });
      setProfile(res.data);
      showSuccess();
    } catch { /* ignore */ }
    finally { setSaving(false); }
  }

  async function handleSavePreferences(data) {
    setSaving(true);
    try {
      const res = await client.put('/api/users/me/preferences', data);
      setPrefs(res.data);
      showSuccess();
    } catch { /* ignore */ }
    finally { setSaving(false); }
  }

  async function handleAvatarUpload(file) {
    if (!file) return;
    const formData = new FormData();
    formData.append('file', file);
    try {
      const res = await client.post('/api/users/me/avatar', formData, { headers: { 'Content-Type': 'multipart/form-data' } });
      setProfile(p => ({ ...p, avatar_url: res.data.avatar_url }));
    } catch { alert('Không thể tải ảnh lên.'); }
  }

  async function handleAvatarDelete() {
    try {
      await client.delete('/api/users/me/avatar');
      setProfile(p => ({ ...p, avatar_url: null }));
    } catch { /* ignore */ }
  }

  function selectSection(id) { setActive(id); setMobileShowContent(true); }

  const activeSection = SECTIONS.find(s => s.id === active);

  const CONTENT_MAP = {
    profile:       <ProfileSection profile={profile} onSave={handleSaveProfile} onAvatarUpload={handleAvatarUpload} onAvatarDelete={handleAvatarDelete} saving={saving} />,
    appearance:    <AppearanceSection prefs={prefs} onSave={handleSavePreferences} saving={saving} />,
    notifications: <NotificationsSection prefs={prefs} onSave={handleSavePreferences} saving={saving} />,
    privacy:       <PrivacySection />,
    journal:       <JournalSection />,
    about:         <AboutSection />,
  };

  return (
    <div className="md:ml-72 min-h-screen flex flex-col pt-16 md:pt-0">
      <div className="px-6 md:px-12 py-6 md:py-8 border-b border-outline-variant/20 flex items-center justify-between">
        <div>
          <span className="text-xs font-bold tracking-[0.2em] text-primary uppercase mb-1 block">Cài đặt</span>
          <h2 className="text-3xl md:text-4xl font-extrabold tracking-tight text-on-background">Settings</h2>
        </div>
        {saveMsg && (
          <div className="flex items-center gap-1.5 text-sm text-primary">
            <span className="material-symbols-outlined text-base">check_circle</span>{saveMsg}
          </div>
        )}
      </div>

      <div className="flex flex-1 overflow-hidden">
        <aside className={`w-full md:w-64 md:flex-shrink-0 flex flex-col gap-1 p-4 border-r border-outline-variant/20 overflow-y-auto ${mobileShowContent ? 'hidden md:flex' : 'flex'}`}>
          {SECTIONS.map(({ id, icon, label }) => (
            <button
              key={id}
              onClick={() => selectSection(id)}
              className={`flex items-center gap-3 px-4 py-3 rounded-xl text-left transition-all ${
                active === id ? 'bg-primary/10 text-primary font-medium' : 'text-on-surface-variant hover:bg-surface-container hover:text-on-surface'
              }`}
            >
              <span className="material-symbols-outlined">{icon}</span>
              <span className="text-sm font-medium">{label}</span>
              <span className="material-symbols-outlined text-base ml-auto md:hidden">chevron_right</span>
            </button>
          ))}
        </aside>

        <main className={`flex-1 overflow-y-auto p-6 md:p-10 ${mobileShowContent ? 'block' : 'hidden md:block'}`}>
          <button onClick={() => setMobileShowContent(false)}
            className="md:hidden flex items-center gap-2 text-on-surface-variant text-sm mb-6 hover:text-primary transition-colors">
            <span className="material-symbols-outlined">arrow_back</span>{activeSection?.label}
          </button>
          {CONTENT_MAP[active]}
        </main>
      </div>
    </div>
  );
}
