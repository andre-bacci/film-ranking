import { IndividualListCreateData, ListFilmCreateData } from "services/types";
import * as Yup from "yup";

export const ListFilmSchema = Yup.object().shape({
  film_id: Yup.string().required("Required"),
  ranking: Yup.number(),
  comment: Yup.string(),
  grade: Yup.number(),
} as Record<keyof ListFilmCreateData, Yup.AnySchema>);

export const IndividualListSchema = Yup.object().shape({
  compilation_id: Yup.string().required("Required"),
  list_films: Yup.array().of(ListFilmSchema).min(1),
} as Record<keyof IndividualListCreateData, Yup.AnySchema>);
