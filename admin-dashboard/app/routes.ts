import {
  type RouteConfig,
  index,
  layout,
  route,
} from "@react-router/dev/routes";

export default [
  index("routes/home.tsx"),
  route("/login", "routes/login.tsx"),
  layout("layouts/protectedRoute.layout.tsx", [
    route("/dashboard", "routes/dashboard.tsx"),
    route("/stores", "routes/stores.tsx"),
  ]),
] satisfies RouteConfig;
