import { ListService } from "services/lists";
import "./styles.scss";
import { useEffect, useState } from "react";
import { Compilation } from "models/Compilation";
import { CompilationComponent } from "components";

export default function CompilationForm() {
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
      </div>
    </>
  );
}
