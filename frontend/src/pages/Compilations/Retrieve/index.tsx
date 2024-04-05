import { ListService } from "services/lists";
import "./styles.scss";
import { useEffect, useState } from "react";
import { Compilation } from "models/Compilation";
import { Button, CompilationComponent } from "components";
import { useNavigate, useParams } from "react-router-dom";

export default function RetrieveCompilation() {
  const navigate = useNavigate();
  const listService = new ListService();
  const [compilation, setCompilation] = useState<Compilation>();
  const { compilationId } = useParams();

  useEffect(() => {
    if (!compilationId) return;
    listService
      .retrieveCompilation(compilationId)
      .then((response) => setCompilation(response));
  }, []);

  const deleteCompilation = async (compilationId: string) => {
    await listService.deleteCompilation(compilationId);
    navigate("/compilations");
  };

  return (
    <>
      <div className="compilation-detail">
        {compilation && <CompilationComponent compilation={compilation} />}
        <div className="button-wrapper">
          <Button cssClass="add-button" onClick={() => navigate("edit")}>
            Edit
          </Button>
          {compilation && (
            <Button
              cssClass="delete-button"
              onClick={() => deleteCompilation(compilation.id)}
            >
              Delete
            </Button>
          )}
        </div>
      </div>
    </>
  );
}
