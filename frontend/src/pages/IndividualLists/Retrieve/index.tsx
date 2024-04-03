import { ListService } from "services/lists";
import "./styles.scss";
import { useEffect, useState } from "react";
import { IndividualList } from "models/IndividualList";
import { IndividualListComponent } from "components";

export default function RetrieveList() {
  const listService = new ListService();
  const [lists, setLists] = useState<IndividualList[]>([]);

  useEffect(() => {
    listService.listIndividualLists().then((response) => setLists(response));
  }, []);

  return (
    <>
      <div className="lists">
        {lists.map((list) => (
          <IndividualListComponent list={list} />
        ))}
      </div>
    </>
  );
}
