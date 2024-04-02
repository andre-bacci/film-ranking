import { RootState } from "store";
import "./styles.scss";
import { useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";

export default function Header() {
  const navigate = useNavigate();
  const user = useSelector((state: RootState) => state.auth.user);

  return (
    <header className="header">
      <div className="flex items-center">
        <p className="font-bold logo">Film Ranking Application</p>
        <div className="menus">
          {user?.id ? (
            <button>{user.name}</button>
          ) : (
            <button onClick={() => navigate("/login")}>Login</button>
          )}
        </div>
      </div>
    </header>
  );
}
