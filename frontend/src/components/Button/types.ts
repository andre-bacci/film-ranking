export interface ButtonProps {
  style?: "box" | "text";
  children: React.ReactNode;
  onClick?: () => void;
  type?: "button" | "submit" | "reset";
  disabled?: boolean;
  cssClass?: string;
}
