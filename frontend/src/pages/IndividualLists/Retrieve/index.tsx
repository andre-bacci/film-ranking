import { ListService } from "services/lists";
import "./styles.scss";
import { useEffect, useState } from "react";
import { IndividualList } from "models/IndividualList";
import { IndividualListComponent } from "components";
import { useParams } from "react-router-dom";

export default function RetrieveIndividualList() {
  const listService = new ListService();
  const [list, setList] = useState<IndividualList>();
  const { listId } = useParams();

  useEffect(() => {
    if (!listId) return;
    listService
      .retrieveIndividualList(listId)
      .then((response) => setList(response));
  }, []);

  return (
    <>
      <div className="lists">
        {list && <IndividualListComponent list={list} />}
      </div>
    </>
  );
}
