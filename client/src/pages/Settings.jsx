import { useState } from 'react';

const SECTIONS = [
  { id: 'profile',       icon: 'person',        label: 'Hồ sơ' },
  { id: 'appearance',   icon: 'palette',        label: 'Giao diện' },
  { id: 'notifications',icon: 'notifications',  label: 'Nhắc nhở' },
  { id: 'privacy',      icon: 'lock',           label: 'Quyền riêng tư' },
  { id: 'journal',      icon: 'menu_book',      label: 'Nhật ký' },
  { id: 'about',        icon: 'info',           label: 'Giới thiệu' },
];

/* ── Các mục setting ── */

function ProfileSection() {
  return (
    <div className="flex flex-col gap-8">
      <div>
        <h3 className="text-xl font-bold text-on-background mb-1">Hồ sơ cá nhân</h3>
        <p className="text-sm text-on-surface-variant">Thông tin hiển thị trong ứng dụng của bạn.</p>
      </div>

      {/* Avatar */}
      <div className="flex items-center gap-6">
        <div className="w-20 h-20 rounded-2xl overflow-hidden border-2 border-outline-variant/30 flex-shrink-0">
          <img
            alt="Avatar"
            className="w-full h-full object-cover"
            src="https://lh3.googleusercontent.com/aida-public/AB6AXuDmY5oIBZgF4FVvkeIODuj3VqAtvWkCSeDIguGXs45Y0T5z_x7SRl0QeAzMD1RwO4ybplKnndqJWJWIVA2ijUjhvMKREHcGYLEiZLelM512Ym7qb9CNOoxYkYF6gg3fBqd4mRowxO4GTNs5IutTfsPL7zxFO9sDxUDU_CcBjjWy7IUTxe1MQ9KtyvAJlK7fBbRK6tRtA1e7VRviNGa-hKwm4avmZPS6uYh08O1eDvOfYaL7epiMqIswXzrUhRemdkeI5se25kweC0s"
          />
        </div>
        <div className="flex flex-col gap-2">
          <button className="px-5 py-2 bg-primary text-on-primary rounded-xl text-sm font-medium hover:opacity-90 transition-opacity">
            Đổi ảnh đại diện
          </button>
          <button className="px-5 py-2 text-on-surface-variant text-sm hover:text-error transition-colors">
            Xoá ảnh
          </button>
        </div>
      </div>

      {/* Fields */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Field label="Tên hiển thị" defaultValue="Người dùng" />
        <Field label="Email" defaultValue="user@example.com" type="email" />
        <Field label="Ngày sinh" defaultValue="" type="date" />
        <Field label="Múi giờ" defaultValue="Asia/Ho_Chi_Minh" />
      </div>

      <SaveButton />
    </div>
  );
}

function AppearanceSection() {
  const [fontSize, setFontSize] = useState('medium');
  const [darkMode, setDarkMode] = useState(false);

  return (
    <div className="flex flex-col gap-8">
      <div>
        <h3 className="text-xl font-bold text-on-background mb-1">Giao diện</h3>
        <p className="text-sm text-on-surface-variant">Tuỳ chỉnh cách hiển thị của ứng dụng.</p>
      </div>

      <SettingRow
        icon="dark_mode"
        label="Chế độ tối"
        desc="Bảo vệ mắt khi dùng ban đêm"
        action={<Toggle value={darkMode} onChange={setDarkMode} />}
      />

      <div className="flex flex-col gap-3">
        <label className="text-sm font-semibold text-on-surface">Cỡ chữ</label>
        <div className="flex gap-3">
          {[
            { id: 'small', label: 'Nhỏ' },
            { id: 'medium', label: 'Vừa' },
            { id: 'large', label: 'Lớn' },
          ].map(opt => (
            <button
              key={opt.id}
              onClick={() => setFontSize(opt.id)}
              className={`flex-1 py-3 rounded-xl border text-sm font-medium transition-all ${
                fontSize === opt.id
                  ? 'bg-primary/10 border-primary/30 text-primary'
                  : 'border-outline-variant/30 text-on-surface-variant hover:border-primary/20'
              }`}
            >
              {opt.label}
            </button>
          ))}
        </div>
      </div>

      <div className="flex flex-col gap-3">
        <label className="text-sm font-semibold text-on-surface">Màu chủ đề</label>
        <div className="grid grid-cols-3 gap-3">
          {[
            { name: 'Rừng xanh', primary: '#5b614d', bg: 'bg-[#5b614d]', active: true },
            { name: 'Bình minh', primary: '#7c5c3a', bg: 'bg-[#7c5c3a]', active: false },
            { name: 'Đại dương', primary: '#3a5f7c', bg: 'bg-[#3a5f7c]', active: false },
          ].map(theme => (
            <button
              key={theme.name}
              className={`flex items-center gap-3 p-3 rounded-xl border transition-all ${
                theme.active
                  ? 'border-primary/40 bg-primary/5'
                  : 'border-outline-variant/30 hover:border-primary/20'
              }`}
            >
              <span className={`w-5 h-5 rounded-full ${theme.bg} flex-shrink-0`} />
              <span className="text-sm text-on-surface">{theme.name}</span>
              {theme.active && <span className="material-symbols-outlined text-primary ml-auto text-base">check</span>}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

function NotificationsSection() {
  const [reminder, setReminder] = useState(true);
  const [streak, setStreak] = useState(true);
  const [weekly, setWeekly] = useState(false);

  return (
    <div className="flex flex-col gap-8">
      <div>
        <h3 className="text-xl font-bold text-on-background mb-1">Nhắc nhở</h3>
        <p className="text-sm text-on-surface-variant">Đặt lịch để không bỏ lỡ ngày nào.</p>
      </div>

      <SettingRow
        icon="edit_note"
        label="Nhắc viết nhật ký"
        desc="Nhắc nhở hàng ngày vào giờ cố định"
        action={<Toggle value={reminder} onChange={setReminder} />}
      />

      {reminder && (
        <div className="ml-10 flex flex-col gap-2">
          <label className="text-xs font-bold uppercase tracking-widest text-on-surface-variant">Giờ nhắc</label>
          <input
            type="time"
            defaultValue="21:00"
            className="w-40 bg-surface-container-lowest border border-outline-variant/30 rounded-xl px-4 py-3 text-on-surface text-sm focus:ring-2 focus:ring-primary/20 transition-all"
          />
        </div>
      )}

      <SettingRow
        icon="local_fire_department"
        label="Nhắc duy trì streak"
        desc="Cảnh báo khi sắp mất chuỗi ngày viết"
        action={<Toggle value={streak} onChange={setStreak} />}
      />

      <SettingRow
        icon="insights"
        label="Báo cáo hàng tuần"
        desc="Tóm tắt cảm xúc và xu hướng 7 ngày qua"
        action={<Toggle value={weekly} onChange={setWeekly} />}
      />
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

      <SettingRow
        icon="pin"
        label="Khoá bằng mã PIN"
        desc="Yêu cầu PIN khi mở ứng dụng"
        action={<Toggle value={pinLock} onChange={setPinLock} />}
      />

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
            <span className="material-symbols-outlined text-primary">download</span>
            Xuất nhật ký (JSON)
          </button>
          <button className="flex items-center gap-3 px-5 py-3 rounded-xl border border-outline-variant/30 text-sm text-on-surface hover:bg-surface-container transition-colors">
            <span className="material-symbols-outlined text-primary">picture_as_pdf</span>
            Xuất nhật ký (PDF)
          </button>
          <button className="flex items-center gap-3 px-5 py-3 rounded-xl border border-error/30 text-sm text-error hover:bg-error/5 transition-colors">
            <span className="material-symbols-outlined">delete_forever</span>
            Xoá toàn bộ dữ liệu
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

      <SettingRow
        icon="psychology"
        label="Phân tích cảm xúc AI"
        desc="Tự động phân tích tâm trạng sau mỗi bài viết"
        action={<Toggle value={aiAnalysis} onChange={setAiAnalysis} />}
      />

      <SettingRow
        icon="auto_awesome"
        label="Gợi ý chủ đề"
        desc="Hiện câu hỏi gợi ý khi bắt đầu viết"
        action={<Toggle value={prompts} onChange={setPrompts} />}
      />

      <SettingRow
        icon="save"
        label="Tự động lưu"
        desc="Lưu nháp mỗi 30 giây khi đang viết"
        action={<Toggle value={autoSave} onChange={setAutoSave} />}
      />

      <div className="flex flex-col gap-3">
        <label className="text-sm font-semibold text-on-surface">Tags mặc định</label>
        <p className="text-xs text-on-surface-variant">Tags sẽ tự động xuất hiện khi tạo bài mới.</p>
        <div className="flex flex-wrap gap-2">
          {['Công việc', 'Gia đình', 'Bản thân', 'Sức khoẻ', 'Học tập'].map(tag => (
            <span
              key={tag}
              className="flex items-center gap-1 px-4 py-1.5 bg-surface-container border border-outline-variant/30 rounded-full text-sm text-on-surface"
            >
              {tag}
              <span className="material-symbols-outlined text-on-surface-variant hover:text-error cursor-pointer" style={{ fontSize: '16px' }}>close</span>
            </span>
          ))}
          <button className="px-4 py-1.5 bg-surface-container-high rounded-full text-sm text-primary border border-dashed border-primary/30 hover:bg-primary/5 transition-colors">
            + Thêm tag
          </button>
        </div>
      </div>
    </div>
  );
}

function AboutSection() {
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
          <p className="text-xs text-on-surface-variant mt-1">Nhật ký thông minh — The Digital Sanctuary</p>
        </div>
      </div>

      <div className="flex flex-col gap-3">
        {[
          { icon: 'rate_review', label: 'Gửi phản hồi' },
          { icon: 'star', label: 'Đánh giá ứng dụng' },
          { icon: 'policy', label: 'Chính sách quyền riêng tư' },
          { icon: 'gavel', label: 'Điều khoản sử dụng' },
        ].map(item => (
          <button
            key={item.label}
            className="flex items-center gap-4 px-5 py-4 rounded-xl border border-outline-variant/20 text-on-surface hover:bg-surface-container transition-colors text-sm"
          >
            <span className="material-symbols-outlined text-on-surface-variant">{item.icon}</span>
            {item.label}
            <span className="material-symbols-outlined text-on-surface-variant ml-auto text-base">chevron_right</span>
          </button>
        ))}
      </div>

      <button className="flex items-center gap-3 px-5 py-4 rounded-xl border border-error/20 text-error hover:bg-error/5 transition-colors text-sm">
        <span className="material-symbols-outlined">logout</span>
        Đăng xuất
      </button>
    </div>
  );
}

/* ── Shared UI components ── */

function Field({ label, defaultValue, type = 'text' }) {
  return (
    <div className="flex flex-col gap-2">
      <label className="text-xs font-bold uppercase tracking-widest text-on-surface-variant">{label}</label>
      <input
        type={type}
        defaultValue={defaultValue}
        className="bg-surface-container-lowest border border-outline-variant/30 rounded-xl px-4 py-3 text-on-surface text-sm focus:ring-2 focus:ring-primary/20 transition-all"
      />
    </div>
  );
}

function Toggle({ value, onChange }) {
  return (
    <button
      onClick={() => onChange(!value)}
      className={`relative w-12 h-6 rounded-full transition-colors flex-shrink-0 ${value ? 'bg-primary' : 'bg-surface-container-highest'}`}
    >
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

function SaveButton() {
  return (
    <button className="self-start px-8 py-3 bg-primary text-on-primary rounded-xl font-medium text-sm hover:opacity-90 transition-opacity shadow-lg shadow-primary/10">
      Lưu thay đổi
    </button>
  );
}

const CONTENT_MAP = {
  profile:       <ProfileSection />,
  appearance:    <AppearanceSection />,
  notifications: <NotificationsSection />,
  privacy:       <PrivacySection />,
  journal:       <JournalSection />,
  about:         <AboutSection />,
};

/* ── Main Settings Page ── */

export default function Settings() {
  const [active, setActive] = useState('profile');
  const [mobileShowContent, setMobileShowContent] = useState(false);

  function selectSection(id) {
    setActive(id);
    setMobileShowContent(true);
  }

  const activeSection = SECTIONS.find(s => s.id === active);

  return (
    <div className="md:ml-72 min-h-screen flex flex-col pt-16 md:pt-0">
      {/* Page header */}
      <div className="px-6 md:px-12 py-6 md:py-8 border-b border-outline-variant/20">
        <span className="text-xs font-bold tracking-[0.2em] text-primary uppercase mb-1 block">Cài đặt</span>
        <h2 className="text-3xl md:text-4xl font-extrabold tracking-tight text-on-background">Settings</h2>
      </div>

      <div className="flex flex-1 overflow-hidden">
        {/* ── SUB-SIDEBAR (desktop luôn hiện, mobile chỉ hiện khi chưa chọn) ── */}
        <aside className={`
          w-full md:w-64 md:flex-shrink-0 flex flex-col gap-1 p-4
          border-r border-outline-variant/20 overflow-y-auto
          ${mobileShowContent ? 'hidden md:flex' : 'flex'}
        `}>
          {SECTIONS.map(({ id, icon, label }) => (
            <button
              key={id}
              onClick={() => selectSection(id)}
              className={`flex items-center gap-3 px-4 py-3 rounded-xl text-left transition-all ${
                active === id
                  ? 'bg-primary/10 text-primary font-medium'
                  : 'text-on-surface-variant hover:bg-surface-container hover:text-on-surface'
              }`}
            >
              <span className="material-symbols-outlined">{icon}</span>
              <span className="text-sm font-medium">{label}</span>
              <span className="material-symbols-outlined text-base ml-auto md:hidden">chevron_right</span>
            </button>
          ))}
        </aside>

        {/* ── CONTENT PANEL ── */}
        <main className={`
          flex-1 overflow-y-auto p-6 md:p-10
          ${mobileShowContent ? 'block' : 'hidden md:block'}
        `}>
          {/* Mobile: nút back */}
          <button
            onClick={() => setMobileShowContent(false)}
            className="md:hidden flex items-center gap-2 text-on-surface-variant text-sm mb-6 hover:text-primary transition-colors"
          >
            <span className="material-symbols-outlined">arrow_back</span>
            {activeSection?.label}
          </button>

          {CONTENT_MAP[active]}
        </main>
      </div>
    </div>
  );
}
