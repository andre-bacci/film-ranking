import { IndividualList, IndividualListData } from "models/IndividualList";
import { get, post, put } from "./axios";
import { Compilation, CompilationData } from "models/Compilation";
import { CompilationCreateData, IndividualListCreateData } from "./types";

export class ListService {

  async listIndividualLists(): Promise<IndividualList[]> {
    return get("lists/individual_lists/")
      .then(
        (response: IndividualListData[]) => response.map((data) => new IndividualList(data))
      )
  }

  async retrieveIndividualList(listId: string): Promise<IndividualList> {
    return get(`lists/individual_lists/${listId}`)
      .then(
        (response: IndividualListData) =>  new IndividualList(response)
      )
  }

  async createIndividualList(data: IndividualListCreateData): Promise<IndividualList> {
    return post("lists/individual_lists/", data).then(
      (response: IndividualListData) => new IndividualList(response)
    )
  }

  async updateIndividualList(data: IndividualListCreateData, listId: string): Promise<IndividualList> {
    return put(`lists/individual_lists/${listId}/`, data).then(
      (response: IndividualListData) => new IndividualList(response)
    )
  }

  async listCompilations(): Promise<Compilation[]> {
    return get("lists/compilations/")
      .then(
        (response: CompilationData[]) => response.map((data) => new Compilation(data))
      )
  }

  async retrieveCompilation(compilationId: string): Promise<Compilation> {
    return get(`lists/compilations/${compilationId}`)
      .then(
        (response: CompilationData) =>  new Compilation(response)
      )
  }

  async createCompilation(data: CompilationCreateData): Promise<Compilation> {
    return post("lists/compilations/", data).then(
      (response: CompilationData) => new Compilation(response)
    )
  }

  async updateCompilation(data: CompilationCreateData, compilationId: string): Promise<Compilation> {
    return put(`lists/compilations/${compilationId}/`, data).then(
      (response: CompilationData) => new Compilation(response)
    )
  }
}
