export interface ListFilmCreateData {
  film_id: string;
  ranking: number;
  comment: string;
  grade: number;
}

export interface IndividualListCreateData {
  list_films: ListFilmCreateData[];
  compilation_id: string;
}

export interface CompilationCreateData {
  title: string;
}
