export interface UserData {
  id: number;
  username: string;
  full_name: string;
  email: string;
}

export class User {
  id: number;
  name: string;
  username: string;
  email: string;

  constructor(data: UserData) {
    this.id = data.id
    this.name = data.full_name
    this.email = data.email
    this.username = data.username
  }
}
