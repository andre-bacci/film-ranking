import "./styles.scss";
import { ListFilmProps } from "./types";

export default function ListFilmComponent({ listFilm }: ListFilmProps) {
  return (
    <div className="list-film-wrapper">
      <div className="list-film-title">
        <p>
          <b>{listFilm.ranking}</b> - {listFilm.title} ({listFilm.releaseYear})
        </p>
      </div>
      <div className="directed-by">Directed by: {listFilm.directedBy}</div>
      <div className="film-comment">Comment: {listFilm.comment}</div>
    </div>
  );
}
