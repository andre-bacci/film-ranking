import "./styles.scss";
import { CompilationProps } from "./types";

export default function CompilationComponent({
  compilation,
}: CompilationProps) {
  return <div className="individual-list-wrapper">{compilation.title}</div>;
}
