import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import apiClient from '../../api/client';

function StatCard({ icon, label, value, sub }) {
  return (
    <div className="bg-surface-container rounded-2xl p-5 flex items-center gap-4">
      <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center flex-shrink-0">
        <span className="material-symbols-outlined text-primary">{icon}</span>
      </div>
      <div>
        <p className="text-2xl font-bold text-on-surface">{value ?? '—'}</p>
        <p className="text-sm text-on-surface-variant">{label}</p>
        {sub != null && (
          <p className="text-xs text-primary mt-0.5">+{sub} tuần này</p>
        )}
      </div>
    </div>
  );
}

export default function AdminDashboard() {
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);
  const [users, setUsers] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const [searchInput, setSearchInput] = useState('');
  const [loadingStats, setLoadingStats] = useState(true);
  const [loadingUsers, setLoadingUsers] = useState(true);
  const [togglingId, setTogglingId] = useState(null);

  const LIMIT = 10;

  useEffect(() => {
    apiClient.get('/api/admin/stats')
      .then(r => setStats(r.data))
      .catch(() => {})
      .finally(() => setLoadingStats(false));
  }, []);

  const fetchUsers = useCallback(() => {
    setLoadingUsers(true);
    const params = { page, limit: LIMIT };
    if (search) params.search = search;
    apiClient.get('/api/admin/users', { params })
      .then(r => {
        setUsers(r.data.users);
        setTotal(r.data.total);
      })
      .catch(() => {})
      .finally(() => setLoadingUsers(false));
  }, [page, search]);

  useEffect(() => { fetchUsers(); }, [fetchUsers]);

  function handleSearch(e) {
    e.preventDefault();
    setPage(1);
    setSearch(searchInput);
  }

  async function handleToggle(userId) {
    setTogglingId(userId);
    try {
      const r = await apiClient.patch(`/api/admin/users/${userId}/toggle-active`);
      setUsers(prev => prev.map(u => u.id === userId ? { ...u, is_active: r.data.is_active } : u));
    } catch {}
    setTogglingId(null);
  }

  const totalPages = Math.ceil(total / LIMIT);

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="sticky top-0 z-10 bg-surface-container-low/80 backdrop-blur-lg border-b border-outline-variant/30 px-6 py-4 flex items-center gap-4">
        <button
          onClick={() => navigate(-1)}
          className="p-2 rounded-xl text-on-surface-variant hover:text-primary hover:bg-primary/10 transition-all"
        >
          <span className="material-symbols-outlined">arrow_back</span>
        </button>
        <div className="flex items-center gap-3">
          <span className="material-symbols-outlined text-primary">admin_panel_settings</span>
          <h1 className="text-xl font-bold text-on-surface">Admin Dashboard</h1>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-6 py-8 space-y-10">
        {/* Thống kê hệ thống */}
        <section>
          <h2 className="text-base font-semibold text-on-surface-variant mb-4 flex items-center gap-2">
            <span className="material-symbols-outlined text-[18px]">bar_chart</span>
            Thống kê hệ thống
          </h2>
          {loadingStats ? (
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              {[...Array(6)].map((_, i) => (
                <div key={i} className="bg-surface-container rounded-2xl p-5 h-24 animate-pulse" />
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              <StatCard icon="group" label="Tổng người dùng" value={stats?.total_users} sub={stats?.new_users_this_week} />
              <StatCard icon="check_circle" label="Đang hoạt động" value={stats?.active_users} />
              <StatCard icon="book_2" label="Tổng nhật ký" value={stats?.total_entries} sub={stats?.new_entries_this_week} />
              <StatCard icon="psychology" label="Tổng phân tích AI" value={stats?.total_analyses} />
              <StatCard icon="person_add" label="User mới tuần này" value={stats?.new_users_this_week} />
              <StatCard icon="edit_note" label="Nhật ký mới tuần này" value={stats?.new_entries_this_week} />
            </div>
          )}
        </section>

        {/* Quản lý người dùng */}
        <section>
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-4">
            <h2 className="text-base font-semibold text-on-surface-variant flex items-center gap-2">
              <span className="material-symbols-outlined text-[18px]">manage_accounts</span>
              Quản lý người dùng
              <span className="text-xs bg-primary/10 text-primary px-2 py-0.5 rounded-full font-medium">{total}</span>
            </h2>
            <form onSubmit={handleSearch} className="flex gap-2">
              <input
                type="text"
                value={searchInput}
                onChange={e => setSearchInput(e.target.value)}
                placeholder="Tìm email hoặc username..."
                className="px-4 py-2 rounded-xl bg-surface-container border border-outline-variant/50 text-sm text-on-surface outline-none focus:border-primary/60 transition-colors w-56"
              />
              <button
                type="submit"
                className="px-4 py-2 bg-primary text-on-primary rounded-xl text-sm font-medium hover:opacity-90 transition-opacity"
              >
                Tìm
              </button>
              {search && (
                <button
                  type="button"
                  onClick={() => { setSearchInput(''); setSearch(''); setPage(1); }}
                  className="px-3 py-2 rounded-xl text-on-surface-variant hover:bg-surface-container transition-colors text-sm"
                >
                  Xóa
                </button>
              )}
            </form>
          </div>

          <div className="bg-surface-container rounded-2xl overflow-hidden">
            {loadingUsers ? (
              <div className="p-8 text-center text-on-surface-variant">
                <span className="material-symbols-outlined text-3xl animate-spin">progress_activity</span>
              </div>
            ) : users.length === 0 ? (
              <div className="p-8 text-center text-on-surface-variant text-sm">Không tìm thấy người dùng</div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-outline-variant/30">
                      <th className="text-left px-5 py-3 text-on-surface-variant font-medium">Người dùng</th>
                      <th className="text-left px-5 py-3 text-on-surface-variant font-medium hidden md:table-cell">Email</th>
                      <th className="text-left px-5 py-3 text-on-surface-variant font-medium hidden sm:table-cell">Vai trò</th>
                      <th className="text-left px-5 py-3 text-on-surface-variant font-medium">Trạng thái</th>
                      <th className="text-left px-5 py-3 text-on-surface-variant font-medium hidden lg:table-cell">Nhật ký</th>
                      <th className="text-left px-5 py-3 text-on-surface-variant font-medium hidden lg:table-cell">Tham gia</th>
                      <th className="px-5 py-3"></th>
                    </tr>
                  </thead>
                  <tbody>
                    {users.map(u => (
                      <tr key={u.id} className="border-b border-outline-variant/20 hover:bg-surface-container-high/50 transition-colors">
                        <td className="px-5 py-3">
                          <div className="flex items-center gap-3">
                            <div className="w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0 text-primary font-semibold text-sm">
                              {(u.display_name || u.username)[0]?.toUpperCase()}
                            </div>
                            <span className="font-medium text-on-surface truncate max-w-[120px]">
                              {u.display_name || u.username}
                            </span>
                          </div>
                        </td>
                        <td className="px-5 py-3 text-on-surface-variant hidden md:table-cell">{u.email}</td>
                        <td className="px-5 py-3 hidden sm:table-cell">
                          <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${
                            u.role === 'admin'
                              ? 'bg-primary/15 text-primary'
                              : 'bg-surface-container-high text-on-surface-variant'
                          }`}>
                            {u.role === 'admin' ? 'Admin' : 'User'}
                          </span>
                        </td>
                        <td className="px-5 py-3">
                          <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${
                            u.is_active
                              ? 'bg-green-100 text-green-700'
                              : 'bg-red-100 text-red-600'
                          }`}>
                            {u.is_active ? 'Hoạt động' : 'Vô hiệu'}
                          </span>
                        </td>
                        <td className="px-5 py-3 text-on-surface-variant hidden lg:table-cell">{u.entry_count}</td>
                        <td className="px-5 py-3 text-on-surface-variant hidden lg:table-cell">
                          {new Date(u.created_at).toLocaleDateString('vi-VN')}
                        </td>
                        <td className="px-5 py-3">
                          <button
                            disabled={togglingId === u.id}
                            onClick={() => handleToggle(u.id)}
                            className={`px-3 py-1.5 rounded-xl text-xs font-medium transition-all ${
                              u.is_active
                                ? 'bg-error/10 text-error hover:bg-error/20'
                                : 'bg-primary/10 text-primary hover:bg-primary/20'
                            } disabled:opacity-50`}
                          >
                            {togglingId === u.id
                              ? '...'
                              : u.is_active ? 'Vô hiệu hóa' : 'Kích hoạt'}
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}

            {/* Phân trang */}
            {totalPages > 1 && (
              <div className="flex items-center justify-between px-5 py-3 border-t border-outline-variant/30">
                <span className="text-sm text-on-surface-variant">
                  Trang {page}/{totalPages} · {total} người dùng
                </span>
                <div className="flex gap-2">
                  <button
                    disabled={page <= 1}
                    onClick={() => setPage(p => p - 1)}
                    className="px-3 py-1.5 rounded-xl text-sm text-on-surface-variant hover:bg-surface-container-high disabled:opacity-40 transition-colors"
                  >
                    Trước
                  </button>
                  <button
                    disabled={page >= totalPages}
                    onClick={() => setPage(p => p + 1)}
                    className="px-3 py-1.5 rounded-xl text-sm text-on-surface-variant hover:bg-surface-container-high disabled:opacity-40 transition-colors"
                  >
                    Tiếp
                  </button>
                </div>
              </div>
            )}
          </div>
        </section>
      </div>
    </div>
  );
}
