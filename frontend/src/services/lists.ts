import { IndividualList, IndividualListData } from "models/IndividualList";
import { get, post } from "./axios";

export class ListService {

  async listIndividualLists(): Promise<IndividualList[]> {
    return get("lists/individual_lists/")
      .then(
        (response: IndividualListData[]) => response.map((list) => new IndividualList(list))
      )
  }
}
