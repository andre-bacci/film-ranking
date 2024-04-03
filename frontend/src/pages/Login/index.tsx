import { useNavigate } from "react-router-dom";
import "./styles.scss";
import { Button, Input } from "components";
import { LoginProps } from "./types";
import { useDispatch, useSelector } from "react-redux";
import { RootState } from "store";
import * as Yup from "yup";
import { useEffect } from "react";
import { setLoggedIn } from "store/features/auth/authSlice";
import { useFormik } from "formik";
import { AuthService } from "services/auth";

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
    email: Yup.string().required("Campo obrigatório"),
    password: Yup.string().required("Campo obrigatório"),
  });

  const login = async (values: LoginProps) => {
    await authService.login(values);
    const loggedUser = await authService.retrieveLogged();
    console.log(loggedUser);
    if (loggedUser)
      dispatch(
        setLoggedIn({
          user: {
            id: loggedUser.id,
            email: loggedUser.email,
            isActive: true,
            name: loggedUser.full_name,
          },
        })
      );
  };

  useEffect(() => {
    if (user) navigate("/");
  });

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
