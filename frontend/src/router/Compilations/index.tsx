import { CompilationForm, ListCompilations, RetrieveCompilation } from "pages";
import { Routes, Route } from "react-router-dom";

export default function CompilationRoutes() {
  return (
    <Routes>
      <Route path="/" element={<ListCompilations />} />
      <Route path="/new" element={<CompilationForm />} />
      <Route path="/:compilationId" element={<RetrieveCompilation />} />
      <Route path="/:compilationId/edit" element={<CompilationForm />} />
    </Routes>
  );
}
