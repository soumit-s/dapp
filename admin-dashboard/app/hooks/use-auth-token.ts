import { useLocalStorage } from "usehooks-ts";
export const useAuthToken = () => {
  const [value, setValue, removeValue] = useLocalStorage<string | undefined>(
    "x-user-token",
    undefined,
  );
  return { token: value, setToken: setValue, clearToken: removeValue };
};
