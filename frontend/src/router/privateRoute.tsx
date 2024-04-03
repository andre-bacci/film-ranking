import { useSelector } from "react-redux";
import { Navigate, Outlet } from "react-router-dom";
import { RootState } from "store";

const PrivateRoute = () => {
  const { user } = useSelector((state: RootState) => state.auth);
  const isLoggedIn = !!user;
  console.log(user);

  return isLoggedIn ? <Outlet /> : <Navigate to="/login" replace />;
};

export default PrivateRoute;
