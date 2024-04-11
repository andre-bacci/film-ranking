export interface SearchProps<T> {
  onSelect: () => void;
  onSearch: () => void;
  items: T[];
}
