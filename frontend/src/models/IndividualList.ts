import { ListFilm, ListFilmData } from "./ListFilm";
import { User, UserData } from "./User";

export interface IndividualListData {
  author: UserData;
  list_films: ListFilmData[]
  comment: string;
}

export class IndividualList {
  author: User;
  films: ListFilm[];
  comment: string;

  constructor(data: IndividualListData) {
    this.author = new User(data.author);
    this.films = data.list_films.map((list_film) => new ListFilm(list_film));
    this.comment = data.comment;
  }
}
