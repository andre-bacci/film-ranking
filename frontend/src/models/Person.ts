export interface PersonData {
  imdb_id: string;
  tmdb_id: string;
  name: string;
}

export class Person {
  tmdbId: string;
  imdbId: string;
  name: string;

  constructor(data: PersonData) {
    this.tmdbId = data.tmdb_id;
    this.imdbId = data.imdb_id;
    this.name = data.name;
  }
}
