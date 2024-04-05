import clsx from "clsx";
import "./styles.scss";
import { CompilationProps } from "./types";
import Button from "components/Button";
import { useNavigate } from "react-router-dom";

export default function CompilationComponent({
  compilation,
  isList = false,
}: CompilationProps) {
  const navigate = useNavigate();

  return (
    <div
      className={clsx("compilation-wrapper", {
        "compilation-list": isList,
        "compilation-detail": !isList,
      })}
    >
      <div>{compilation.title}</div>
      {isList && (
        <div className="button-wrapper">
          <Button onClick={() => navigate(compilation.id)}>Detail</Button>
          <Button onClick={() => navigate(`${compilation.id}/edit`)}>
            Edit
          </Button>
        </div>
      )}
    </div>
  );
}
