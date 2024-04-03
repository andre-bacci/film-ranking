import { ListCompilations } from "pages";
import { Routes, Route } from "react-router-dom";

export default function CompilationRoutes() {
  return (
    <Routes>
      <Route path="/" element={<ListCompilations />} />
    </Routes>
  );
}
