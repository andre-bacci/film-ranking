import { ListService } from "services/lists";
import "./styles.scss";
import { IndividualListCreateData } from "services/types";
import { useFormik } from "formik";
import { useNavigate, useParams } from "react-router-dom";
import { useEffect, useMemo, useState } from "react";
import { IndividualListSchema } from "./validation";

export default function IndividualListForm() {
  const listService = new ListService();
  const navigate = useNavigate();

  const { listId, compilationId } = useParams();
  // const isEditing = useMemo(() => !!listId, [listId]);
  const [initialIndividualList, setInitialIndividualList] =
    useState<IndividualListCreateData>();

  const emptyIndividualList: IndividualListCreateData = {
    list_films: [],
    compilation_id: compilationId || "",
  };

  const sendIndividualList = async (values: IndividualListCreateData) => {
    if (!listId) {
      await listService
        .createIndividualList(values)
        .then(() => navigate("/lists"));
    } else {
      await listService
        .updateIndividualList(values, listId)
        .then(() => navigate("/lists"));
    }
  };

  useEffect(() => {
    if (listId)
      listService
        .retrieveIndividualList(listId)
        .then((response) =>
          setInitialIndividualList(response.convertToCreateData())
        );
  }, [listId]);

  const formik = useFormik({
    initialValues: initialIndividualList ?? emptyIndividualList,
    validationSchema: IndividualListSchema,
    onSubmit: sendIndividualList,
    enableReinitialize: true,
  });

  return (
    <div className="individual-list-form">
      <form onSubmit={formik.handleSubmit}>
        <div></div>
      </form>
    </div>
  );
}
