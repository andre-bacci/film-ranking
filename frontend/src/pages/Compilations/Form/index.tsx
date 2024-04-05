import { ListService } from "services/lists";
import "./styles.scss";
import { Button, Input } from "components";
import { CompilationFormProps } from "./types";
import { CompilationCreateData } from "services/types";
import * as Yup from "yup";
import { useFormik } from "formik";

export default function CompilationForm({ isEditing }: CompilationFormProps) {
  const listService = new ListService();

  const initialValues: CompilationCreateData = {
    title: "",
  };

  const CompilationSchema = Yup.object().shape({
    title: Yup.string().required("Required"),
  });

  const sendCompilation = async (values: CompilationCreateData) => {
    await listService.createCompilation(values);
  };

  const formik = useFormik({
    initialValues,
    validationSchema: CompilationSchema,
    onSubmit: sendCompilation,
  });

  return (
    <div className="compilations">
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
