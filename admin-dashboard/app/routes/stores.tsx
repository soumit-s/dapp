import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router";
import { Spinner } from "~/components/ui/spinner";
import { useApiClient } from "~/hooks/use-api-client";

type GetStoresResponse = {
  ok: boolean;
  stores: {
    id: number;
    name: number;
    description: number;
    lat: number;
    long: number;
  }[];
};

export default function Stores() {
  const apiClient = useApiClient();
  const {
    data: stores,
    isLoading,
    error,
  } = useQuery({
    queryKey: ["/v1/admin/stores"],
    queryFn: () =>
      apiClient
        .get<GetStoresResponse>("/v1/admin/stores")
        .then((res) => res.data.stores),
  });

  if (isLoading) {
    return <Spinner />;
  }

  if (error) {
    return <strong className="text-red-500">{error.message}</strong>;
  }

  return (
    <div>
      {stores?.map((store) => (
        <Link to={`${store.id}`}>{store.name}</Link>
      ))}
    </div>
  );
}
