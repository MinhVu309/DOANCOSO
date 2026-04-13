import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import Journaling from './pages/Journaling';
import History from './pages/History';
import Trends from './pages/Trends';
import Categories from './pages/Categories';
import Settings from './pages/Settings';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Navigate to="/journaling" replace />} />
          <Route path="journaling" element={<Journaling />} />
          <Route path="history" element={<History />} />
          <Route path="trends" element={<Trends />} />
          <Route path="categories" element={<Categories />} />
          <Route path="settings" element={<Settings />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
