import "./styles.scss";
import { IndividualListProps } from "./types";
import ListFilmComponent from "components/ListFilm";

export default function IndividualListComponent({ list }: IndividualListProps) {
  return (
    <div className="individual-list-wrapper">
      <div>Compilation: {list.compilation.title}</div>
      <div>Comment: {list.comment}</div>
      {list.films.map((film) => (
        <ListFilmComponent listFilm={film}></ListFilmComponent>
      ))}
    </div>
  );
}
