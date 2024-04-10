import { ListIndividualLists } from "pages";
import { Routes, Route } from "react-router-dom";

export default function ListRoutes() {
  return (
    <Routes>
      <Route path="/" element={<ListIndividualLists />} />
      <Route path="/new" element={<ListIndividualLists />} />
    </Routes>
  );
}
