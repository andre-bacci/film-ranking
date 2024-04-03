import { User, UserData } from "./User";

export interface CompilationData {
  owners: UserData[];
  title: string;
}

export class Compilation {
  owners: User[];
  title: string;

  constructor(data: CompilationData) {
    this.owners = data.owners.map((user) => new User(user));
    this.title = data.title;
  }
}
