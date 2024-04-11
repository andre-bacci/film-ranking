import { PersonData } from "./Person";

export interface FilmData {
  tmdb_id: string;
  imdb_id: string;
  title: string;
  original_title: string;
  pt_br_title: string;
  release_date: Date;
  runtime: number;
  synopsis: string;
  poster_path: string;
  directed_by: PersonData[];
  written_by: PersonData[];
  starring: PersonData[];
  release_year: number;
}

export class Film {
  tmdbId: string;
  imdbId: string;
  title: string;
  originalTitle: string;
  ptBrTitle: string;
  releaseDate: Date;
  runtime: number;
  synopsis: string;
  posterPath: string;
  directedBy: PersonData[];
  writtenBy: PersonData[];
  starring: PersonData[];
  releaseYear: number;

  constructor(data: FilmData) {
    this.tmdbId = data.tmdb_id;
    this.imdbId = data.imdb_id;
    this.title = data.title;
    this.originalTitle = data.original_title;
    this.ptBrTitle = data.pt_br_title;
    this.releaseDate = data.release_date;
    this.runtime = data.runtime;
    this.synopsis = data.synopsis;
    this.posterPath = data.poster_path;
    this.directedBy = data.directed_by;
    this.writtenBy = data.written_by;
    this.starring = data.starring;
    this.releaseYear = data.release_year;
  }
}
