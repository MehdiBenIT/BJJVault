import { useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

export default function AuthCallback() {
  const [searchParams] = useSearchParams();
  const { login } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    const token = searchParams.get("token");
    if (!token) {
      navigate("/login");
      return;
    }
    login(token).then(() => navigate("/profile"));
  }, [searchParams, login, navigate]);

  return <div className="page">Signing you in...</div>;
}
