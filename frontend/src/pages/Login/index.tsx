import { useNavigate } from "react-router-dom";
import "./styles.scss";
import { Button, Input } from "components";
import { LoginProps } from "./types";
import { useDispatch, useSelector } from "react-redux";
import { RootState } from "store";
import * as Yup from "yup";
import { useEffect } from "react";
import {
  setAccessToken,
  setLoggedIn,
  setRefreshToken,
} from "store/features/auth/authSlice";
import { useFormik } from "formik";
import { AuthService } from "services/auth";
import { User } from "models/User";

export default function Login() {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { user } = useSelector((state: RootState) => state.auth);
  const authService = new AuthService();

  const initialValues: LoginProps = {
    email: "",
    password: "",
  };

  const LoginSchema = Yup.object().shape({
    email: Yup.string().required("Required"),
    password: Yup.string().required("Required"),
  });

  const login = async (values: LoginProps) => {
    const tokens = await authService.login(values);
    if (!tokens) return;
    dispatch(setAccessToken(tokens.access));
    dispatch(setRefreshToken(tokens.refresh));
    const loggedUser = await authService.retrieveLogged();
    if (loggedUser && tokens) dispatch(setLoggedIn(new User(loggedUser)));
  };

  useEffect(() => {
    if (user) navigate("/lists");
  }, [user, navigate]);

  const formik = useFormik({
    initialValues,
    validationSchema: LoginSchema,
    onSubmit: login,
  });

  return (
    <div className="login-box">
      <form onSubmit={formik.handleSubmit}>
        <div className="login-wrapper">
          <Input
            name="email"
            label="Email"
            type="text"
            value={formik.values.email}
            onChange={formik.handleChange}
          />
          <Input
            name="password"
            label="Password"
            type="password"
            value={formik.values.password}
            onChange={formik.handleChange}
          />
          <Button
            cssClass="login-button"
            type="submit"
            disabled={!(formik.isValid && formik.dirty)}
          >
            <div>Log In</div>
          </Button>
        </div>
      </form>
    </div>
  );
}
