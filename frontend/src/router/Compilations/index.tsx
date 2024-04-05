import { CompilationForm, ListCompilations } from "pages";
import { Routes, Route } from "react-router-dom";

export default function CompilationRoutes() {
  return (
    <Routes>
      <Route path="/" element={<ListCompilations />} />
      <Route path="/new" element={<CompilationForm isEditing={false} />} />
    </Routes>
  );
}
