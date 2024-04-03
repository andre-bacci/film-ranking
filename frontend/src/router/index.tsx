import { useEffect } from "react";
import { Route, Routes, useLocation } from "react-router-dom";

import { Home, Login, Lists } from "pages";
import PrivateRoute from "./privateRoute";

function Routers() {
  const { pathname } = useLocation();

  useEffect(() => {
    setTimeout(() => {
      window.scrollTo({
        top: 0,
        left: 0,
        behavior: "smooth",
      });
    }, 100);
  }, [pathname]);

  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="" element={<PrivateRoute />}>
        <Route path="/lists" element={<Lists />} />
      </Route>
    </Routes>
  );
}

export default Routers;
