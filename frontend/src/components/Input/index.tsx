import "./styles.scss";
import { InputProps } from "./types";

export default function Input({
  label,
  placeholder,
  onChange,
  type,
  ...rest
}: InputProps) {
  return (
    <div className="input-wrapper">
      <div className="input-label">{label}</div>
      <div className="input-box">
        <input
          type={type}
          placeholder={placeholder}
          onChange={onChange}
          className="input-component"
          {...rest}
        />
      </div>
    </div>
  );
}
