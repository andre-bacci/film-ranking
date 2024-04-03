import "./styles.scss";
import { ButtonProps } from "./types";
import clsx from "clsx";

export default function Button({
  children,
  onClick,
  styled = "box",
  type = "button",
  disabled = false,
  cssClass,
}: ButtonProps) {
  return (
    <button
      className={clsx(`button-component ${cssClass}`, {
        "button-text": styled === "text",
        "button-box": styled === "box",
        "button-disabled": disabled,
      })}
      type={type}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
}
