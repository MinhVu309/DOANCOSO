import { useState } from 'react';
import { NavLink, Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';

const navItems = [
  { to: '/journaling', icon: 'edit_note', label: 'Journaling' },
  { to: '/history', icon: 'history', label: 'History' },
  { to: '/trends', icon: 'insights', label: 'Trends' },
  { to: '/categories', icon: 'grid_view', label: 'Categories' },
  { to: '/settings', icon: 'settings', label: 'Settings' },
];

export default function Layout() {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <div className="bg-background text-on-background min-h-screen">
      {/* ===== MOBILE HEADER ===== */}
      <header className="fixed top-0 left-0 right-0 z-50 md:hidden">
        <div className="flex justify-between items-center px-6 py-4 bg-background/90 backdrop-blur-xl border-b border-surface-variant">
          <span className="text-2xl font-semibold text-primary">Tâm An</span>
          <div className="flex items-center gap-3">
            <span className="material-symbols-outlined text-on-surface-variant">local_fire_department</span>
            <button
              onClick={() => setMenuOpen(prev => !prev)}
              className="w-10 h-10 flex items-center justify-center rounded-xl hover:bg-surface-container transition-colors text-on-surface-variant"
              aria-label="Toggle menu"
            >
              <span className="material-symbols-outlined">
                {menuOpen ? 'close' : 'menu'}
              </span>
            </button>
          </div>
        </div>

        {/* Dropdown Menu */}
        {menuOpen && (
          <div className="bg-background/95 backdrop-blur-xl border-b border-surface-variant shadow-xl shadow-black/5">
            <nav className="px-4 py-3 flex flex-col gap-1">
              {navItems.map(({ to, icon, label }) => (
                <NavLink
                  key={to}
                  to={to}
                  onClick={() => setMenuOpen(false)}
                  className={({ isActive }) =>
                    `flex items-center gap-4 px-4 py-3 rounded-xl transition-all ${
                      isActive
                        ? 'bg-primary/10 text-primary font-medium'
                        : 'text-on-surface-variant hover:bg-surface-container hover:text-on-surface'
                    }`
                  }
                >
                  <span className="material-symbols-outlined">{icon}</span>
                  <span className="font-medium">{label}</span>
                </NavLink>
              ))}
            </nav>
            <div className="px-8 pb-5 pt-2 border-t border-surface-variant/50">
              <button className="w-full py-3 bg-primary text-on-primary rounded-xl font-medium text-sm flex items-center justify-center gap-2">
                <span className="material-symbols-outlined" style={{ fontSize: '18px' }}>add</span>
                New Entry
              </button>
            </div>
          </div>
        )}
      </header>

      {/* Overlay to close menu when clicking outside */}
      {menuOpen && (
        <div
          className="fixed inset-0 z-40 md:hidden"
          onClick={() => setMenuOpen(false)}
        />
      )}

      {/* Desktop Sidebar */}
      <Sidebar />

      <Outlet />
    </div>
  );
}
