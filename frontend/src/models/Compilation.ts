import { User, UserData } from "./User";

export interface CompilationData {
  id: string;
  owners: UserData[];
  title: string;
}

export class Compilation {
  id: string;
  owners: User[];
  title: string;

  constructor(data: CompilationData) {
    this.id = data.id;
    this.owners = data.owners.map((user) => new User(user));
    this.title = data.title;
  }
}
