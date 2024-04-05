import { ListService } from "services/lists";
import "./styles.scss";
import { Button, Input } from "components";
import { CompilationCreateData } from "services/types";
import * as Yup from "yup";
import { useFormik } from "formik";
import { useParams } from "react-router-dom";
import { useEffect, useMemo, useState } from "react";
import { Compilation } from "models/Compilation";

export default function CompilationForm() {
  const listService = new ListService();

  const { compilationId } = useParams();
  const isEditing = useMemo(() => !!compilationId, [compilationId]);
  const [compilation, setCompilation] = useState<Compilation>();

  const initialValues: CompilationCreateData = {
    title: "",
  };

  const CompilationSchema = Yup.object().shape({
    title: Yup.string().required("Required"),
  });

  const sendCompilation = async (values: CompilationCreateData) => {
    if (!isEditing) {
      await listService.createCompilation(values);
    } else if (compilationId) {
      await listService.updateCompilation(values, compilationId);
    }
  };

  useEffect(() => {
    if (compilationId)
      listService
        .retrieveCompilation(compilationId)
        .then((response) => setCompilation(response));
  }, [compilationId]);

  console.log(compilation);

  const formik = useFormik({
    initialValues: compilation ?? initialValues,
    validationSchema: CompilationSchema,
    onSubmit: sendCompilation,
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
