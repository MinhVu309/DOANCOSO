import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Login() {
  const [tab, setTab] = useState('login'); // 'login' | 'register'
  const [form, setForm] = useState({ email: '', username: '', password: '', display_name: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login, register } = useAuth();
  const navigate = useNavigate();

  function update(field, value) {
    setForm(f => ({ ...f, [field]: value }));
    setError('');
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      if (tab === 'login') {
        await login(form.email, form.password);
      } else {
        if (!form.username) { setError('Username là bắt buộc'); setLoading(false); return; }
        await register(form.email, form.username, form.password, form.display_name);
      }
      navigate('/journaling', { replace: true });
    } catch (err) {
      const msg = err.response?.data?.detail;
      setError(Array.isArray(msg) ? msg[0]?.msg : (msg || 'Có lỗi xảy ra, vui lòng thử lại.'));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-background flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-10">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-primary/10 mb-4">
            <span className="material-symbols-outlined text-primary text-4xl">spa</span>
          </div>
          <h1 className="text-3xl font-bold text-on-background">Tâm An</h1>
          <p className="text-on-surface-variant text-sm mt-1">Nhật ký thông minh</p>
        </div>

        {/* Card */}
        <div className="bg-surface-container-low border border-outline-variant/20 rounded-[2rem] p-8 shadow-sm">
          {/* Tabs */}
          <div className="flex bg-surface-container rounded-xl p-1 mb-8 gap-1">
            {[['login', 'Đăng nhập'], ['register', 'Đăng ký']].map(([id, label]) => (
              <button
                key={id}
                onClick={() => { setTab(id); setError(''); }}
                className={`flex-1 py-2.5 rounded-lg text-sm font-semibold transition-all ${
                  tab === id
                    ? 'bg-surface-container-lowest text-primary shadow-sm'
                    : 'text-on-surface-variant hover:text-on-surface'
                }`}
              >
                {label}
              </button>
            ))}
          </div>

          <form onSubmit={handleSubmit} className="flex flex-col gap-5">
            <Field
              label="Email"
              type="email"
              value={form.email}
              onChange={v => update('email', v)}
              required
            />

            {tab === 'register' && (
              <>
                <Field
                  label="Username"
                  value={form.username}
                  onChange={v => update('username', v)}
                  placeholder="Tối thiểu 3 ký tự"
                  required
                />
                <Field
                  label="Tên hiển thị (tùy chọn)"
                  value={form.display_name}
                  onChange={v => update('display_name', v)}
                  placeholder="Ví dụ: Minh Vũ"
                />
              </>
            )}

            <Field
              label="Mật khẩu"
              type="password"
              value={form.password}
              onChange={v => update('password', v)}
              placeholder={tab === 'register' ? 'Tối thiểu 8 ký tự' : ''}
              required
            />

            {error && (
              <div className="text-sm text-error bg-error/5 border border-error/20 rounded-xl px-4 py-3">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="mt-2 py-4 bg-primary text-on-primary rounded-xl font-semibold text-sm shadow-lg shadow-primary/10 hover:opacity-90 disabled:opacity-50 transition-all flex items-center justify-center gap-2"
            >
              {loading ? (
                <span className="material-symbols-outlined animate-spin text-base">progress_activity</span>
              ) : null}
              {tab === 'login' ? 'Đăng nhập' : 'Tạo tài khoản'}
            </button>
          </form>
        </div>

        {/* Seed hint */}
        <p className="text-center text-xs text-on-surface-variant mt-6 opacity-60">
          Tài khoản test: test@nhatki.app / test123
        </p>
      </div>
    </div>
  );
}

function Field({ label, type = 'text', value, onChange, placeholder, required }) {
  return (
    <div className="flex flex-col gap-2">
      <label className="text-xs font-bold uppercase tracking-widest text-on-surface-variant">{label}</label>
      <input
        type={type}
        value={value}
        onChange={e => onChange(e.target.value)}
        placeholder={placeholder}
        required={required}
        className="bg-surface-container-lowest border border-outline-variant/30 rounded-xl px-4 py-3 text-on-surface text-sm focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all placeholder:text-stone-300"
      />
    </div>
  );
}
