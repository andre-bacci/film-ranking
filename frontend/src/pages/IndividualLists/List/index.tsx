import { ListService } from "services/lists";
import "./styles.scss";
import { useEffect, useState } from "react";
import { IndividualList } from "models/IndividualList";
import { Button, IndividualListComponent } from "components";
import { useNavigate } from "react-router-dom";

export default function ListIndividualLists() {
  const listService = new ListService();
  const [lists, setLists] = useState<IndividualList[]>([]);
  const navigate = useNavigate();

  useEffect(() => {
    listService.listIndividualLists().then((response) => setLists(response));
  }, []);

  return (
    <>
      <div className="lists">
        <div>Lists</div>
        {lists.map((list) => (
          <IndividualListComponent list={list} />
        ))}
        <div className="add-compilation">
          <Button cssClass="add-button" onClick={() => navigate("new")}>
            New List
          </Button>
        </div>
      </div>
    </>
  );
}
