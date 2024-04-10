import "./styles.scss";
import { IndividualListProps } from "./types";
import ListFilmComponent from "components/ListFilm";

export default function IndividualListComponent({
  list,
  isDetail = false,
}: IndividualListProps) {
  return (
    <div className="individual-list-wrapper">
      <div>Compilation: {list.compilation.title}</div>
      <div>Comment: {list.comment}</div>
      {isDetail ? (
        list.films.map((film) => (
          <ListFilmComponent listFilm={film}></ListFilmComponent>
        ))
      ) : (
        <div>{list.films.length} films</div>
      )}
    </div>
  );
}
