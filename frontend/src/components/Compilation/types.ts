import { Compilation } from "models/Compilation";

export interface CompilationProps {
  compilation: Compilation;
  isList?: boolean;
  onDelete?: () => void;
}
