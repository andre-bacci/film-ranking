import { get, post } from "./axios";

export class ListService {

  async listIndividualLists(): Promise<any> {
    return get("lists/individual_lists/")
  }
}
