import { Navigate } from "react-router-dom";

const ProtectedRoute = ({ children, role }) => {
  const isLoggedIn = localStorage.getItem("isLoggedIn") === "true";
  const currentRole = localStorage.getItem("role");

  if (!isLoggedIn) return <Navigate to="/login" replace />;
  if (role && currentRole !== role) {
    return <Navigate to={currentRole === "admin" ? "/admin-dashboard" : "/faculty-dashboard"} replace />;
  }
  return children;
};

export default ProtectedRoute;
