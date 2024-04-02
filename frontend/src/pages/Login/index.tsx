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

export default function Login() {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { user } = useSelector((state: RootState) => state.auth);

  const initialValues: LoginProps = {
    email: "",
    password: "",
  };

  const LoginSchema = Yup.object().shape({
    email: Yup.string().required("Campo obrigatório"),
    password: Yup.string().required("Campo obrigatório"),
  });

  const login = (values: LoginProps) => {
    dispatch(
      setLoggedIn({
        user: {
          id: "q",
          email: values.email,
          name: "Nome da silva",
          isActive: true,
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
        <Button cssClass="login-button" type="submit">
          <div>Log In</div>
        </Button>
      </form>
    </div>
  );
}
