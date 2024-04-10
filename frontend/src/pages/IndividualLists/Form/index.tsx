import { ListService } from "services/lists";
import "./styles.scss";
import { Button, Input } from "components";
import { IndividualListCreateData } from "services/types";
import * as Yup from "yup";
import { useFormik } from "formik";
import { useNavigate, useParams } from "react-router-dom";
import { useEffect, useMemo, useState } from "react";
import { IndividualList } from "models/IndividualList";

export default function CompilationForm() {
  const listService = new ListService();
  const navigate = useNavigate();

  const { compilationId: listId } = useParams();
  const isEditing = useMemo(() => !!listId, [listId]);
  const [initialIndividualList, setInitialIndividualList] =
    useState<IndividualList>();

  const emptyIndividualList: IndividualListCreateData = {
    list_films: [],
    compilation_id: "",
  };

  const CompilationSchema = Yup.object().shape({
    title: Yup.string().required("Required"),
  });

  const sendIndividualList = async (values: IndividualListCreateData) => {
    if (!isEditing) {
      await listService
        .createIndividualList(values)
        .then(() => navigate("/lists"));
    } else if (listId) {
      await listService
        .updateIndividualList(values, listId)
        .then(() => navigate("/lists"));
    } else return;
  };

  useEffect(() => {
    if (listId)
      listService
        .retrieveIndividualList(listId)
        .then((response) => setInitialIndividualList(response));
  }, [listId]);

  console.log(initialIndividualList);

  const formik = useFormik({
    initialValues: initialIndividualList ?? emptyIndividualList,
    validationSchema: CompilationSchema,
    onSubmit: sendIndividualList,
    enableReinitialize: true,
  });

  return (
    <div className="compilation-form">
      <form onSubmit={formik.handleSubmit}>
        <Input
          name="title"
          label="Title"
          type="text"
          value={formik.values.title}
          onChange={formik.handleChange}
        />
        <Button
          cssClass="create-compilation-button"
          type="submit"
          disabled={!(formik.isValid && formik.dirty)}
        >
          <div>{isEditing ? "Update" : "Create"}</div>
        </Button>
      </form>
    </div>
  );
}
