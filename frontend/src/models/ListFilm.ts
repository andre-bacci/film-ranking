export interface ListFilmData {
  title: string;
  directed_by: string;
  written_by: string;
  starring: string;
  release_year: number;
  ranking: number;
  grade: number;
  comment: string;
}

export class ListFilm {
  title: string;
  directedBy: string;
  writtenBy: string;
  starring: string;
  releaseYear: number;
  ranking: number;
  grade: number;
  comment: string;

  constructor(data: ListFilmData) {
    this.title = data.title;
    this.directedBy = data.directed_by;
    this.writtenBy = data.written_by;
    this.starring = data.starring;
    this.releaseYear = data.release_year;
    this.ranking = data.ranking;
    this.grade = data.grade;
    this.comment = data.comment;
  }
}
