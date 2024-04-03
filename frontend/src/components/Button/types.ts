export interface ButtonProps {
  styled?: "box" | "text";
  children: React.ReactNode;
  onClick?: () => void;
  type?: "button" | "submit" | "reset";
  disabled?: boolean;
  cssClass?: string;
}
