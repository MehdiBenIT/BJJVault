import { Navigate, Route, Routes, Link } from "react-router-dom";

import { AuthProvider, useAuth } from "./context/AuthContext";
import AuthCallback from "./pages/AuthCallback";
import CompetitionJournal from "./pages/CompetitionJournal";
import Login from "./pages/Login";
import Profile from "./pages/Profile";
import TrainingJournal from "./pages/TrainingJournal";

function RequireAuth({ children }: { children: JSX.Element }) {
  const { user, loading } = useAuth();
  if (loading) return <div className="page">Loading...</div>;
  if (!user) return <Navigate to="/login" replace />;
  return children;
}

function Nav() {
  const { user, logout } = useAuth();
  if (!user) return null;
  return (
    <nav className="nav">
      <Link to="/profile">Profile</Link>
      <Link to="/training">Training Journal</Link>
      <Link to="/competitions">Competition Journal</Link>
      <span className="nav-spacer" />
      <span>{user.display_name}</span>
      <button onClick={logout}>Log out</button>
    </nav>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <Nav />
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/auth/callback" element={<AuthCallback />} />
        <Route
          path="/profile"
          element={
            <RequireAuth>
              <Profile />
            </RequireAuth>
          }
        />
        <Route
          path="/training"
          element={
            <RequireAuth>
              <TrainingJournal />
            </RequireAuth>
          }
        />
        <Route
          path="/competitions"
          element={
            <RequireAuth>
              <CompetitionJournal />
            </RequireAuth>
          }
        />
        <Route path="*" element={<Navigate to="/profile" replace />} />
      </Routes>
    </AuthProvider>
  );
}
