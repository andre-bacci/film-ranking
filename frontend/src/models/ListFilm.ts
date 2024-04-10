import { ListFilmCreateData } from "services/types";

export interface ListFilmData {
  film_id: string;
  title: string;
  directed_by: string;
  written_by: string;
  starring: string;
  release_year: number;
  ranking: number;
  grade: number;
  comment: string;
  poster_url: string;
}

export class ListFilm {
  filmId: string;
  title: string;
  directedBy: string;
  writtenBy: string;
  starring: string;
  releaseYear: number;
  ranking: number;
  grade: number;
  comment: string;
  posterUrl: string;

  constructor(data: ListFilmData) {
    this.filmId = data.film_id;
    this.title = data.title;
    this.directedBy = data.directed_by;
    this.writtenBy = data.written_by;
    this.starring = data.starring;
    this.releaseYear = data.release_year;
    this.ranking = data.ranking;
    this.grade = data.grade;
    this.comment = data.comment;
    this.posterUrl = data.poster_url;
  }

  static convertToCreateData(data: ListFilm): ListFilmCreateData {
    return {
      film_id: data.filmId,
      ...data
    }
  }
}
