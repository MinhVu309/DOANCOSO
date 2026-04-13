import { NavLink } from 'react-router-dom';

const navItems = [
  { to: '/journaling', icon: 'edit_note', label: 'Journaling' },
  { to: '/history', icon: 'history', label: 'History' },
  { to: '/trends', icon: 'insights', label: 'Trends' },
  { to: '/categories', icon: 'grid_view', label: 'Categories' },
];

export default function Sidebar() {
  return (
    <aside className="fixed left-0 top-0 h-full hidden md:flex flex-col p-6 gap-8 z-40 bg-surface-container-low/80 backdrop-blur-lg w-72 rounded-r-[2.5rem] border-r border-outline-variant/30">
      {/* Logo & User */}
      <div className="flex items-center gap-4 px-2">
        <div className="w-10 h-10 rounded-xl overflow-hidden">
          <img
            alt="User profile"
            className="w-full h-full object-cover"
            src="https://lh3.googleusercontent.com/aida-public/AB6AXuDmY5oIBZgF4FVvkeIODuj3VqAtvWkCSeDIguGXs45Y0T5z_x7SRl0QeAzMD1RwO4ybplKnndqJWJWIVA2ijUjhvMKREHcGYLEiZLelM512Ym7qb9CNOoxYkYF6gg3fBqd4mRowxO4GTNs5IutTfsPL7zxFO9sDxUDU_CcBjjWy7IUTxe1MQ9KtyvAJlK7fBbRK6tRtA1e7VRviNGa-hKwm4avmZPS6uYh08O1eDvOfYaL7epiMqIswXzrUhRemdkeI5se25kweC0s"
          />
        </div>
        <div>
          <h1 className="text-xl font-bold tracking-tight text-on-surface">Tâm An</h1>
          <p className="text-xs text-on-surface-variant font-medium">The Digital Sanctuary</p>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex flex-col gap-2 flex-grow">
        {navItems.map(({ to, icon, label }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `flex items-center gap-4 px-4 py-3 transition-all duration-300 ease-out ${
                isActive
                  ? 'bg-primary/10 text-primary rounded-xl font-medium'
                  : 'text-on-surface-variant hover:text-primary hover:translate-x-1'
              }`
            }
          >
            <span className="material-symbols-outlined">{icon}</span>
            <span className="font-medium">{label}</span>
          </NavLink>
        ))}
      </nav>

      {/* Settings & Support */}
      <div className="flex flex-col gap-2 pt-6 border-t border-outline-variant/30">
        <NavLink
          to="/settings"
          className={({ isActive }) =>
            `flex items-center gap-4 px-4 py-2 transition-all duration-300 ease-out ${
              isActive ? 'text-primary font-medium' : 'text-on-surface-variant hover:text-primary hover:translate-x-1'
            }`
          }
        >
          <span className="material-symbols-outlined">settings</span>
          <span className="text-sm">Settings</span>
        </NavLink>
        <button className="flex items-center gap-4 px-4 py-2 text-on-surface-variant hover:text-primary hover:translate-x-1 transition-all duration-300 ease-out">
          <span className="material-symbols-outlined">help_outline</span>
          <span className="text-sm">Support</span>
        </button>
      </div>

      <button className="w-full py-4 bg-primary text-on-primary rounded-2xl font-medium text-sm flex items-center justify-center gap-2 shadow-lg shadow-primary/10 hover:opacity-90 transition-opacity">
        <span className="material-symbols-outlined" style={{ fontSize: '20px' }}>add</span>
        New Entry
      </button>
    </aside>
  );
}
