import { ListIndividualLists } from "pages";
import IndividualListForm from "pages/IndividualLists/Form";
import { Routes, Route } from "react-router-dom";

export default function ListRoutes() {
  return (
    <Routes>
      <Route path="/" element={<ListIndividualLists />} />
      <Route path="/:compilationId/new" element={<IndividualListForm />} />
      <Route path="/:compilationId/:listId" element={<IndividualListForm />} />
    </Routes>
  );
}
