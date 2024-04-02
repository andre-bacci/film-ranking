import { RootState } from "store";
import "./styles.scss";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { setLogout } from "store/features/auth/authSlice";

export default function Header() {
  const navigate = useNavigate();
  const user = useSelector((state: RootState) => state.auth.user);
  const dispatch = useDispatch();

  return (
    <header className="header">
      <div className="flex items-center">
        <p className="font-bold logo text-xl">Film Ranking Application</p>
        <div className="menus">
          {user?.id ? (
            <button onClick={() => dispatch(setLogout())}>{user.name}</button>
          ) : (
            <div className="text-lg">
              <button onClick={() => navigate("/login")}>Login</button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
