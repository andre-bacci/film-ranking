import "./styles.scss";
import { ButtonProps } from "./types";
import clsx from "clsx";

export default function Button({
  children,
  onClick,
  style = "box",
  type = "button",
  disabled = false,
  cssClass,
}: ButtonProps) {
  return (
    <button
      className={clsx(`button-component ${cssClass}`, {
        "button-text": style === "text",
        "button-box": style === "box",
      })}
      type={type}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
}
