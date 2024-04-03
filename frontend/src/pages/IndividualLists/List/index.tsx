import { ListService } from "services/lists";
import "./styles.scss";
import { useEffect, useState } from "react";

export default function ListIndividualLists() {
  const listService = new ListService();
  const [lists, setLists] = useState([]);

  useEffect(() => {
    listService.listIndividualLists().then((response) => setLists(response));
  }, []);

  return (
    <>
      <div className="lists">{JSON.stringify(lists)}</div>
    </>
  );
}
