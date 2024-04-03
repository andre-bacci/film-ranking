import { User, UserData } from "./User";

export interface IndividualListData {
  author: UserData
}

export class IndividualList {
  author: User

  constructor(data: IndividualListData) {
    this.author = new User(data.author)
  }
}
