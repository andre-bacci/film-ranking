import { RootState } from "store";
import "./styles.scss";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { setLogout } from "store/features/auth/authSlice";
import { Button } from "components";

export default function Header() {
  const navigate = useNavigate();
  const user = useSelector((state: RootState) => state.auth.user);
  const dispatch = useDispatch();

  return (
    <header className="header">
      <div className="flex items-center">
        <p className="font-bold logo text-xl">Film Ranking Application</p>
        <div className="menus">
          {user ? (
            <>
              <Button styled="text">{user.name}</Button>
              <Button styled="text" onClick={() => navigate("/lists")}>
                Lists
              </Button>
              <Button styled="text" onClick={() => navigate("/compilations")}>
                Compilations
              </Button>
              <Button styled="text" onClick={() => dispatch(setLogout())}>
                Logout
              </Button>
            </>
          ) : (
            <div className="text-lg">
              <Button styled="text" onClick={() => navigate("/login")}>
                Login
              </Button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
