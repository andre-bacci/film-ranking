import { ListService } from "services/lists";
import "./styles.scss";
import { useEffect, useState } from "react";
import { Compilation } from "models/Compilation";
import { Button, CompilationComponent } from "components";
import { useNavigate } from "react-router-dom";

export default function ListCompilations() {
  const navigate = useNavigate();
  const listService = new ListService();
  const [compilations, setCompilations] = useState<Compilation[]>([]);

  useEffect(() => {
    listService
      .listCompilations()
      .then((response) => setCompilations(response));
  }, []);

  return (
    <>
      <div className="compilations">
        {compilations.map((compilation) => (
          <CompilationComponent compilation={compilation} />
        ))}
        <div className="add-compilation">
          <Button cssClass="add-button" onClick={() => navigate("new")}>
            New Compilation
          </Button>
        </div>
      </div>
    </>
  );
}
