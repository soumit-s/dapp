import { Outlet, redirect } from "react-router";
import { getAuthToken } from "~/lib/auth";

export async function clientLoader() {
  const token = getAuthToken();
  if (!token) {
    throw redirect("/login");
  }

  return { isAuthenticated: true };
}

export default function ProtectedRoute() {
  return <Outlet />;
}
