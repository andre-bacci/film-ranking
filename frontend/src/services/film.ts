import { get } from "./axios";
import { Film, FilmData } from "models/Film";

export interface FilmSearchParams {
  search: string;
  page?: number;
  length?: number;
}

export class FilmService {

  async search(params: FilmSearchParams): Promise<Film[]> {
    return get("films/search/", {params: params})
      .then(
        (response: FilmData[]) => response.map((data) => new Film(data))
      )
  }
}
